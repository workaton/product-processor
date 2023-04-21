from contextlib import ExitStack
import json
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, MadisJsonConverter
from app.media_types import MediaTypes
import pytest
from tests.conftest import compare_xml


class TestMadisJsonConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = MadisJsonConverter()
        with ExitStack() as stack:
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            metadata = json.loads(METADATA)
            metadata_byte_string = json.dumps(metadata['Doc']).encode('utf-8')
            results = await converter.convert([ConversionInput(metadata_byte_string, MediaTypes.APPLICATION_JSON)])

        xml_tree = etree.fromstring(XML)
        for result in results:
            assert len(result.data) > 0
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)


METADATA = b'''\
    {
        "Storage": {
            "Publisher": "ngitws",
            "Publish-Date": "2020-08-06T13:31:30Z",
            "Object-Identities": [
                {
                    "Catalog-Identifier": "NGITWS_OBJECTS",
                    "Record-Identifier": "60b02828-a099-4135-ad94-c765ea7a2db2",
                    "@id": "http://nids-objws.cp.ncep.noaa.gov:8080/objws/v1/catalogs/NGITWS_OBJECTS/objects/60b02828-a099-4135-ad94-c765ea7a2db2"
                }
            ],
            "Record-Identifier": "27964b10-356c-42a9-abd2-96ec6ef50a20",
            "@id": "http://nids-metaws.cp.ncep.noaa.gov:8080/metaws/v1/catalogs/NGITWS_MADIS_CSV_METADATA/records/27964b10-356c-42a9-abd2-96ec6ef50a20"
        },
        "Doc": {
            "feed": "MADIS_MESONET",
            "observationTime": 1596720000000,
            "dataProvider": "APRSWXNET",
            "subProvider": null,
            "stationId": "D1880",
            "dewpoint": {
                "value": 287.71112,
                "unit": "kelvin",
                "qc": "V"
            },
            "elevation": {
                "value": 309.09,
                "unit": "meter",
                "qc": "Z"
            },
            "seaLevelPressure": {
                "value": null,
                "unit": "pascal",
                "qc": "Z"
            },
            "altimeter": {
                "value": 101980.0,
                "unit": "pascal",
                "qc": "V"
            },
            "temperature": {
                "value": 292.03888,
                "unit": "kelvin",
                "qc": "V"
            },
            "windDir": {
                "value": 310.0,
                "unit": "degree",
                "qc": "V"
            },
            "windSpeed": {
                "value": 0.0,
                "unit": "meter/sec",
                "qc": "V"
            },
            "windGust": {
                "value": 0.0,
                "unit": "meter/sec",
                "qc": "S"
            },
            "visibility": {
                "value": null,
                "unit": "meter",
                "qc": "Z"
            },
            "presentWeather": null,
            "skyCover": [
                null,
                null,
                null,
                null,
                null,
                null
            ],
            "skyLayerBase": [
                null,
                null,
                null,
                null,
                null,
                null
            ],
            "skyLayerBaseUnit": "meter",
            "precipitationLast3Hours": {
                "value": null,
                "unit": "meter",
                "qc": "Z"
            },
            "maxTemp24Hour": {
                "value": null,
                "unit": "kelvin",
                "qc": null
            },
            "minTemp24Hour": {
                "value": null,
                "unit": "kelvin",
                "qc": null
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -89.2225,
                    43.19167
                ]
            }
        }
    }
'''  # noqa: E501


XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><MesonetSurfaceObservation xmlns:gml="http://www.opengis.net/gml/3.2" xmlns="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/mesonetSurfaceObservation.xsd" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><siteIdentification><SiteIdentificationAndProperties><siteIdentifier>D1880</siteIdentifier><location><gml:Point axisLabels="Lat Long" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:pos>43.191670 -89.222500</gml:pos></gml:Point></location><networkName>APRSWXNET</networkName><subNetworkName /></SiteIdentificationAndProperties></siteIdentification><observationTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-06T13:20:00Z</gml:timePosition></gml:TimeInstant></observationTime><airTemperature uom="K">292.0</airTemperature><dewpointTemperature uom="K">287.7</dewpointTemperature><qnh uom="hPa">1019.8000000000001</qnh><windDirection uom="deg">310</windDirection><windSpeed uom="m/s">0.0</windSpeed><windGust uom="m/s">0.0</windGust></MesonetSurfaceObservation>
'''  # noqa: E501
