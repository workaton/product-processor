from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, TcaConverter
from app.media_types import MediaTypes
import pendulum
import pytest
from tests.conftest import compare_xml
import time_machine


class TestTcaConverter:

    @pytest.mark.asyncio
    async def test_convert(self):
        converter = TcaConverter()
        with ExitStack() as stack:
            stack.enter_context(time_machine.travel(pendulum.parse('2020-07-23T07:09:21Z')))
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])
        assert len(results) == 1
        xml_tree = etree.fromstring(XML)
        result = results[0]
        assert len(result.data) > 0
        result_tree = etree.fromstring(result.data)
        assert compare_xml(xml_tree, result_tree)


TAC = b'''\
\r\r\n
FKNT23 KNHC 011501\r\r\n
TCANT3\r\r\n
\r\r\n
TROPICAL STORM HELENE ICAO ADVISORY NUMBER  01\r\r\n
NWS NATIONAL HURRICANE CENTER MIAMI FL       AL012018\r\r\n
1501 UTC FRI MAY 01 2018\r\r\n
\r\r\n
TC ADVISORY\r\r\n
DTG:                      20180501/1501Z\r\r\n
TCAC:                     KNHC\r\r\n
TC:                       HELENE\r\r\n
ADVISORY NR:              2018/01\r\r\n
OBS PSN:                  01/1430Z N3254 W03618\r\r\n
CB:                       WI N3332 W03620-N3406 W03641-N34 W035-\r\r\n
                          N3325 W03617-N3332 W03620 TOP BLW FL350\r\r\n
CB:                       WI N3140 W03525-N3061 W03611-N3030 W03449-\r\r\n
                          N3140 W03525 TOP FL350\r\r\n
MOV:                      STNR\r\r\n
INTST CHANGE:             NC\r\r\n
C:                        0988HPA\r\r\n
MAX WIND:                 060KT\r\r\n
FCST PSN +6 HR:           01/2100Z N3438 W03546\r\r\n
FCST MAX WIND +6 HR:      060KT\r\r\n
FCST PSN +12 HR:          02/0300Z N3613 W03458\r\r\n
FCST MAX WIND +12 HR:     060KT\r\r\n
FCST PSN +18 HR:          02/0900Z N3740 W03355\r\r\n
FCST MAX WIND +18 HR:     055KT\r\r\n
FCST PSN +24 HR:          02/1500Z N3858 W03233\r\r\n
FCST MAX WIND +24 HR:     055KT\r\r\n
RMK:                      NIL\r\r\n
NXT MSG:                  20180912/0000Z=\r\r\n
'''  # noqa: E501


