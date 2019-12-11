# Usage

This assumes that you are using the Docker Container.
Docker commands for _neuroscout-cli_ will always being with:

    docker run -it

Assuming you've already created an analysis on neuroscout.org, and have its analysis id (e.g.: `5xH93`), you can run it in one line:

    docker run -it neuroscout/neuroscout-cli run /outdir 5xH93

Neuroscout will download the necessary images, analysis bundle, and fit your model.

## Mounting Volumes

Most likely, you'll want to mount at least two volumes , in order to cache input data (`/data`), and inspect output results (`/out`)

In this example, we mount both of these directories to local volumes:

    docker run -it -v /local/datadir:/data -v /local/outdir:/out neuroscout/neuroscout-cli run /out 5xH937f

The necessary dataset will be downloaded to your local volume (`/local/datadir`), and next time you run a model with the same dataset, it will not need to re-download the fMRI data.
The model-fitting outputs will also be locally saved at `/local/outdir`.


## Command-Line Arguments

    neuroscout

    Usage:
        neuroscout run [-ui <dir> -s <k> -w <dir> -c <n> -n <nv> -d] <outdir> <bundle_id>...
        neuroscout install [-ui <dir>] <bundle_id>...
        neuroscout ls <bundle_id>
        neuroscout -h | --help
        neuroscout --version


### Commands (first positional argument)

#### run                      
Runs analysis. Downloads data if necessary.

#### install
Download analysis bundle, and download data if necessary.

#### ls       
List input fMRI data files associated with this analysis, to be downloaded.

### Options

#### -i, --install-dir <dir>  

Directory to download data. Default is current directory, which is `/data`.


#### -w, --work-dir <dir>    

Path where intermediate results should be stored

#### -c, --n-cpus <n>         

Maximum number of threads across all processes [default: 1]

#### -s, --smoothing <k>      

Smoothing kernel FWHM at group level [default: 4]

#### -u, --unlock             

Unlock datalad dataset (only necessary if mapping to local dataset)

#### -n, --neurovault <nv>    

Upload mode (disable, force, or enable) [default: enable]

Options:

 - Enable - Upload results to Neurovault
 - Force - Force upload, with a new collection name if necessary.
 - Disable - Don't upload to Neurovault.

#### -d, --drop-missing

Drop missing inputs/contrasts in model fitting.
Necessary in cases where a run has no events of a given type, and no inputs
are available at the next level for fitting.