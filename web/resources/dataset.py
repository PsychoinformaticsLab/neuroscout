from flask_apispec import MethodResource, marshal_with, doc
from marshmallow import Schema, fields
from models import Dataset

class DatasetSchema(Schema):
	""" Dataset validation schema. """
	id = fields.Int()
	name = fields.Str(description='Dataset name')
	description = fields.Dict()
	mimetypes = fields.List(fields.Str(),
                         description='Dataset mimetypes/modalities')
	tasks = fields.List(fields.Str(),
                     description='Tasks in dataset runs.')
	runs = fields.Nested('RunSchema', many=True, only='id')
	tasks = fields.Nested('TaskSchema', many=True, only=['id', 'name'])


class DatasetResource(MethodResource):
    @doc(tags=['dataset'], summary='Get dataset by id.')
    @marshal_with(DatasetSchema)
    def get(self, dataset_id):
    	return Dataset.query.filter_by(id=dataset_id).first_or_404()

class DatasetListResource(MethodResource):
    @doc(tags=['dataset'], summary='Returns list of datasets.')
    @marshal_with(DatasetSchema(many=True))
    def get(self):
    	return Dataset.query.all()
