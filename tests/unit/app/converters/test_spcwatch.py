from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, SpcWatchConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestSpcWatchConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = SpcWatchConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-07-27T14:32:37Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            result = await converter.convert([
                ConversionInput(TAC_SAW, MediaTypes.TEXT_PLAIN, id='SAW'),
                ConversionInput(TAC_SEL, MediaTypes.TEXT_PLAIN, id='SEL')
            ])

        assert len(result) == 2
        for product in result:
            if product.id == 'SAW':
                saw_xml_tree = etree.fromstring(XML_SAW)
                saw_result_tree = etree.fromstring(product.data)
                assert compare_xml(saw_xml_tree, saw_result_tree)
            elif product.id == 'SEL':
                sel_xml_tree = etree.fromstring(XML_SEL)
                sel_result_tree = etree.fromstring(product.data)
                assert compare_xml(sel_xml_tree, sel_result_tree)
            else:
                pytest.fail('Converter should only return SAW and SEL products')


TAC_SAW = b'''\
\r\r\n
000\r\r\n
WWUS30 KWNS 140216\r\r\n
SAW8\r\r\n
SPC AWW 140216\r\r\n
WW 368 SEVERE TSTM KS NE 140220Z - 140800Z\r\r\n
AXIS..60 STATUTE MILES EAST AND WEST OF LINE..\r\r\n
45WNW OLU/COLUMBUS NE/ - 75SSW HSI/HASTINGS NE/\r\r\n
..AVIATION COORDS.. 50NM E/W /21NNE OBH - 62ENE HLC/\r\r\n
HAIL SURFACE AND ALOFT..2 INCHES. WIND GUSTS..70 KNOTS.\r\r\n
MAX TOPS TO 500. MEAN STORM MOTION VECTOR 27035.\r\r\n
\r\r\n
LAT...LON 41699699 39599784 39590010 41699932\r\r\n
\r\r\n
THIS IS AN APPROXIMATION TO THE WATCH AREA.  FOR A\r\r\n
COMPLETE DEPICTION OF THE WATCH SEE WOUS64 KWNS\r\r\n
FOR WOU8.\r\r\n
\r\r\n
'''  # noqa: E501


TAC_SEL = b'''\
\r\r\n
000\r\r\n
WWUS20 KWNS 140216\r\r\n
SEL8\r\r\n
SPC WW 140216\r\r\n
KSZ000-NEZ000-140800-\r\r\n
\r\r\n
URGENT - IMMEDIATE BROADCAST REQUESTED\r\r\n
Severe Thunderstorm Watch Number 368\r\r\n
NWS Storm Prediction Center Norman OK\r\r\n
920 PM CDT Mon Jul 13 2020\r\r\n
\r\r\n
The NWS Storm Prediction Center has issued a\r\r\n
\r\r\n
* Severe Thunderstorm Watch for portions of\r\r\n
  North Central Kansas\r\r\n
  Central Nebraska\r\r\n
\r\r\n
* Effective this Monday night and Tuesday morning from 920 PM\r\r\n
  until 300 AM CDT.\r\r\n
\r\r\n
* Primary threats include...\r\r\n
  Widespread damaging winds and isolated significant gusts to 80\r\r\n
    mph likely\r\r\n
  Scattered large hail and isolated very large hail events to 2\r\r\n
    inches in diameter possible\r\r\n
\r\r\n
SUMMARY...A fast-moving bow echo over southwest Nebraska is expected\r\r\n
to track across the watch area during the next few hours, posing a\r\r\n
risk of damaging winds and some hail.\r\r\n
\r\r\n
The severe thunderstorm watch area is approximately along and 60\r\r\n
statute miles east and west of a line from 45 miles west northwest\r\r\n
of Columbus NE to 75 miles south southwest of Hastings NE. For a\r\r\n
complete depiction of the watch see the associated watch outline\r\r\n
update (WOUS64 KWNS WOU8).\r\r\n
\r\r\n
PRECAUTIONARY/PREPAREDNESS ACTIONS...\r\r\n
\r\r\n
REMEMBER...A Severe Thunderstorm Watch means conditions are\r\r\n
favorable for severe thunderstorms in and close to the watch area.\r\r\n
Persons in these areas should be on the lookout for threatening\r\r\n
weather conditions and listen for later statements and possible\r\r\n
warnings. Severe thunderstorms can and occasionally do produce\r\r\n
tornadoes.\r\r\n
\r\r\n
&&\r\r\n
\r\r\n
OTHER WATCH INFORMATION...CONTINUE...WW 366...WW 367...\r\r\n
\r\r\n
AVIATION...A few severe thunderstorms with hail surface and aloft to\r\r\n
2 inches. Extreme turbulence and surface wind gusts to 70 knots. A\r\r\n
few cumulonimbi with maximum tops to 500. Mean storm motion vector\r\r\n
27035.\r\r\n
\r\r\n
...Hart\r\r\n
\r\r\n
'''  # noqa: E501

