from app.extractors import CwaExtractor
import pytest


class TestCwaExtractor:

    @pytest.fixture
    def extractor(self):
        return CwaExtractor()

    @pytest.mark.asyncio
    async def test_extract_uswx10(self, extractor):
        assert await extractor.extract(USWX10) == {
            'cwsuIdentifier': 'ZMA',
            'sequenceIssuance': '105',
            'phenomenonTime': {
                'start': '2020-09-01T23:22:00Z',
                'end': '2020-09-02T01:22:00Z'
            },
            'resultTime': '2020-09-01T23:22:00Z',
            'observedProperty': 'http://nws.weather.gov/codes/NWSI10-803/2013/BasisForIssuance/Tstm',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[22.429, -68.572], [20.557, -70.185], [20.783, -73.867], [22.191, -74.224], [22.429, -68.572]]
                ]
            },
            'statementText': 'AREA OF TS MOV FM 11015KT. MAX TOPS EST TO FL440. EXP LTL CHG THRU PD. MS'
        }


USWX10 = b'''\
<uswx:CenterWeatherAdvisory
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:om="http://www.opengis.net/om/2.0"
    xmlns:saf="http://icao.int/saf/1.1"
    xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    gml:id="uuid.c34dfc9d-7418-4211-b475-887ed8a223d9"
    status="NORMAL"
    xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 http://nws.weather.gov/schemas/USWX/1.0/CWA/schema/cwa.xsd">
    <!-- Original TAC: 000 FAUS21 KZMA 012322 ZMA1 CWA 012322 ZMA CWA 105 VALID UNTIL 020122 FROM 155ENE GTK-75SE GTK-15SW ZIN-80NNW ZIN-155ENE GTK AREA OF TS MOV FM 11015KT. MAX TOPS EST TO FL440. EXP LTL CHG THRU PD. MS = -->
    <!-- Original TAC: 000 FAUS21 KZMA 012322 ZMA1 CWA 012322 ZMA CWA 105 VALID UNTIL 020122 FROM 155ENE GTK-75SE GTK-15SW ZIN-80NNW ZIN-155ENE GTK AREA OF TS MOV FM 11015KT. MAX TOPS EST TO FL440. EXP LTL CHG THRU PD. MS = -->
    <uswx:centerWeatherServiceUnit gml:id="uuid.7a433770-7b48-4ef8-a585-4d81bec5de01">
        <saf:name>Miami Center Weather Service Unit</saf:name>
        <saf:type>MWO</saf:type>
        <saf:designator>ZMA</saf:designator>
    </uswx:centerWeatherServiceUnit>
    <uswx:sequenceIssuance>105</uswx:sequenceIssuance>
    <uswx:centerWeatherAdvisoryRecord gml:id="uuid.d7f99af1-1a6a-45e5-93f5-17126c0d0c9b">
        <om:phenomenonTime>
            <gml:TimePeriod gml:id="uuid.8f620e2b-6d4b-4841-98c5-1d64b33ccefd">
                <gml:beginPosition>2020-09-01T23:22:00Z</gml:beginPosition>
                <gml:endPosition>2020-09-02T01:22:00Z</gml:endPosition>
            </gml:TimePeriod>
        </om:phenomenonTime>
        <om:resultTime>
            <gml:TimeInstant gml:id="uuid.aa11b76c-2c4a-4b27-8735-9298bed0f75b">
                <gml:timePosition>2020-09-01T23:22:00Z</gml:timePosition>
            </gml:TimeInstant>
        </om:resultTime>
        <om:procedure xlink:href="http://www.nws.noaa.gov/directives/sym/pd01008003curr.pdf"/>
        <om:observedProperty xlink:href="http://nws.weather.gov/codes/NWSI10-803/2013/BasisForIssuance/Tstm"/>
        <om:featureOfInterest>
            <gml:DynamicFeature gml:id="uuid.aca75100-5c26-41d8-ab81-559856fd13d4">
                <gml:location>
                    <gml:Polygon axisLabels="latitude longitude" gml:id="uuid.b0807d89-082a-4f46-9ed4-256e18e11edd" srsDimension="2" srsName="urn:ogc:def:crs:EPSG::4326" uomLabels="deg deg">
                        <gml:exterior>
                            <gml:LinearRing>
                                <gml:posList count="5">22.429 -68.572 20.557 -70.185 20.783 -73.867 22.191 -74.224 22.429 -68.572</gml:posList>
                            </gml:LinearRing>
                        </gml:exterior>
                    </gml:Polygon>
                </gml:location>
            </gml:DynamicFeature>
        </om:featureOfInterest>
        <om:result>
            <uswx:CenterWeatherAdvisoryStatement>
                <uswx:centerWeatherAdvisoryText>AREA OF TS MOV FM 11015KT. MAX TOPS EST TO FL440. EXP LTL CHG THRU PD. MS</uswx:centerWeatherAdvisoryText>
            </uswx:CenterWeatherAdvisoryStatement>
        </om:result>
    </uswx:centerWeatherAdvisoryRecord>
</uswx:CenterWeatherAdvisory>'''  # noqa: E501
