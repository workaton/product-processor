from app.extractors import PirepExtractor
import pytest


class TestPirepExtractor:

    @pytest.fixture
    def extractor(self):
        return PirepExtractor()

    @pytest.mark.asyncio
    async def test_extract_iwxxmus10(self, extractor):
        assert await extractor.extract(IWXXMUS10) == {}


IWXXMUS10 = b'''\
<iwxxm-us:PilotReport gml:id="uuid.723b0f3e-b7dc-4ef2-afa0-503bb8c602ed" xmlns:aixm="http://www.aixm.aero/schema/5.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:om="http://www.opengis.net/om/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release http://nws.weather.gov/schemas/IWXXM-US/1.0/Release/schemas/pirep.xsd"><iwxxm-us:flightLevelUnknownFlag>true</iwxxm-us:flightLevelUnknownFlag><iwxxm-us:observation><om:OM_Observation gml:id="uuid.a0f7a62c-1a03-4616-922e-6a46e7592362"><om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/PilotReportObservation"/><om:phenomenonTime><gml:TimeInstant gml:id="uuid.e8758963-1275-42ea-a3ac-8c31ab2606e5"><gml:timePosition>2020-07-13T20:37:06Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime xlink:href="#uuid.e8758963-1275-42ea-a3ac-8c31ab2606e5"/><om:procedure><Process gml:id="uuid.969dd994-d765-415e-a349-d799464b1fbe" xmlns="http://def.wmo.int/metce/2013"><gml:description>Federal Meteorological Handbook No.12 United States Meteorological Codes and Coding Practices, Chapter 1</gml:description></Process></om:procedure><om:observedProperty nilReason="unknown"/><om:featureOfInterest><gml:DynamicFeature gml:id="uuid.e8fdf243-e75c-4ebe-a234-5ca0b09fd696"><gml:location><gml:Point axisLabels="latitude longitude" gml:id="uuid.472c39a9-7603-4744-9942-ebd16513391f" srsName="urn:ogc:def:crs:EPSG::4326" uomLabels="degree degree"><gml:pos>60.4918 -145.4776</gml:pos></gml:Point></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><iwxxm-us:AircraftMeteorologicalObservationRecord gml:id="uuid.bfb5a24d-1a2e-4644-8233-71b316244c28"><iwxxm-us:remarks>DURD RY09 (AKFSS</iwxxm-us:remarks><iwxxm-us:turbulence><iwxxm-us:Turbulence gml:id="uuid.a6f02223-aa5c-4ee9-a54c-41fd122a661d"><iwxxm-us:turbRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-11-030/8" xlink:title="Nil"/></iwxxm-us:Turbulence></iwxxm-us:turbulence><iwxxm-us:icing><iwxxm-us:Icing gml:id="uuid.74552675-c783-49ad-b614-7ac6bdce56aa"><iwxxm-us:icingRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-041/0" xlink:title="No icing"/></iwxxm-us:Icing></iwxxm-us:icing></iwxxm-us:AircraftMeteorologicalObservationRecord></om:result></om:OM_Observation></iwxxm-us:observation><iwxxm-us:aircraftReference>B190 </iwxxm-us:aircraftReference><iwxxm-us:phaseOfFlight xlink:href="http://nws.weather.gov/codes/FMH-12/PhaseOfFlight/DESCENDING"/><iwxxm-us:reportType xlink:href="http://nws.weather.gov/codes/FMH-12/ReportType/ROUTINE"/><iwxxm-us:location>CDV </iwxxm-us:location><iwxxm-us:encoderSite>CDV</iwxxm-us:encoderSite></iwxxm-us:PilotReport>
'''  # noqa: E501
