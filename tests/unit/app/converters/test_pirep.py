from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, PirepConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestPirepConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = PirepConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-08-13T20:37:00Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])

        assert len(results) > 0
        for index, result in enumerate(results):
            assert len(result.data) > 0
            xml_tree = etree.fromstring(XML_MULTI[index])
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)


TAC = b'''\
\r\r\n
000\r\r\n
UBUS31 KWBC 132045\r\r\n
PRCUS\r\r\n
LYH UA /OV MOL050030/TM 2039/FL375/TP B738/TB LGT-MOD=\r\r\n
CDV UA /OV CDV /TM 2037 /FLUNKN /TP B190 /TB NEG /IC NEG /RM DURD\r\r\n
    RY09 (AKFSS=\r\r\n
\r\r\n
'''  # noqa: E501

XML_MULTI = [
    b'''<?xml version="1.0" encoding="UTF-8"?><iwxxm-us:PilotReport xmlns:aixm="http://www.aixm.aero/schema/5.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:om="http://www.opengis.net/om/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release https://nws.weather.gov/schemas/iwxxm-us/1.0/pirep.xsd" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:flightLevelUnknownFlag>false</iwxxm-us:flightLevelUnknownFlag><iwxxm-us:observation><om:OM_Observation gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/PilotReportObservation" /><om:phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-13T20:39:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#uuid.a36a2138-2c09-473e-bd0d-916531537b02" /><om:procedure><Process xmlns="http://def.wmo.int/metce/2013" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:description>Federal Meteorological Handbook No.12 United States Meteorological Codes and Coding Practices, Chapter 1</gml:description></Process></om:procedure><om:observedProperty nilReason="unknown" /><om:featureOfInterest><gml:DynamicFeature gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>38.283 -78.700</gml:pos></gml:Point></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><iwxxm-us:AircraftMeteorologicalObservationRecord gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:turbulence><iwxxm-us:Turbulence gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:turbRangeEnd xlink:href="http://codes.wmo.int/bufr4/codeflag/0-11-030/10" /><iwxxm-us:turbRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-11-030/9" /></iwxxm-us:Turbulence></iwxxm-us:turbulence></iwxxm-us:AircraftMeteorologicalObservationRecord></om:result></om:OM_Observation></iwxxm-us:observation><iwxxm-us:aircraftReference>B738</iwxxm-us:aircraftReference><iwxxm-us:flightLevel><iwxxm-us:VerticalLevel gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:verticalLevelReference>STD</iwxxm-us:verticalLevelReference><iwxxm-us:verticalLevel uom="FL">37500</iwxxm-us:verticalLevel></iwxxm-us:VerticalLevel></iwxxm-us:flightLevel><iwxxm-us:reportType xlink:href="https://codes.nws.noaa.gov/FMH-12/ReportType/ROUTINE" /><iwxxm-us:location>MOL050030</iwxxm-us:location><iwxxm-us:encoderSite>LYH</iwxxm-us:encoderSite></iwxxm-us:PilotReport>''',  # noqa: E501
    b'''<?xml version="1.0" encoding="UTF-8"?><iwxxm-us:PilotReport xmlns:aixm="http://www.aixm.aero/schema/5.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:om="http://www.opengis.net/om/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release https://nws.weather.gov/schemas/iwxxm-us/1.0/pirep.xsd" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:flightLevelUnknownFlag>true</iwxxm-us:flightLevelUnknownFlag><iwxxm-us:observation><om:OM_Observation gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/PilotReportObservation" /><om:phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-13T20:37:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#uuid.a36a2138-2c09-473e-bd0d-916531537b02" /><om:procedure><Process xmlns="http://def.wmo.int/metce/2013" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:description>Federal Meteorological Handbook No.12 United States Meteorological Codes and Coding Practices, Chapter 1</gml:description></Process></om:procedure><om:observedProperty nilReason="unknown" /><om:featureOfInterest><gml:DynamicFeature gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>60.4918 -145.4776</gml:pos></gml:Point></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><iwxxm-us:AircraftMeteorologicalObservationRecord gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:remarks>DURD RY09 (AKFSS</iwxxm-us:remarks><iwxxm-us:turbulence><iwxxm-us:Turbulence gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:turbRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-11-030/8" /></iwxxm-us:Turbulence></iwxxm-us:turbulence><iwxxm-us:icing><iwxxm-us:Icing gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><iwxxm-us:icingRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-041/0" /></iwxxm-us:Icing></iwxxm-us:icing></iwxxm-us:AircraftMeteorologicalObservationRecord></om:result></om:OM_Observation></iwxxm-us:observation><iwxxm-us:aircraftReference>B190 </iwxxm-us:aircraftReference><iwxxm-us:phaseOfFlight xlink:href="https://codes.nws.noaa.gov/FMH-12/PhaseOfFlight/DESCENDING" /><iwxxm-us:reportType xlink:href="https://codes.nws.noaa.gov/FMH-12/ReportType/ROUTINE" /><iwxxm-us:location>CDV </iwxxm-us:location><iwxxm-us:encoderSite>CDV</iwxxm-us:encoderSite></iwxxm-us:PilotReport>'''  # noqa: E501
]
