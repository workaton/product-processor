from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, SwbConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestSwbConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = SwbConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-08-13T17:00:00Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])

        xml_tree = etree.fromstring(XML)
        for result in results:
            assert len(result.data) > 0
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)

    @pytest.mark.asyncio
    async def test_convert_multiple_events(self):
        converter = SwbConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-08-13T17:00:00Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC_MULTI, MediaTypes.TEXT_PLAIN)])

        assert len(results) > 0
        i = 0
        for result in results:
            assert len(result.data) > 0
            xml_tree = etree.fromstring(XML_MULTI[i])
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)
            i = + 1


TAC = b'''\
\r\r\n
000\r\r\n
WUUS54 KOUN 130944\r\r\n
SVROUN\r\r\n
OKC011-043-131030-\r\r\n
/O.NEW.KOUN.SV.W.0569.200713T0944Z-200713T1030Z/\r\r\n
\r\r\n
BULLETIN - IMMEDIATE BROADCAST REQUESTED\r\r\n
Severe Thunderstorm Warning\r\r\n
National Weather Service Norman OK\r\r\n
444 AM CDT Mon Jul 13 2020\r\r\n
\r\r\n
The National Weather Service in Norman has issued a\r\r\n
\r\r\n
* Severe Thunderstorm Warning for...\r\r\n
  Central Blaine County in northwestern Oklahoma...\r\r\n
  Southeastern Dewey County in northwestern Oklahoma...\r\r\n
\r\r\n
* Until 530 AM CDT.\r\r\n
\r\r\n
* At 443 AM CDT, a severe thunderstorm was located near Eagle City,\r\r\n
  moving east at 40 mph.\r\r\n
\r\r\n
  HAZARD...70 mph wind gusts and nickel size hail.\r\r\n
\r\r\n
  SOURCE...Radar indicated.\r\r\n
\r\r\n
  IMPACT...Expect considerable tree damage. Damage is likely to \r\r\n
           mobile homes, roofs, and outbuildings.\r\r\n
\r\r\n
* Locations impacted include...\r\r\n
  Watonga, Hitchcock, Oakwood, Eagle City and Fay. \r\r\n
\r\r\n
PRECAUTIONARY/PREPAREDNESS ACTIONS...\r\r\n
\r\r\n
For your protection move to an interior room on the lowest floor of a\r\r\n
building.\r\r\n
\r\r\n
&&\r\r\n
\r\r\n
LAT...LON 3603 9821 3576 9821 3581 9859 3581 9866\r\r\n
      3582 9875 3602 9872\r\r\n
TIME...MOT...LOC 0943Z 275DEG 35KT 3592 9865 \r\r\n
\r\r\n
HAIL...0.88IN\r\r\n
WIND...70MPH\r\r\n
\r\r\n
$$\r\r\n
\r\r\n
WR\r\r\n
\r\r\n
'''  # noqa: E501

TAC_MULTI = b'''\
\r\r\n
619\r\r\n
WWUS53 KABR 111323\r\r\n
SVSABR\r\r\n
\r\r\n
Severe Weather Statement\r\r\n
National Weather Service Aberdeen SD\r\r\n
823 AM CDT Tue Aug 11 2020\r\r\n
\r\r\n
SDC041-111333-\r\r\n
/O.CAN.KABR.SV.W.0211.000000T0000Z-200811T1330Z/\r\r\n
Dewey SD-\r\r\n
823 AM CDT Tue Aug 11 2020\r\r\n
\r\r\n
...THE SEVERE THUNDERSTORM WARNING FOR NORTHEASTERN DEWEY COUNTY IS
CANCELLED...\r\r\n
\r\r\n
The severe thunderstorm which prompted the warning has moved out of\r\r\n
the warned area. Therefore, the warning has been cancelled.\r\r\n
\r\r\n
LAT...LON 4537 9990 4534 10029 4539 10028 4540 10029\r\r\n
      4542 10030 4543 10032 4544 10032 4555 10001\r\r\n
TIME...MOT...LOC 1323Z 257DEG 22KT 4541 10014\r\r\n
\r\r\n
$$\r\r\n
\r\r\n
SDC129-111330-\r\r\n
/O.CON.KABR.SV.W.0211.000000T0000Z-200811T1330Z/\r\r\n
Walworth SD-\r\r\n
823 AM CDT Tue Aug 11 2020\r\r\n
\r\r\n
...A SEVERE THUNDERSTORM WARNING REMAINS IN EFFECT UNTIL 830 AM CDT\r\r\n
FOR CENTRAL WALWORTH COUNTY...\r\r\n
\r\r\n
At 823 AM CDT, a severe thunderstorm was located near Akaska, or 8\r\r\n
miles southwest of Selby, moving east at 25 mph.\r\r\n
\r\r\n
HAZARD...60 mph wind gusts and quarter size hail.\r\r\n
\r\r\n
SOURCE...Radar indicated.\r\r\n
\r\r\n
IMPACT...Hail damage to vehicles is expected. Expect wind damage to\r\r\n
         roofs, siding, and trees.\r\r\n
\r\r\n
Locations impacted include...\r\r\n
Selby and New Everets Resort.\r\r\n
\r\r\n
PRECAUTIONARY/PREPAREDNESS ACTIONS...\r\r\n
\r\r\n
For your protection move to an interior room on the lowest floor of a\r\r\n
building.\r\r\n
\r\r\n
&&\r\r\n
\r\r\n
LAT...LON 4537 9990 4534 10029 4539 10028 4540 10029\r\r\n
      4542 10030 4543 10032 4544 10032 4555 10001\r\r\n
TIME...MOT...LOC 1323Z 257DEG 22KT 4541 10014\r\r\n
\r\r\n
HAIL...1.00IN\r\r\n
WIND...60MPH\r\r\n
\r\r\n
$$\r\r\n
'''  # noqa: E501


XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><uswx:SvrWxrBulletin xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/svrWxrBulletin.xsd" eventTrackingNumber="0569" productType="Operational" lifeCycleState="New" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:issuingWFO><uswx:officeName>Norman OK</uswx:officeName><uswx:officeIdentifier>OUN</uswx:officeIdentifier></uswx:issuingWFO><uswx:svrWxrInformation gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/Severe Thunderstorm Warning" /><om:phenomenonTime><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-13T09:44:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#SV.a36a2138-2c09-473e-bd0d-916531537b02" /><om:validTime><gml:TimePeriod gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition>2020-07-13T09:44:00Z</gml:beginPosition><gml:endPosition>2020-07-13T10:30:00Z</gml:endPosition></gml:TimePeriod></om:validTime><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01005011cur.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/SevereWeatherPhenomena/Severe Thunderstorm" /><om:featureOfInterest><gml:DynamicFeature gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:exterior><gml:LinearRing><gml:posList count="7">36.03 -98.21 35.76 -98.21 35.81 -98.59 35.81 -98.66 35.82 -98.75 36.02 -98.72 36.03 -98.21</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:SvrWxrTextAndMotion><uswx:rationale>The National Weather Service in Norman has issued a * Severe Thunderstorm Warning for... Central Blaine County in northwestern Oklahoma... Southeastern Dewey County in northwestern Oklahoma... * Until 530 AM CDT. * At 443 AM CDT, a severe thunderstorm was located near Eagle City, moving east at 40 mph. HAZARD...70 mph wind gusts and nickel size hail. SOURCE...Radar indicated. IMPACT...Expect considerable tree damage. Damage is likely to  mobile homes, roofs, and outbuildings. * Locations impacted include... Watonga, Hitchcock, Oakwood, Eagle City and Fay. </uswx:rationale><uswx:callToAction>PRECAUTIONARY/PREPAREDNESS ACTIONS... For your protection move to an interior room on the lowest floor of a building.</uswx:callToAction><uswx:timeOfPosition><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-13T09:43:00Z</gml:timePosition></gml:TimeInstant></uswx:timeOfPosition><uswx:warnedPointFeatureMotion><uswx:position gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2"><gml:pos>35.92 -98.65</gml:pos></uswx:position><uswx:direction uom="deg">275</uswx:direction><uswx:speed uom="[kn_i]">35</uswx:speed></uswx:warnedPointFeatureMotion></uswx:SvrWxrTextAndMotion></om:result></uswx:svrWxrInformation><uswx:forecasterID>WR</uswx:forecasterID></uswx:SvrWxrBulletin>
'''  # noqa: E501


XML_MULTI = [
    b'''<?xml version="1.0" encoding="UTF-8"?><uswx:SvrWxrBulletin xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/svrWxrBulletin.xsd" eventTrackingNumber="0211" productType="Operational" lifeCycleState="Cancelled" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:issuingWFO><uswx:officeName>Aberdeen SD</uswx:officeName><uswx:officeIdentifier>ABR</uswx:officeIdentifier></uswx:issuingWFO><uswx:svrWxrInformation gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/Severe Thunderstorm Warning" /><om:phenomenonTime><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition indeterminatePosition="now" /></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#SV.a36a2138-2c09-473e-bd0d-916531537b02" /><om:validTime><gml:TimePeriod gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition indeterminatePosition="now" /><gml:endPosition>2020-08-11T13:30:00Z</gml:endPosition></gml:TimePeriod></om:validTime><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01005011cur.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/SevereWeatherPhenomena/Severe Thunderstorm" /><om:featureOfInterest><gml:DynamicFeature gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:exterior><gml:LinearRing><gml:posList count="9">45.37 -99.90 45.34 -100.29 45.39 -100.28 45.40 -100.29 45.42 -100.30 45.43 -100.32 45.44 -100.32 45.55 -100.01 45.37 -99.90</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:SvrWxrTextAndMotion><uswx:rationale>...THE SEVERE THUNDERSTORM WARNING FOR NORTHEASTERN DEWEY COUNTY IS CANCELLED... The severe thunderstorm which prompted the warning has moved out of the warned area. Therefore, the warning has been cancelled.</uswx:rationale><uswx:callToAction>NONE.</uswx:callToAction><uswx:timeOfPosition><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-11T13:23:00Z</gml:timePosition></gml:TimeInstant></uswx:timeOfPosition><uswx:warnedPointFeatureMotion><uswx:position gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2"><gml:pos>45.41 -100.14</gml:pos></uswx:position><uswx:direction uom="deg">257</uswx:direction><uswx:speed uom="[kn_i]">22</uswx:speed></uswx:warnedPointFeatureMotion></uswx:SvrWxrTextAndMotion></om:result></uswx:svrWxrInformation></uswx:SvrWxrBulletin>''',  # noqa: E501
    b'''<?xml version="1.0" encoding="UTF-8"?><uswx:SvrWxrBulletin xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/svrWxrBulletin.xsd" eventTrackingNumber="0211" productType="Operational" lifeCycleState="Continuation" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:issuingWFO><uswx:officeName>Aberdeen SD</uswx:officeName><uswx:officeIdentifier>ABR</uswx:officeIdentifier></uswx:issuingWFO><uswx:svrWxrInformation gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/Severe Thunderstorm Warning" /><om:phenomenonTime><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition indeterminatePosition="now" /></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#SV.a36a2138-2c09-473e-bd0d-916531537b02" /><om:validTime><gml:TimePeriod gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition indeterminatePosition="now" /><gml:endPosition>2020-08-11T13:30:00Z</gml:endPosition></gml:TimePeriod></om:validTime><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01005011cur.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-511/SevereWeatherPhenomena/Severe Thunderstorm" /><om:featureOfInterest><gml:DynamicFeature gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2" gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:exterior><gml:LinearRing><gml:posList count="9">45.37 -99.90 45.34 -100.29 45.39 -100.28 45.40 -100.29 45.42 -100.30 45.43 -100.32 45.44 -100.32 45.55 -100.01 45.37 -99.90</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:SvrWxrTextAndMotion><uswx:rationale>...A SEVERE THUNDERSTORM WARNING REMAINS IN EFFECT UNTIL 830 AM CDT FOR CENTRAL WALWORTH COUNTY... At 823 AM CDT, a severe thunderstorm was located near Akaska, or 8 miles southwest of Selby, moving east at 25 mph. HAZARD...60 mph wind gusts and quarter size hail. SOURCE...Radar indicated. IMPACT...Hail damage to vehicles is expected. Expect wind damage to roofs, siding, and trees. Locations impacted include... Selby and New Everets Resort.</uswx:rationale><uswx:callToAction>PRECAUTIONARY/PREPAREDNESS ACTIONS... For your protection move to an interior room on the lowest floor of a building.</uswx:callToAction><uswx:timeOfPosition><gml:TimeInstant gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-11T13:23:00Z</gml:timePosition></gml:TimeInstant></uswx:timeOfPosition><uswx:warnedPointFeatureMotion><uswx:position gml:id="SV.a36a2138-2c09-473e-bd0d-916531537b02" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2"><gml:pos>45.41 -100.14</gml:pos></uswx:position><uswx:direction uom="deg">257</uswx:direction><uswx:speed uom="[kn_i]">22</uswx:speed></uswx:warnedPointFeatureMotion></uswx:SvrWxrTextAndMotion></om:result></uswx:svrWxrInformation></uswx:SvrWxrBulletin>'''  # noqa: E501
]
