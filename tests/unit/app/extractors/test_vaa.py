from app.extractors import VolcanicAshExtractor
import pytest


class TestVolcanicAshExtractor:

    @pytest.fixture
    def extractor(self):
        return VolcanicAshExtractor()

    @pytest.mark.asyncio
    async def test_extract_iwxxm20(self, extractor):
        assert await extractor.extract(IWXXM_20) == {}

    @pytest.mark.asyncio
    @pytest.mark.skip('needs an actual product to test')
    async def test_extract_iwxxm30(self, extractor):
        assert await extractor.extract(IWXXM_30) == {}


IWXXM_20 = b'''\
<uswx:ConvectiveGuidanceForecast automated="false" gml:id="tcf-46d4089b-d0df-4d5f-be1d-95c0dcfe9fca" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 http://nws.weather.gov/schemas/USWX/1.0/CWFG/schema/cwfg.xsd"><uswx:issuingMetWatchOffice gml:id="tcf-0f4d5765-190d-42ef-b2c5-3c50d394393c"><saf:name>Aviation Weather Center, Kansas City MO</saf:name><saf:type>MWO</saf:type><saf:designator>AWC</saf:designator></uswx:issuingMetWatchOffice><uswx:convectiveGuidanceForecast gml:id="tcf-1fe6616c-72e9-4103-8774-fad6d7a47bda"><om:type xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MesoscaleConvectiveSystemForecastTypes/TCF"/><om:phenomenonTime><gml:TimeInstant gml:id="tcf-ac469f97-de2a-4227-823c-5628a8dbbd64"><gml:timePosition>2020-07-14T05:00:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="tcf-0f272c62-3273-41d5-8d9c-5f8b47cc34b4"><gml:timePosition>2020-07-13T21:00:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:procedure xlink:href="http://aviationweather.gov/tcf/help"/><om:observedProperty xlink:href="http://aviationweather.gov/tcf/help" xlink:title="Traffic Flow Management (TFM) Convective Forecast (TCF) Help"/><om:featureOfInterest><gml:FeatureCollection gml:id="tcf-bfe81ae3-7919-4e02-a18e-ecc378d22d8d"><gml:boundedBy><gml:Envelope axisLabels="latitude longitude" srsDimension="2" srsName="urn:ogc:def:EPSG::4326" uomLabels="degree degree"><gml:lowerCorner>24.23 -123.42</gml:lowerCorner><gml:upperCorner>49.0 -67.01</gml:upperCorner></gml:Envelope></gml:boundedBy></gml:FeatureCollection></om:featureOfInterest><om:result><uswx:ConvectiveGuidanceForecastRecord numberOfConvectiveFeatures="5"><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MaximumConvectionTopHeights/FL350-FL390"/><uswx:coverageWithInPolygon xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ConvectionCoverages/Sparse"/><uswx:forecastConfidence xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ForecastGuidanceConfidences/High"/><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:pos>34.2 -75.7</gml:pos><gml:pos>34.6 -75.8</gml:pos><gml:pos>34.9 -75.8</gml:pos><gml:pos>35.6 -74.0</gml:pos><gml:pos>36.0 -73.3</gml:pos><gml:pos>36.4 -72.6</gml:pos><gml:pos>35.0 -72.6</gml:pos><gml:pos>35.0 -72.6</gml:pos><gml:pos>34.6 -73.4</gml:pos><gml:pos>34.0 -74.4</gml:pos><gml:pos>34.1 -75.5</gml:pos><gml:pos>34.2 -75.7</gml:pos><gml:pos>34.2 -75.7</gml:pos></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MaximumConvectionTopHeights/FL300-FL340"/><uswx:coverageWithInPolygon xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ConvectionCoverages/Sparse"/><uswx:forecastConfidence xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ForecastGuidanceConfidences/High"/><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:pos>45.5 -100.3</gml:pos><gml:pos>45.3 -102.0</gml:pos><gml:pos>44.8 -103.3</gml:pos><gml:pos>45.1 -104.3</gml:pos><gml:pos>45.6 -103.4</gml:pos><gml:pos>46.0 -101.9</gml:pos><gml:pos>46.2 -100.0</gml:pos><gml:pos>45.9 -99.8</gml:pos><gml:pos>45.5 -100.3</gml:pos></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MaximumConvectionTopHeights/FL350-FL390"/><uswx:coverageWithInPolygon xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ConvectionCoverages/Sparse"/><uswx:forecastConfidence xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ForecastGuidanceConfidences/High"/><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:pos>38.1 -99.3</gml:pos><gml:pos>37.3 -99.5</gml:pos><gml:pos>36.8 -99.6</gml:pos><gml:pos>36.4 -99.8</gml:pos><gml:pos>36.0 -100.2</gml:pos><gml:pos>36.1 -100.6</gml:pos><gml:pos>36.5 -100.7</gml:pos><gml:pos>37.0 -100.8</gml:pos><gml:pos>37.5 -100.7</gml:pos><gml:pos>38.3 -100.5</gml:pos><gml:pos>38.5 -100.1</gml:pos><gml:pos>38.5 -99.6</gml:pos><gml:pos>38.5 -99.4</gml:pos><gml:pos>38.1 -99.3</gml:pos></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MaximumConvectionTopHeights/FL400"/><uswx:coverageWithInPolygon xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ConvectionCoverages/Medium"/><uswx:forecastConfidence xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ForecastGuidanceConfidences/High"/><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:pos>46.3 -93.4</gml:pos><gml:pos>46.9 -92.5</gml:pos><gml:pos>46.7 -91.9</gml:pos><gml:pos>46.2 -92.0</gml:pos><gml:pos>45.3 -92.8</gml:pos><gml:pos>44.7 -94.1</gml:pos><gml:pos>44.4 -94.9</gml:pos><gml:pos>44.2 -95.6</gml:pos><gml:pos>44.6 -95.8</gml:pos><gml:pos>45.1 -94.9</gml:pos><gml:pos>45.7 -94.2</gml:pos><gml:pos>46.3 -93.4</gml:pos></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/MaximumConvectionTopHeights/FL350-FL390"/><uswx:coverageWithInPolygon xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ConvectionCoverages/Sparse"/><uswx:forecastConfidence xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/ForecastGuidanceConfidences/High"/><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:pos>40.7 -99.7</gml:pos><gml:pos>41.6 -99.3</gml:pos><gml:pos>42.4 -99.3</gml:pos><gml:pos>43.1 -100.0</gml:pos><gml:pos>43.6 -99.9</gml:pos><gml:pos>43.6 -99.1</gml:pos><gml:pos>43.3 -98.5</gml:pos><gml:pos>43.2 -97.8</gml:pos><gml:pos>43.3 -97.0</gml:pos><gml:pos>43.1 -96.6</gml:pos><gml:pos>42.6 -97.4</gml:pos><gml:pos>42.1 -97.8</gml:pos><gml:pos>41.2 -97.9</gml:pos><gml:pos>40.6 -98.2</gml:pos><gml:pos>40.2 -98.7</gml:pos><gml:pos>40.2 -99.4</gml:pos><gml:pos>40.7 -99.7</gml:pos></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures></uswx:ConvectiveGuidanceForecastRecord></om:result></uswx:convectiveGuidanceForecast></uswx:ConvectiveGuidanceForecast>
'''  # noqa: E501


IWXXM_30 = b'''\
'''  # noqa: E501