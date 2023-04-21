from app.extractors import MadisCsvExtractor
import pytest


class TestMadisCsvExtractor:

    @pytest.fixture
    def extractor(self):
        return MadisCsvExtractor()

    @pytest.mark.asyncio
    async def test_extract_maritime(self, extractor):
        assert await extractor.extract(MARITIME) == {
            'feed': 'MADIS_MARITIME',
            'timestamp': '2020-12-31T14:44:00.000Z',
            'observationTime': 1609425840000,
            'dataProvider': 'MARITIME',
            'subProvider': None,
            'stationId': 'SCXA2',
            'dewpoint': {
                'value': 273.55,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'elevation': {
                'value': 15.0,
                'unit': 'meter',
                'qc': 'Z'
            },
            'seaLevelPressure': {
                'value': 100600.0,
                'unit': 'pascal',
                'qc': 'V'
            },
            'altimeter': {
                'value': None,
                'unit': 'pascal',
                'qc': 'Z'
            },
            'temperature': {
                'value': 273.95,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'windDir': {
                'value': None,
                'unit': 'degree',
                'qc': 'Z'
            },
            'windSpeed': {
                'value': None,
                'unit': 'meter/sec',
                'qc': 'Z'
            },
            'windGust': {
                'value': 9.3,
                'unit': 'meter/sec',
                'qc': 'S'
            },
            'visibility': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'presentWeather': None,
            'precipitationLastHour': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'precipitationLast6Hours': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    -134.65,
                    58.21
                ]
            }
        }

    @pytest.mark.asyncio
    async def test_extract_mesonet(self, extractor):
        assert await extractor.extract(MESONET) == {
            'feed': 'MADIS_MESONET',
            'timestamp': '2020-12-31T14:40:00.000Z',
            'observationTime': 1609425600000,
            'dataProvider': 'MesoWest',
            'subProvider': 'TWDB',
            'stationId': 'TWB55',
            'dewpoint': {
                'value': 274.99,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'elevation': {
                'value': 216.4,
                'unit': 'meter',
                'qc': 'Z'
            },
            'seaLevelPressure': {
                'value': None,
                'unit': 'pascal',
                'qc': 'Z'
            },
            'altimeter': {
                'value': 101480.69,
                'unit': 'pascal',
                'qc': 'V'
            },
            'temperature': {
                'value': 275.63,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'windDir': {
                'value': 37.0,
                'unit': 'degree',
                'qc': 'V'
            },
            'windSpeed': {
                'value': 6.75,
                'unit': 'meter/sec',
                'qc': 'V'
            },
            'windGust': {
                'value': 11.33,
                'unit': 'meter/sec',
                'qc': 'S'
            },
            'visibility': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'presentWeather': None,
            'skyCover': [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            'skyLayerBase': [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            'skyLayerBaseUnit': 'meter',
            'precipitationLast3Hours': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'maxTemp24Hour': {
                'value': None,
                'unit': 'kelvin',
                'qc': None
            },
            'minTemp24Hour': {
                'value': None,
                'unit': 'kelvin',
                'qc': None
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    -97.21,
                    32.4
                ]
            }
        }

    @pytest.mark.asyncio
    async def test_extract_metar(self, extractor):
        assert await extractor.extract(METAR) == {
            'feed': 'MADIS_METAR',
            'timestamp': '2020-12-30T20:56:00.000Z',
            'observationTime': 1609361760000,
            'dataProvider': 'OTHER-MTR',
            'subProvider': None,
            'stationId': 'KWVL',
            'dewpoint': {
                'value': 262.05,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'elevation': {
                'value': 101.0,
                'unit': 'meter',
                'qc': 'Z'
            },
            'seaLevelPressure': {
                'value': None,
                'unit': 'pascal',
                'qc': 'Z'
            },
            'altimeter': {
                'value': 102070.0,
                'unit': 'pascal',
                'qc': 'V'
            },
            'temperature': {
                'value': 271.45,
                'unit': 'kelvin',
                'qc': 'V'
            },
            'windDir': {
                'value': None,
                'unit': 'degree',
                'qc': 'Z'
            },
            'windSpeed': {
                'value': 3.1,
                'unit': 'meter/sec',
                'qc': 'V'
            },
            'windGust': {
                'value': None,
                'unit': 'meter/sec',
                'qc': 'Z'
            },
            'visibility': {
                'value': 16090.0,
                'unit': 'meter',
                'qc': 'C'
            },
            'presentWeather': None,
            'rawMessage': 'KWVL 302056Z AUTO VRB06KT 10SM FEW050 SCT060 M02/M11 A3014 RMK AO2 SLP239 T10171111 56033 FZRANO',  # noqa: E501 -- it's just that long
            'skyCover': [
                'FEW',
                'SCT',
                None,
                None,
                None,
                None
            ],
            'skyLayerBase': [
                1520.0,
                1830.0,
                None,
                None,
                None,
                None
            ],
            'skyLayerBaseUnit': 'meter',
            'precipitationLastHour': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'precipitationLast3Hours': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'precipitationLast6Hours': {
                'value': None,
                'unit': 'meter',
                'qc': 'Z'
            },
            'maxTemp24Hour': {
                'value': None,
                'unit': 'kelvin',
                'qc': None
            },
            'minTemp24Hour': {
                'value': None,
                'unit': 'kelvin',
                'qc': None
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    -69.68,
                    44.53
                ]
            }
        }


MARITIME = b''' SCXA2     ,12/31/2020,14:44,MARITIME  ,           ,   273.549988,V,-99999.000000,Z,100600.000000,V,   273.950012,V,-99999.000000,Z,-99999.000000,Z,-99999.000000,Z,    15.000000,Z,    58.209999,Z,  -134.649994,Z,-99999.000000,Z,-99999.000000,Z,-99999.000000,Z,     9.300000,S,,             ,,             ,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,                         ,        ,        ,        ,        ,        ,         ,                                                                                                                                                                                                                                                                '''  # noqa: E501


MESONET = b''' TWB55     ,12/31/2020,14:40,MesoWest  ,TWDB       ,   274.988007,V,101480.687500,V,-99999.000000,Z,   275.632996,V,    37.000000,V,     6.755000,V,-99999.000000,Z,   216.399994,Z,    32.398911,Z,   -97.208794,Z,-99999.000000,Z,-99999.000000,Z,-99999.000000,Z,    11.328000,S,,             ,,             ,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,                         ,        ,        ,        ,        ,        ,         ,                                                                                                                                                                                                                                                                '''  # noqa: E501


METAR = b''' KWVL      ,12/30/2020,20:56,OTHER-MTR ,           ,   262.049988,V,102070.000000,V,-99999.000000,Z,   271.450012,V,-99999.000000,Z,     3.100000,V, 16090.000000,C,   101.000000,Z,    44.529999,Z,   -69.680000,Z,-99999.000000,Z,-99999.000000,Z,-99999.000000,Z,-99999.000000,Z,,             ,,             ,  1520.000000,Z,  1830.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,999999.000000,Z,                         ,FEW     ,SCT     ,        ,        ,        ,         ,KWVL 302056Z AUTO VRB06KT 10SM FEW050 SCT060 M02/M11 A3014 RMK AO2 SLP239 T10171111 56033 FZRANO                                                                                                                                                                '''  # noqa: E501