XML = b'''\
<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<MeteorologicalBulletin xmlns="http://def.wmo.int/collect/2014" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://def.wmo.int/collect/2014 http://schemas.wmo.int/collect/1.2/collect.xsd" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><meteorologicalInformation><TropicalCycloneAdvisory xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns="http://icao.int/iwxxm/3.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd" permissibleUsage="OPERATIONAL" reportStatus="NORMAL" translationCentreName="NCEP Central Operations" translationCentreDesignator="KWNO" translationTime="2020-07-23T07:09:21Z" translatedBulletinReceptionTime="2020-07-23T07:09:21Z" translatedBulletinID="FKNT23KNHC011501" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><issueTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-01T15:01:00Z</gml:timePosition></gml:TimeInstant></issueTime><issuingTropicalCycloneAdvisoryCentre><aixm:Unit gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><aixm:timeSlice><aixm:UnitTimeSlice gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:validTime /><aixm:interpretation>SNAPSHOT</aixm:interpretation><aixm:type>OTHER:TCAC</aixm:type><aixm:designator>KNHC</aixm:designator></aixm:UnitTimeSlice></aixm:timeSlice></aixm:Unit></issuingTropicalCycloneAdvisoryCentre><tropicalCycloneName><TropicalCyclone xmlns="http://def.wmo.int/metce/2013" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><name>HELENE</name></TropicalCyclone></tropicalCycloneName><advisoryNumber>2018/01</advisoryNumber><observation><TropicalCycloneObservedConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-01T14:30:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><tropicalCyclonePosition><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>32.900 -36.300</gml:pos></gml:Point></tropicalCyclonePosition><cumulonimbusCloudLocation><aixm:AirspaceVolume gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><aixm:upperLimit nilReason="unknown" xsi:nil="true" /><aixm:upperLimitReference>STD</aixm:upperLimitReference><aixm:maximumLimit uom="FL">350</aixm:maximumLimit><aixm:horizontalProjection><aixm:Surface gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:polygonPatches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList count="5">33.533 -36.333 33.417 -36.283 34.000 -35.000 34.100 -36.683 33.533 -36.333</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:polygonPatches></aixm:Surface></aixm:horizontalProjection></aixm:AirspaceVolume></cumulonimbusCloudLocation><cumulonimbusCloudLocation><aixm:AirspaceVolume gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><aixm:upperLimit uom="FL">350</aixm:upperLimit><aixm:upperLimitReference>STD</aixm:upperLimitReference><aixm:lowerLimit uom="FL">350</aixm:lowerLimit><aixm:lowerLimitReference>STD</aixm:lowerLimitReference><aixm:horizontalProjection><aixm:Surface gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:polygonPatches><gml:PolygonPatch><gml:exterior><gml:LinearRing><gml:posList count="4">31.667 -35.417 31.017 -36.183 30.500 -34.817 31.667 -35.417</gml:posList></gml:LinearRing></gml:exterior></gml:PolygonPatch></gml:polygonPatches></aixm:Surface></aixm:horizontalProjection></aixm:AirspaceVolume></cumulonimbusCloudLocation><movement>STATIONARY</movement><centralPressure uom="hPa">988</centralPressure><maximumSurfaceWindSpeed uom="[kn_i]">60</maximumSurfaceWindSpeed></TropicalCycloneObservedConditions></observation><forecast><TropicalCycloneForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-01T21:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><tropicalCyclonePosition><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>34.633 -35.767</gml:pos></gml:Point></tropicalCyclonePosition><maximumSurfaceWindSpeed uom="[kn_i]">60</maximumSurfaceWindSpeed></TropicalCycloneForecastConditions></forecast><forecast><TropicalCycloneForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-02T03:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><tropicalCyclonePosition><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>36.217 -34.967</gml:pos></gml:Point></tropicalCyclonePosition><maximumSurfaceWindSpeed uom="[kn_i]">60</maximumSurfaceWindSpeed></TropicalCycloneForecastConditions></forecast><forecast><TropicalCycloneForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-02T09:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><tropicalCyclonePosition><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>37.667 -33.917</gml:pos></gml:Point></tropicalCyclonePosition><maximumSurfaceWindSpeed uom="[kn_i]">55</maximumSurfaceWindSpeed></TropicalCycloneForecastConditions></forecast><forecast><TropicalCycloneForecastConditions gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-05-02T15:00:00Z</gml:timePosition></gml:TimeInstant></phenomenonTime><tropicalCyclonePosition><gml:Point gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" srsDimension="2"><gml:pos>38.967 -32.550</gml:pos></gml:Point></tropicalCyclonePosition><maximumSurfaceWindSpeed uom="[kn_i]">55</maximumSurfaceWindSpeed></TropicalCycloneForecastConditions></forecast><remarks nilReason="http://codes.wmo.int/common/nil/inapplicable" /><nextAdvisoryTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2018-09-12T00:00:00Z</gml:timePosition></gml:TimeInstant></nextAdvisoryTime></TropicalCycloneAdvisory></meteorologicalInformation><bulletinIdentifier>A_LKNT23KNHC011501_C_KNHC_20200723070921.xml</bulletinIdentifier></MeteorologicalBulletin>
'''  # noqa: E501
