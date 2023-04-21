from app.extractors import SawExtractor
import pytest


class TestSawExtractor:

    @pytest.fixture
    def extractor(self):
        return SawExtractor()

    @pytest.mark.asyncio
    async def test_extract_uswx10(self, extractor):
        assert await extractor.extract(USWX10) == {}


USWX10 = b'''\
<uswx:AviationWatchNotification awnState="New" gml:id="awn-80c576c8-2ab5-46c7-8b9a-9234ec82788a" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 http://nws.weather.gov/schemas/USWX/1.0/AWN/schema/awn.xsd"><uswx:watchNumber>368</uswx:watchNumber><uswx:IssuingOffice gml:id="avn-c6e2034c-09b6-4f6c-839c-772a75d13852"><saf:name>NWS Storm Prediction Center Norman OK</saf:name><saf:type>MWO</saf:type></uswx:IssuingOffice><uswx:WatchInformation gml:id="avn-15cdf027-6014-4639-bf90-9652d878075e"><om:type xlink:href="http://nws.weather.gov/codes/NWSI10-512/2013/Severe Thunderstorm Watch"/><om:phenomenonTime><gml:TimePeriod gml:id="avn-c101bcad-70f2-403e-853c-ca9fc072d2b4"><gml:beginPosition>2020-07-14T02:20:00Z</gml:beginPosition><gml:endPosition>2020-07-14T08:00:00Z</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="avn-d9c3b655-9268-4187-b7e2-a81a72effdb5"><gml:timePosition>2020-07-14T02:16:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:validTime xlink:href="#avn-c101bcad-70f2-403e-853c-ca9fc072d2b4"/><om:procedure xlink:href="http://www.nws.noaa.gov/directives/sym/pd01005012curr.pdf"/><om:observedProperty xlink:href="http://nws.weather.gov/codes/SevereWeatherPhenomena/Severe Thunderstorm"/><om:featureOfInterest><gml:DynamicFeature gml:id="avn-69e2f460-5161-4ec8-8286-a7af77f462f7"><gml:location><gml:Polygon gml:id="avn-80e72969-7012-4114-b5d9-0694e1f803e1"><gml:exterior><gml:LinearRing><gml:posList axisLabels="latitude longitude" count="5" srsDimension="2" srsName="urn:ogc:def:crs:EPSG::4326" uomLabels="deg deg">41.69 -96.99 39.59 -97.84 39.59 -100.10 41.69 -99.32 41.69 -96.99</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon></gml:location></gml:DynamicFeature></om:featureOfInterest><om:result><uswx:WatchThreatParameters><uswx:meanStormDirection uom="deg">270</uswx:meanStormDirection><uswx:meanStormSpeed uom="[kn_i]">35</uswx:meanStormSpeed><uswx:hailSurfaceAndAloft uom="[in_i]">2</uswx:hailSurfaceAndAloft><uswx:windGusts uom="[kn_i]">70</uswx:windGusts><uswx:maxTops uom="[ft_i]">50000</uswx:maxTops></uswx:WatchThreatParameters></om:result></uswx:WatchInformation><uswx:watchDescription>AXIS..60 STATUTE MILES EAST AND WEST OF LINE..45WNW OLU/COLUMBUS NE/ - 75SSW HSI/HASTINGS NE/..AVIATION COORDS.. 50NM E/W /21NNE OBH - 62ENE HLC/</uswx:watchDescription></uswx:AviationWatchNotification>
'''  # noqa: E501
