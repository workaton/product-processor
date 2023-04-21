from contextlib import AsyncExitStack
from io import BytesIO
import json
import logging
import os
from pathlib import Path
import re
import sys
import traceback
from typing import List, Optional, Sequence

from aio_msgpack_rpc.error import RPCResponseError
from app.config import Configuration
from app.converters import ConversionInput, ConversionResult, CONVERTERS
from app.daemon import Daemon
from app.extractors import EXTRACTORS
from app.handlers import HANDLERS
from app.resources import ResourceManager
from app.rpc import RpcClient
import click
from ngitws.catalog import CatalogIdentity
from ngitws.cli import async_command, MissingEnvironmentVariableError, Path as PathType, standard_options
from ngitws.logging import is_debug_enabled
from ngitws.monitoring import OperationResult, report_operation
from ngitws.types import MediaType

from .console import Console
from .main import main


@main.command('convert')
@click.option('-S', '--socket-path', type=PathType(), help='Path to daemon socket')
@click.option('-l', '--list', 'list_types', is_flag=True, help='List supported converter types')
@click.option('-v', '--verbose', is_flag=True, help='Show verbose output')
@standard_options('app')
@click.argument('converter_name', required=False)
@click.argument('input_files', nargs=-1, required=False)
@async_command
async def convert(
    converter_name: Optional[str],
    input_files: Sequence[str],
    list_types: bool,
    socket_path: Path,
    verbose: bool
):
    """Convert a file from one format to another.

    Each input_file may either be a path name or take the form of 'id=input_file_path' to associate an id with the file.
    """
    console = Console()
    if is_debug_enabled():
        verbose = True
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if list_types:
        name_width = max([len(name) for name in CONVERTERS])
        for name, converter_class in CONVERTERS.items():
            console.text(f'{name:<{name_width}}  {converter_class.description()}')
        return

    if not converter_name or not input_files:
        console.text(click.get_current_context().get_help())
        return 1

    config = Configuration(os.environ)
    conversion_inputs = _create_conversion_inputs(input_files)
    conversion_results: Sequence[ConversionResult] = []
    if socket_path is None:
        try:
            # Try to run locally first.
            async with ResourceManager(config) as resources:
                converter = await resources.converter(converter_name)
                conversion_results = await converter.convert(conversion_inputs)
        except MissingEnvironmentVariableError:
            # Fall back on socket.
            socket_path = config.socket_path
    if socket_path is not None:
        try:
            async with AsyncExitStack() as stack:
                try:
                    client = await stack.enter_async_context(RpcClient(socket_path))
                except (FileNotFoundError, ConnectionRefusedError):
                    console.error(f'Could not connect to socket at {socket_path} -- is the daemon running?')
                    return 1

                conversion_results = await client.run_converter(converter_name, conversion_inputs)
        except RPCResponseError as ex:
            console.error(f'Request failed: {str(ex)}')
            return 1
        except:  # noqa: E722
            console.error(f'Converter failed unexpectedly:\n{traceback.format_exc()}')
            return 1

    for result in conversion_results:
        console.info(f'Produced output of type {result.media_type}')
        sys.stdout.buffer.write(result.data)
        sys.stdout.buffer.write(b'\n')


@main.command('daemon')
@click.option('-S', '--socket-path', type=PathType(), help='Path to daemon socket')
@click.option('-v', '--verbose', is_flag=True, help='Show verbose output')
@click.option('-H', '--handlers', multiple=True, help='Only register the indicated handlers')
@click.option('-P', '--no-pubsub', is_flag=True, help='Disable pubsub integration')
@standard_options('app', default_log_format='EXTRA')
@async_command
async def daemon(handlers: Sequence[str], no_pubsub: bool, socket_path: Path, verbose: bool):
    """Run the application as a pubsub daemon."""
    config = Configuration(os.environ)
    if is_debug_enabled():
        verbose = True
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    use_pubsub = not no_pubsub
    if not socket_path:
        socket_path = config.socket_path

    async with Daemon(config=config, handlers=handlers, pubsub=use_pubsub, socket_path=socket_path) as app:
        await app.run()