XML_SAW = b'''\
<?xml version="1.0" encoding="UTF-8"?><uswx:AviationWatchNotification xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/awn.xsd" awnState="New" gml:id="awn-a36a2138-2c09-473e-bd0d-916531537b02"><uswx:watchNumber>368</uswx:watchNumber><uswx:IssuingOffice gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><saf:name>NWS Storm Prediction Center Norman OK</saf:name><saf:type>MWO</saf:type></uswx:IssuingOffice><uswx:WatchInformation gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-512/Severe Thunderstorm Watch" /><om:phenomenonTime><gml:TimePeriod gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition>2020-07-14T02:20:00Z</gml:beginPosition><gml:endPosition>2020-07-14T08:00:00Z</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T02:16:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:validTime xlink:href="#avn-a36a2138-2c09-473e-bd0d-916531537b02" /><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01005012curr.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-512/SevereWeatherPhenomena/Severe Thunderstorm" /><om:featureOfInterest><gml:DynamicFeature gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon gml:id="avn-a36a2138-2c09-473e-bd0d-916531537b02"><gml:exterior><gml:LinearRing><gml:posList srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2" count="5">41.69 -96.99 39.59 -97.84 39.59 -100.10 41.69 -99.32 41.69 -96.99</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:WatchThreatParameters><uswx:meanStormDirection uom="deg">270</uswx:meanStormDirection><uswx:meanStormSpeed uom="[kn_i]">35</uswx:meanStormSpeed><uswx:hailSurfaceAndAloft uom="[in_i]">2</uswx:hailSurfaceAndAloft><uswx:windGusts uom="[kn_i]">70</uswx:windGusts><uswx:maxTops uom="[ft_i]">50000</uswx:maxTops></uswx:WatchThreatParameters></om:result></uswx:WatchInformation><uswx:watchDescription>\r\r\n\nAXIS..60 STATUTE MILES EAST AND WEST OF LINE..\r\r\n\n45WNW OLU/COLUMBUS NE/ - 75SSW HSI/HASTINGS NE/\r\r\n\n..AVIATION COORDS.. 50NM E/W /21NNE OBH - 62ENE HLC/\r\r\n\n</uswx:watchDescription></uswx:AviationWatchNotification>
'''  # noqa: E501

XML_SEL = b'''\
<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<uswx:PublicWatchNotification xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/spcPublicWatch.xsd" watchNumber="368" publicWatchNotificationState="New" isBackupCenter="false" isParticularlyDangerousSituation="false" isCorrection="false" gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><uswx:issuingCenter>NWS Storm Prediction Center Norman OK</uswx:issuingCenter><uswx:awnID>awn-a36a2138-2c09-473e-bd0d-916531537b02</uswx:awnID><uswx:publicWatchMessage gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-512/Severe Thunderstorm Watch" /><om:phenomenonTime><gml:TimePeriod gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><gml:beginPosition>2020-07-14T02:20:00Z</gml:beginPosition><gml:endPosition>2020-07-14T08:00:00Z</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T02:16:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:validTime xlink:href="#sel-a36a2138-2c09-473e-bd0d-916531537b02" /><om:procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01005012cur.pdf" /><om:observedProperty xlink:href="https://codes.nws.noaa.gov/NWSI-10-512/SevereWeatherPhenomena/Severe Thunderstorm" /><om:featureOfInterest><gml:DynamicFeature gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><gml:location><gml:Polygon srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2" gml:id="sel-a36a2138-2c09-473e-bd0d-916531537b02"><gml:exterior><gml:LinearRing><gml:posList count="5">41.69 -96.99 39.59 -97.84 39.59 -100.10 41.69 -99.32 41.69 -96.99</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:WatchText><uswx:aviationThreat>A few severe thunderstorms with hail surface and aloft to 2 inches. Extreme turbulence and surface wind gusts to 70 knots. A few cumulonimbi with maximum tops to 500. Mean storm motion vector 27035.</uswx:aviationThreat><uswx:callToAction>PRECAUTIONARY/PREPAREDNESS ACTIONS... REMEMBER...A Severe Thunderstorm Watch means conditions are favorable for severe thunderstorms in and close to the watch area. Persons in these areas should be on the lookout for threatening weather conditions and listen for later statements and possible warnings. Severe thunderstorms can and occasionally do produce tornadoes.</uswx:callToAction><uswx:threatText>The NWS Storm Prediction Center has issued a\n* Severe Thunderstorm Watch for portions of\nNorth Central Kansas\nCentral Nebraska\n* Effective this Monday night and Tuesday morning from 920 PM\nuntil 300 AM CDT.\n* Primary threats include...\nWidespread damaging winds and isolated significant gusts to 80\nmph likely\nScattered large hail and isolated very large hail events to 2\ninches in diameter possible\nSUMMARY...A fast-moving bow echo over southwest Nebraska is expected\nto track across the watch area during the next few hours, posing a\nrisk of damaging winds and some hail.\nThe severe thunderstorm watch area is approximately along and 60\nstatute miles east and west of a line from 45 miles west northwest\nof Columbus NE to 75 miles south southwest of Hastings NE. For a\ncomplete depiction of the watch see the associated watch outline\nupdate (WOUS64 KWNS WOU8).\nOTHER WATCH INFORMATION...CONTINUE...WW 366...WW 367...\r\r\n\n\r\r\n\n</uswx:threatText></uswx:WatchText></om:result></uswx:publicWatchMessage><uswx:forecasterID>Hart</uswx:forecasterID></uswx:PublicWatchNotification>
'''  # noqa: E501
