from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import AirepConverter, ConversionInput
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestAirepConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = AirepConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-08-13T17:00:00Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])

        for result in results:
            assert len(result.data) > 0
            xml_tree = etree.fromstring(XML)
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)


TAC = b'''\
\r\r\n
000\r\r\n
UAUS31 KWBC 131709\r\r\n
ARP UAL1738 3816N 09429W 1700 F390 MS55 292/049KT TB LGT=\r\r\n
\r\r\n
'''  # noqa: E501

XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><iwxxm-us:AircraftReport xmlns:iwxxm="http://icao.int/iwxxm/1.1" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:om="http://www.opengis.net/om/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:aixm="http://www.aixm.aero/schema/5.1" xmlns:metce="http://def.wmo.int/metce/2013" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release https://nws.weather.gov/schemas/iwxxm-us/1.0/aircraftreport.xsd" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:flightLevelUnknownFlag>false</iwxxm-us:flightLevelUnknownFlag><iwxxm-us:observation><om:OM_Observation gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/AircraftReportObservation" /><om:phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-13T17:00:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#uuid.a36a2138-2c09-473e-bd0d-916531537b02" /><om:procedure><metce:Process gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:description>ICAO Annex 3 Meteorological Service for International Air Navigation, Chapter 5 "Aircraft observations and reports"</gml:description></metce:Process></om:procedure><om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/AircraftReport" xlink:title="ICAO Annex 3 Meteorological Service for International Air Navigation, Chapter 5 Aircraft observations and reports" /><om:featureOfInterest><gml:DynamicFeature gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:description>Aircraft observation of meteorological phenomena at a given time and location</gml:description><gml:location><gml:MultiPoint gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:pointMember><gml:Point axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:pos>38.2667 -94.4833</gml:pos></gml:Point></gml:pointMember></gml:MultiPoint></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><iwxxm-us:AircraftMeteorologicalObservationRecord gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:windSpeed uom="[kn_i]">049</iwxxm-us:windSpeed><iwxxm-us:windDirection uom="deg">292</iwxxm-us:windDirection></iwxxm-us:AircraftMeteorologicalObservationRecord></om:result></om:OM_Observation></iwxxm-us:observation><iwxxm-us:aircraftReference>UAL1738</iwxxm-us:aircraftReference><iwxxm-us:flightLevel><iwxxm-us:VerticalLevel gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:verticalLevelReference>STD</iwxxm-us:verticalLevelReference><iwxxm-us:verticalLevel uom="[ft_i]">39000</iwxxm-us:verticalLevel></iwxxm-us:VerticalLevel></iwxxm-us:flightLevel><iwxxm-us:reportType xlink:href="https://codes.nws.noaa.gov/FMH-12/ReportType/ROUTINE" /></iwxxm-us:AircraftReport>
'''  # noqa: E501
