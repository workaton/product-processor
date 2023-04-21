from __future__ import annotations

import asyncio
import io
import logging
import subprocess
from typing import Sequence

from app.media_types import MediaTypes
from PIL import Image

from .base import ConversionInput, ConversionResult, Converter


class GfaConverter(Converter):
    """Converts Canadian GFA fax files to PNG images."""

    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger(__name__)

    async def _convert(self, inputs: Sequence[ConversionInput]) -> Sequence[ConversionResult]:
        try:
            process = await asyncio.create_subprocess_shell(
                'g3topbm',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except OSError as ex:
            raise RuntimeError('Error setting up g3topbm to convert Canadian GFA') from ex
        else:
            stdout, stderr = await process.communicate(inputs[0].data)
            messages = stderr.decode('utf-8')
            if process.returncode:
                raise RuntimeError(f'g3topbm returned error converting Canadian GFA to intermediate PBM:\n{messages}')

            if messages:
                self.__logger.debug(f'g3topbm conversion of Canadian GFA to PBM image completed:\n{messages}')
            else:
                self.__logger.debug('g3topbm conversion of Canadian GFA to PBM image completed')

            infile = io.BytesIO(stdout)
            outfile = io.BytesIO()
            try:
                with Image.open(infile) as image:
                    image.save(outfile, 'png')
            except IOError as ex:
                raise RuntimeError('Error converting intermediate PBM image of Canadian GFA to PNG') from ex

            outfile.seek(0)
            return [ConversionResult(outfile.read(), MediaTypes.IMAGE_PNG, id='GFA')]
