# product-processor

The product processor core is an NGITWS pubsub application that performs operations on incoming files and records as they are added to the catalog system.


## Requirements

* Python 3.8+ (python3)
* Python 3 development kit (python3-devel)
* libjpeg development kit (libjpeg-turbo-devel)
* zlib development kit (zlib-devel)
* [Poetry] 1.0+


## Setting up for development

After cloning the project and ensuring that any dependencies are installed, run the following command:

```sh
make dev
```

Assuming the command completes successfully, the project is set up and can be executed via the command line interface.  Convenient linting and testing are also available via `make lint` and `make test`, both of which are run as part of the build pipeline.

As this project uses a modern PEP-518 compliant build system, Poetry is the package and dependency manager rather than the traditional setuptools, and _pyproject.toml_ serves as the configuration file in place of _setup.py_ or _setup.cfg_.


### Using docker-compose

Using docker-compose requires either the `docker-compose` or `podman-compose` system package.  Once installed, run the following command in the project root to run and attach to a container:

```sh
docker-compose run app
```

In the event you need to alter and rebuild the image, run:

```sh
docker-compose build
```


## Command line interface

The command line interface for the product processor is available via `bin/product-processor` once the development environment is set up.  Running this command without arguments will provide a list of subcommands.  Use the `--help` flag in conjunction with these to see more information.  In most cases where commands take file arguments, `-` will instead read from standard input.

In addition to running the main daemon program, this program also performs resource operations on files, such as conversion and metadata extraction.  See the help output for more details.


## Registering resources

The project has a number of resource types, which are loosely coupled via entry points and the `app.resources.ResourceManager` class.  This provides some dedicated resources but also allows for the following pluggable resources:

* converters
* extractors
* splitters
* SPOT (STQ & FWS)

In general, registering a pluggable resource involves adding an entry to the project's _pyproject.toml_ of the form:

```
<name> = <module>:<class>
```


### Converters

Converters transform data from one format to another.  They must be descendants of `app.converters.base.ConverterBase`, and by convention they expose an async `convert` method which accepts a byte string and returns a `ConversionResult` containing both the output byte string and a media type.  The method signature may vary somewhat; for example, `SpcWatchConverter` takes both a SAW and a SEL product and returns a result object containing a `ConversionResult` for each.

Converters are registered by class in the `app.converters` entry point group.

```toml
[tool.poetry.plugins."app.converters"]
METAR-COLLECTIVE = app.converters.metar:MetarCollectiveConverter
```


### Extractors

Extractors assemble a hierarchical data structure from input data and must be descendants of `app.extractors.base.ExtractorBase`.  By convention, they expose an async `extract` method which accepts a byte string and returns a JSON-compatible `JsonType` (see `ngitws.typing`) data structure.  Usually, this will be a dictionary, but it can vary; collective converters return lists of dictionaries, for example.

Extractors are registered by class in the `app.extractors` entry point group.

```toml
[tool.poetry.plugins."app.extractors"]
TAF = "app.extractors:TafExtractor"
```


### Splitters

Splitters separate input data into multiple parts and must be descendants of `app.splitters.base.SplitterBase`.  By convention, they expose an async `split` method which accepts a byte string and returns a sequence of them.

Splitters are registered by class in the `app.splitters` entry point group.

```toml
[tool.poetry.plugins."app.splitters"]
IWXXM = "app.splitters:IwxxmSplitter"
```

[poetry]: https://python-poetry.org/docs/


### SPOT (STQ & FWS)

The Product-Processor handles JSON and text file products needed by the SPOT application. Those being `STQ` and `FWS` files objects.

#### STQ:
Process JSON data posted by SPOT in the SPOT_RQUESTS catalog to create the STQ files, which are then posted into SPOT_STQ_FILES and SPOT_STQ_METADATA respectively. 

STQ files are conformed using a jinja2 template. 

#### FWS:
Extract data from text file objects posted in NGITWS_FWS_FILES catalog. These data is then posted in NGITWS_FWS_METADATA.

Both the text file object and the data extracted are sent to SPOT via the SPOT-API. 