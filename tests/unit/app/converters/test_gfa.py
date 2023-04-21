from app.converters import ConversionInput, GfaConverter
from app.media_types import MediaTypes
import pytest
from tests.conftest import read_sample_binary_file


class TestGfaConverter:

    @pytest.fixture
    def converter(self):
        return GfaConverter()

    @pytest.mark.asyncio
    async def test_convert(self, converter):
        g3 = read_sample_binary_file('gfa.g3')
        png = read_sample_binary_file('gfa.png')

        result = await converter.convert([ConversionInput(g3, MediaTypes.IMAGE_G3FAX)])
        assert len(result) == 1
        assert result[0].media_type == MediaTypes.IMAGE_PNG
        assert result[0].data == png
