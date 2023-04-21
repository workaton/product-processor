from app.extractors import MisExtractor
import pytest


class TestMisExtractor:

    @pytest.fixture
    def extractor(self):
        return MisExtractor()

    @pytest.mark.asyncio
    async def test_extract_uswx10(self, extractor):
        assert await extractor.extract(USWX10) == {}


USWX10 = b'''\
<uswx:MeteorologicalImpactStatement gml:id="uuid.0fdd53c2-1995-4ed6-9539-bf9a0b7c1859" status="NORMAL" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 http://nws.weather.gov/schemas/USWX/1.0/MIS/schema/mis.xsd"><uswx:centerWeatherServiceUnit gml:id="uuid.786d71dc-8555-49f7-8d8c-1743faf829f3"><saf:name>New York City Center Weather Service Unit</saf:name><saf:type>MWO</saf:type><saf:designator>ZNY</saf:designator></uswx:centerWeatherServiceUnit><uswx:sequenceIssuance>01</uswx:sequenceIssuance><uswx:meteorologicalImpactStatementRecord gml:id="uuid.33ed6b39-d148-4588-9250-62b470b650b7"><om:phenomenonTime><gml:TimePeriod gml:id="uuid.6b03add1-c53e-47a1-833c-7e690fa3a790"><gml:beginPosition>2020-07-13T18:15:00</gml:beginPosition><gml:endPosition>2020-07-14T02:30:00</gml:endPosition></gml:TimePeriod></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="uuid.84fce651-3f70-474b-8b97-ba01083efc01"><gml:timePosition>2020-07-13T18:07:00</gml:timePosition></gml:TimeInstant></om:resultTime><om:procedure xlink:href="http://www.nws.noaa.gov/directives/sym/pd01008003curr.pdf"/><om:observedProperty xlink:href="http://nws.weather.gov/schemas/USWX/observedProperties/MeteorologicalImpactStatement"/><om:featureOfInterest xlink:href="http://nws.weather.gov/schemas/USWX/geodata/artcc/ZNY.xml"/><om:result><uswx:MeteorologicalImpactStatementText><uswx:misText>THE CWSU AT ZNY WILL BE COVERED REMOTELY BTW 18300230Z AND CAN BE
REACHED VIA EMAIL ZNY.OPERATIONSNOAA.GOV. NORMAL ONSITE COVERAGE
RESUMES AT 1030Z TUESDAY.</uswx:misText></uswx:MeteorologicalImpactStatementText></om:result></uswx:meteorologicalImpactStatementRecord></uswx:MeteorologicalImpactStatement>
'''  # noqa: E501
