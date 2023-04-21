from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, MisConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestMisConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = MisConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-07-27T14:32:37Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])

        xml_tree = etree.fromstring(XML)
        for result in results:
            assert len(result.data) > 0
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)


TAC = b'''\
\r\r\n
000\r\r\n
FAUS20 KZNY 131807\r\r\n
ZNY MIS 01 VALID 131815-140230\r\r\n
...FOR ATC PLANNING PURPOSES ONLY...\r\r\n
THE CWSU AT ZNY WILL BE COVERED REMOTELY BTW 1830-0230Z AND CAN BE\r\r\n
REACHED VIA EMAIL ZNY.OPERATIONS@NOAA.GOV. NORMAL ON-SITE COVERAGE\r\r\n
RESUMES AT 1030Z TUESDAY.\r\r\n
=\r\r\n
\r\r\n
'''  # noqa: E501

XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><uswx:MeteorologicalImpactStatement xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/mis.xsd" status="NORMAL" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:centerWeatherServiceUnit gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><saf:name>New York City Center Weather Service Unit</saf:name><saf:type>MWO</saf:type><saf:designator>ZNY</saf:designator></uswx:centerWeatherServiceUnit><uswx:sequenceIssuance>1</uswx:sequenceIssuance><uswx:meteorologicalImpactStatementRecord gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:phenomenonTime><gml:TimePeriod gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition>2020-07-13T18:15:00</gml:beginPosition><gml:endPosition>2020-07-14T02:30:00</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-13T18:07:00</gml:timePosition></gml:TimeInstant></om:resultTime><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01008003curr.pdf" /><om:observedProperty xlink:href="https://nws.weather.gov/schemas/USWX/observedProperties/MeteorologicalImpactStatement" /><om:featureOfInterest xlink:href="https://nws.weather.gov/schemas/USWX/geodata/artcc/ZNY.xml" /><om:result><uswx:MeteorologicalImpactStatementText><uswx:misText>THE CWSU AT ZNY WILL BE COVERED REMOTELY BTW 18300230Z AND CAN BE\n\nREACHED VIA EMAIL ZNY.OPERATIONSNOAA.GOV. NORMAL ONSITE COVERAGE\n\nRESUMES AT 1030Z TUESDAY.</uswx:misText></uswx:MeteorologicalImpactStatementText></om:result></uswx:meteorologicalImpactStatementRecord></uswx:MeteorologicalImpactStatement>
'''  # noqa: E501
