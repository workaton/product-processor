import functools
import logging
import os
from pathlib import Path
import re
from typing import Mapping, Union

import click
import dotenv
from ngitws.cli import initialize
from osgeo import gdal, ogr


ENV_FILES = ['.env', '.env.dist']


def load_env_config(*env_files: Union[Path, str], verbose: bool = False):
    """Load environment variable files."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for env_file in env_files:
                if os.path.isfile(str(env_file)):
                    envs = dotenv.dotenv_values(env_file)
                    if verbose:
                        logging.debug(f'Loading environment from {env_file}')
                        for name, value in envs.items():
                            if name in os.environ:
                                if verbose:
                                    logging.debug(f'Ignoring environment variable {name}; already set')
                            else:
                                os.environ[name] = value
                                if verbose:
                                    if re.match(r'(PASSWORD|SECRET)', value, re.IGNORECASE):
                                        value = '*' * len(value)
                                    logging.debug(f'Setting environment variable {name}={value}')
                    dotenv.load_dotenv(dotenv_path=str(env_file))

            return func(*args, **kwargs)
        return wrapper
    return decorator


def logging_levels(levels: Mapping[str, int]):
    """Set special logging levels."""
    def decorator(func):
        for name, level in levels.items():
            logging.getLogger(name).setLevel(level)
        return func

    return decorator


@logging_levels({'shapely.geos': logging.INFO})
@initialize()
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@load_env_config(*ENV_FILES, verbose=False)
def main():
    """Application for managing products submitted to the NGITWS catalog system."""
    gdal.UseExceptions()
    ogr.UseExceptions()
