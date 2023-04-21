from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, VolcanicAshConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestVolcanicAshConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = VolcanicAshConverter()
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
FVXX20 KNES 140253\r\r\n
VAAAK1\r\r\n
VA ADVISORY\r\r\n
DTG: 20200714/0253Z\r\r\n
\r\r\n
VAAC: WASHINGTON\r\r\n
\r\r\n
VOLCANO: POPOCATEPETL 341090\r\r\n
PSN: N1901 W09837\r\r\n
\r\r\n
AREA: MEXICO\r\r\n
\r\r\n
SUMMIT ELEV: 17802 FT (5426 M)\r\r\n
\r\r\n
ADVISORY NR: 2020/683\r\r\n
\r\r\n
INFO SOURCE: GOES-EAST. NWP MODELS. VOLCAT.\r\r\n
RADIOSONDE.\r\r\n
\r\r\n
ERUPTION DETAILS: CONTG VA EMS.\r\r\n
\r\r\n
OBS VA DTG: 14/0246Z\r\r\n
\r\r\n
OBS VA CLD: SFC/FL190 N1917 W09838 - N1901 W09837\r\r\n
- N1901 W09839 - N1915 W09850 - N1917 W09838 MOV\r\r\n
NW 10-15KT\r\r\n
\r\r\n
FCST VA CLD +6HR: 14/0900Z SFC/FL190 N1923 W09841\r\r\n
- N1902 W09837 - N1901 W09838 - N1918 W09855 -\r\r\n
N1923 W09841\r\r\n
\r\r\n
FCST VA CLD +12HR: 14/1500Z NO VA EXP\r\r\n
\r\r\n
FCST VA CLD +18HR: 14/2100Z NO VA EXP\r\r\n
\r\r\n
RMK: VA OBS IN SAT UP TO 15 NM NNW OF SUMMIT.\r\r\n
MULTIPLE VOLCAT ALERTS FOR VA SINCE PREV\r\r\n
ADVISORY. WX CLDS IN AREA MAY OBSC PORTIONS OF VA\r\r\n
CLD. FL WINDS EXP TO PERSIST THRU T+6. ...CLARK\r\r\n
\r\r\n
NXT ADVISORY: WILL BE ISSUED BY 20200714/0900Z\r\r\n
\r\r\n
'''  # noqa: E501


XML = b'''\
<?xml version="1.0" encoding="UTF-8"?><VolcanicAshAdvisory xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns="http://icao.int/iwxxm/3.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd" permissibleUsage="OPERATIONAL" reportStatus="NORMAL" translationCentreName="NCEP Central Operations" translationCentreDesignator="KWNO" translationTime="2020-07-27T14:32:37Z" translatedBulletinReceptionTime="2020-07-27T14:32:37Z" translatedBulletinID="FVXX20KNES140253" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><issueTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T02:53:00Z</gml:timePosition></gml:TimeInstant></issueTime><issuingVolcanicAshAdvisoryCentre><Unit gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" xmlns="http://www.aixm.aero/schema/5.1.1"><timeSlice><UnitTimeSlice gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:validTime /><interpretation>SNAPSHOT</interpretation><name>WASHINGTON</name><type>OTHER:VAAC</type></UnitTimeSlice></timeSlice></Unit></issuingVolcanicAshAdvisoryCentre><volcano><EruptingVolcano xmlns="http://def.wmo.int/metce/2013" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><name>POPOCATEPETL 341090</name><position><gml:Point axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:pos>19.017 -98.617</gml:pos></gml:Point></position><eruptionDate>2020-07-14T02:53:00Z</eruptionDate></EruptingVolcano></volcano><stateOrRegion>MEXICO</stateOrRegion><summitElevation uom="[ft_i]">17802</summitElevation><advisoryNumber>2020/683</advisoryNumber><informationSource>GOES-EAST. NWP MODELS. VOLCAT. RADIOSONDE.</informationSource><eruptionDetails>CONTG VA EMS.</eruptionDetails><observation><VolcanicAshObservedOrEstimatedConditions status="IDENTIFIABLE" isEstimated="false" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T02:46:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><ashCloud><VolcanicAshCloudObservedOrEstimated gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><ashCloudExtent><aixm:AirspaceVolume gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><aixm:upperLimit uom="FL">190</aixm:upperLimit><aixm:upperLimitReference>STD</aixm:upperLimitReference><aixm:lowerLimit>GND</aixm:lowerLimit><aixm:lowerLimitReference>SFC</aixm:lowerLimitReference><aixm:horizontalProjection><aixm:Surface gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:patches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList count="5">19.283 -98.633 19.250 -98.834 19.017 -98.650 19.017 -98.617 19.283 -98.633</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:patches></aixm:Surface></aixm:horizontalProjection></aixm:AirspaceVolume></ashCloudExtent><directionOfMotion uom="deg">315</directionOfMotion><speedOfMotion uom="[kn_i]">10</speedOfMotion></VolcanicAshCloudObservedOrEstimated></ashCloud></VolcanicAshObservedOrEstimatedConditions></observation><forecast><VolcanicAshForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" status="PROVIDED"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T09:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><ashCloud><VolcanicAshCloudForecast gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><ashCloudExtent><aixm:AirspaceVolume gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><aixm:upperLimit uom="FL">190</aixm:upperLimit><aixm:upperLimitReference>STD</aixm:upperLimitReference><aixm:lowerLimit>GND</aixm:lowerLimit><aixm:lowerLimitReference>SFC</aixm:lowerLimitReference><aixm:horizontalProjection><aixm:Surface gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:patches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList count="5">19.383 -98.683 19.300 -98.917 19.017 -98.633 19.033 -98.617 19.383 -98.683</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:patches></aixm:Surface></aixm:horizontalProjection></aixm:AirspaceVolume></ashCloudExtent></VolcanicAshCloudForecast></ashCloud></VolcanicAshForecastConditions></forecast><forecast><VolcanicAshForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" status="NO_VOLCANIC_ASH_EXPECTED"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T15:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime></VolcanicAshForecastConditions></forecast><forecast><VolcanicAshForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" status="NO_VOLCANIC_ASH_EXPECTED"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T21:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime></VolcanicAshForecastConditions></forecast><remarks>VA OBS IN SAT UP TO 15 NM NNW OF SUMMIT. MULTIPLE VOLCAT ALERTS FOR VA SINCE PREV ADVISORY. WX CLDS IN AREA MAY OBSC PORTIONS OF VA CLD. FL WINDS EXP TO PERSIST THRU T+6. ...CLARK</remarks><nextAdvisoryTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition indeterminatePosition="before">2020-07-14T09:00:00Z</gml:timePosition></gml:TimeInstant></nextAdvisoryTime></VolcanicAshAdvisory>
'''  # noqa: E501
