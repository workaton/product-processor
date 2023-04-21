from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, CwaConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestCwaConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = CwaConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-08-05T15:25:00Z')))
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
FAUS21 KZOB 132158\r\r\n
ZOB1 CWA 132158\r\r\n
ZOB CWA 102 VALID UNTIL 132300\r\r\n
FROM 25W SYR-30SW SYR-45SW SYR-15S BUF-5NNW BUF-25W SYR\r\r\n
AREA TS WITH MOD/HVY RAIN MOV FROM 29025KT. TOPS TO FL380.\r\r\n
TREND...MINIMAL CHG.\r\r\n
=\r\r\n
\r\r\n
'''  # noqa: E501

XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><uswx:CenterWeatherAdvisory xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:saf="http://icao.int/saf/1.1" xmlns:om="http://www.opengis.net/om/2.0" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/cwa.xsd" status="NORMAL" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:centerWeatherServiceUnit gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><saf:name>Cleveland Center Weather Service Unit</saf:name><saf:type>MWO</saf:type><saf:designator>ZOB</saf:designator></uswx:centerWeatherServiceUnit><uswx:sequenceIssuance>102</uswx:sequenceIssuance><uswx:centerWeatherAdvisoryRecord gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:phenomenonTime><gml:TimePeriod gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition>2020-07-13T21:58:00Z</gml:beginPosition><gml:endPosition>2020-07-13T23:00:00Z</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-08-05T15:25:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01008003curr.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-803/BasisForIssuance/Tstm" /><om:featureOfInterest><gml:DynamicFeature gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326"><gml:exterior><gml:LinearRing><gml:posList count="5">42.695 -76.106 42.758 -76.590 42.581 -76.832 42.940 -79.072 42.909 -78.626</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:CenterWeatherAdvisoryStatement><uswx:centerWeatherAdvisoryText>25W SYR\r\r  AREA TS WITH MOD/HVY RAIN MOV FROM 29025KT. TOPS TO FL380.\r\r  TREND...MINIMAL CHG.</uswx:centerWeatherAdvisoryText></uswx:CenterWeatherAdvisoryStatement></om:result></uswx:centerWeatherAdvisoryRecord></uswx:CenterWeatherAdvisory>
'''  # noqa: E501
