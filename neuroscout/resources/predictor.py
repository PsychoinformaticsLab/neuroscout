from marshmallow import Schema, fields, post_dump
import webargs as wa
from flask_apispec import MethodResource, marshal_with, use_kwargs, doc
from models import Predictor, PredictorEvent, PredictorRun
from .utils import first_or_404, make_cache_key
from sqlalchemy import func
from database import db
from sqlalchemy.dialects import postgresql
from core import cache


class ExtractedFeatureSchema(Schema):
    id = fields.Int(description="Extractor id")
    description = fields.Str(description="Feature description.")
    created_at = fields.Str(description="Extraction timestamp.")
    extractor_name = fields.Str(description="Extractor name.")
    modality = fields.Str()


class PredictorSchema(Schema):
    id = fields.Int()
    name = fields.Str(description="Predictor name.")
    description = fields.Str(description="Predictor description")
    extracted_feature = fields.Nested('ExtractedFeatureSchema', skip_if=None)
    source = fields.Str()

    max = fields.Float(description="Maximum value")
    min = fields.Float(description="Minimum value")
    mean = fields.Float(description="Mean value")
    stddev = fields.Float(description="Standard deviation of value")
    num_na = fields.Int(description="Number of missing values")

    @post_dump
    def remove_null_values(self, data):
        if data.get('extracted_feature', True) is None:
            data.pop('extracted_feature')
        return data


class PredictorEventSchema(Schema):
    id = fields.Str()
    onset = fields.Number(description="Onset in seconds.")
    duration = fields.Number(description="Duration in seconds.")
    value = fields.Str(description="Value, or amplitude.")
    run_id = fields.Int()
    predictor_id = fields.Int()


def dump_pe(pes):
    """ Serialize PredictorEvents, with *SPEED*, using core SQL.
    Warning: relies on attributes being in correct order. """
    statement = str(pes.statement.compile(dialect=postgresql.dialect()))
    params = pes.statement.compile(dialect=postgresql.dialect()).params
    res = db.session.connection().execute(statement, params)
    return [{
      'id': r[0],
      'onset': r[1],
      'duration': r[2],
      'value':  r[3],
      'run_id': r[5],
      'predictor_id': r[6]
      } for r in res]


class PredictorRunSchema(Schema):
    run_id = fields.Int()
    mean = fields.Number()
    stdev = fields.Number()


class PredictorResource(MethodResource):
    @doc(tags=['predictors'], summary='Get predictor by id.')
    @marshal_with(PredictorSchema)
    def get(self, predictor_id, **kwargs):
        return first_or_404(Predictor.query.filter_by(id=predictor_id))


def get_predictors(newest=True, **kwargs):
    """ Helper function for querying newest predictors """
    if newest:
        predictor_ids = db.session.query(
            func.max(Predictor.id)).group_by(Predictor.name)
    else:
        predictor_ids = db.session.query(Predictor.id)

    if 'run_id' in kwargs:
        # This following JOIN can be slow
        predictor_ids = predictor_ids.join(PredictorRun).filter(
            PredictorRun.run_id.in_(kwargs.pop('run_id')))

    query = Predictor.query.filter(Predictor.id.in_(predictor_ids))
    for param in kwargs:
        query = query.filter(getattr(Predictor, param).in_(kwargs[param]))

    # Only display active predictors
    return query.filter_by(active=True).all()


class PredictorListResource(MethodResource):
    @doc(tags=['predictors'], summary='Get list of predictors.',)
    @use_kwargs({
        'run_id': wa.fields.DelimitedList(
            fields.Int(), description="Run id(s). Warning, slow query."),
        'name': wa.fields.DelimitedList(fields.Str(),
                                        description="Predictor name(s)"),
        'newest': wa.fields.Boolean(
            missing=True,
            description="Return only newest Predictor by name")
        },
        locations=['query'])
    @cache.cached(key_prefix=make_cache_key)
    @marshal_with(PredictorSchema(many=True))
    def get(self, **kwargs):
        newest = kwargs.pop('newest')
        return get_predictors(newest=newest, **kwargs)


class PredictorEventListResource(MethodResource):
    @doc(tags=['predictors'], summary='Get events for predictor(s)',)
    @cache.cached(60 * 60 * 24 * 300, key_prefix=make_cache_key)
    @use_kwargs({
        'run_id': wa.fields.DelimitedList(
            fields.Int(),
            description="Run id(s)"),
        'predictor_id': wa.fields.DelimitedList(
            fields.Int(),
            description="Predictor id(s)"),
    }, locations=['query'])
    def get(self, **kwargs):
        query = PredictorEvent.query
        for param in kwargs:
            query = query.filter(
                getattr(PredictorEvent, param).in_(kwargs[param]))
        return dump_pe(query.all())