@main.command('extract')
@click.option('-S', '--socket-path', type=PathType(), help='Path to daemon socket')
@click.option('-l', '--list', 'list_types', is_flag=True, help='List supported extractor types')
@click.option('-v', '--verbose', is_flag=True, help='Show verbose output')
@standard_options('app')
@click.argument('extractor_name', required=False)
@click.argument('input_file', type=click.File('rb'), required=False)
@async_command
async def extract(
    extractor_name: Optional[str],
    input_file: Optional[BytesIO],
    list_types: bool,
    socket_path: Path,
    verbose: bool
):
    """Extract metadata from a file."""
    console = Console()
    if is_debug_enabled():
        verbose = True
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if list_types:
        name_width = max([len(name) for name in EXTRACTORS])
        for name, extractor_class in EXTRACTORS.items():
            console.text(f'{name:<{name_width}}  {extractor_class.description()}')
        return 0

    if not extractor_name or not input_file:
        console.text(click.get_current_context().get_help())
        return 1
    data = input_file.read()

    config = Configuration(os.environ)
    if socket_path is None:
        try:
            # Try to run locally first.
            async with ResourceManager(config) as resources:
                extractor = await resources.extractor(extractor_name)
                extracted = await extractor.extract(data)
        except MissingEnvironmentVariableError:
            # Fall back on socket.
            socket_path = config.socket_path
    if socket_path is not None:
        try:
            async with AsyncExitStack() as stack:
                try:
                    client = await stack.enter_async_context(RpcClient(socket_path))
                except (FileNotFoundError, ConnectionRefusedError):
                    console.error(f'Could not connect to socket at {socket_path} -- is the daemon running?')
                    return 1

                extracted = await client.run_extractor(extractor_name, data)
        except RPCResponseError as ex:
            console.error(f'Request failed: {str(ex)}')
            return 1
        except:  # noqa: E722
            console.error(f'Extractor failed unexpectedly:\n{traceback.format_exc()}')
            return 1

    click.echo(json.dumps(extracted, indent=2))
    return 0


@main.command('run')
@click.option('-S', '--socket-path', type=PathType(), help='Path to daemon socket')
@click.option('-l', '--list', 'list_types', is_flag=True, help='List supported handler types')
@click.option('-v', '--verbose', is_flag=True, help='Show verbose output')
@standard_options('app')
@click.argument('handler_name', required=False)
@click.argument('record', required=False)
@async_command
async def run(handler_name: Optional[str], record: Optional[str], list_types: bool, socket_path: Path, verbose: bool):
    """Process a catalog record using a specific processor.

    The RECORD argument takes the format <CATALOG ID:RECORD ID>.
    Example: NGITWS_CATALOG:foobar

    """
    console = Console()
    if is_debug_enabled():
        verbose = True
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if list_types:
        name_width = max([len(name) for name in HANDLERS])
        for name, handler_class in HANDLERS.items():
            console.text(f'{name:<{name_width}}  {handler_class.description()}')
        return

    if not handler_name or not record:
        console.text(click.get_current_context().get_help())
        return 1

    match = re.match(r'^([A-Za-z0-9_]+):([A-Za-z0-9._-]+)$', record)
    if not match:
        console.error('Must provide a valid record in the form <CATALOG ID>:<RECORD ID>')
        return 1
    identity = CatalogIdentity(match.group(1), match.group(2))

    config = Configuration(os.environ)

    with report_operation('run') as operation:
        if socket_path is None:
            try:
                # Try to run locally first.
                async with ResourceManager(config) as resources:
                    handler = await resources.handler(handler_name)
                    await handler.run(identity, operation)
            except MissingEnvironmentVariableError:
                # Fall back on socket.
                socket_path = config.socket_path
        if socket_path is not None:
            try:
                async with AsyncExitStack() as stack:
                    try:
                        client = await stack.enter_async_context(RpcClient(socket_path))
                    except (FileNotFoundError, ConnectionRefusedError):
                        console.error(f'Could not connect to socket at {socket_path} -- is the daemon running?')
                        return 1

                await client.run_handler(handler_name, identity, operation)
            except RPCResponseError as ex:
                console.error(f'Request failed: {str(ex)}')
                return 1
            except:  # noqa: E722
                console.error(f'Handler failed unexpectedly:\n{traceback.format_exc()}')
                return 1

    message = operation.result.name
    if operation.message:
        message = f'{message}: {operation.message}'
    if verbose and operation.error:
        stack_trace = ''.join(traceback.format_exception(
            operation.error.__class__.__name__,
            operation.error,
            operation.error.__traceback__
        ))
        message = f'{message}\n{stack_trace}'

    if operation.result == OperationResult.PASS:
        console.info(message)
    elif operation.result in (OperationResult.DEFER, OperationResult.SKIP):
        console.warning(message)
    else:
        console.error(message)


def _create_conversion_inputs(input_files: Sequence[str]) -> Sequence[ConversionInput]:
    conversion_inputs: List[ConversionInput] = []
    stdin_read = False
    for input_file in input_files:
        match = re.match(r'^(?:(?P<id>[^:]*)=)?(?P<path>[^:]+)(?::(?P<media>[^:]+/[^:]+))?$', input_file)
        if not match:
            raise RuntimeError(f'Did not recognize input: {input_file}')

        input_id = match.group('id')
        filename = match.group('path')
        media_type = MediaType.parse(match.group('media') or 'application/octet-stream')

        if filename == '-':
            if stdin_read is True:
                raise RuntimeError('Cannot read stdin for more than one input')
            data = sys.stdin.buffer.read()
            stdin_read = True
        else:
            with open(filename, 'rb') as file:
                data = file.read()

        conversion_inputs.append(ConversionInput(data, media_type, id=input_id))

    return conversion_inputs
