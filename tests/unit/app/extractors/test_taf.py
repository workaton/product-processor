from app.extractors import TafCollectiveExtractor, TafExtractor
import pytest


class TestTafExtractor:

    @pytest.fixture
    def extractor(self):
        return TafExtractor()

    @pytest.mark.asyncio
    async def test_extract_iwxxm11(self, extractor):
        assert await extractor.extract(IWXXM11) == {
            'issueTime': '2020-07-12T06:00:00Z',
            'locationIdentifier': 'RKSI',
            'geometry': {
                'type': 'Point',
                'coordinates': [37.4667, 126.45]
            },
            'validPeriod': {
                'start': '2020-07-12T06:00:00Z',
                'end': '2020-07-13T12:00:00Z'
            }
        }

    @pytest.mark.asyncio
    async def test_extract_iwxxm30(self, extractor):
        assert await extractor.extract(IWXXM30) == {
            'issueTime': '2020-06-15T17:29:00Z',
            'locationIdentifier': 'KSBN',
            'geometry': {
                'type': 'Point',
                'coordinates': [41.71, -86.32]
            },
            'validPeriod': {
                'start': '2020-06-15T18:00:00Z',
                'end': '2020-06-16T18:00:00Z'
            }
        }

    @pytest.mark.asyncio
    async def test_extract_iwxxmus10(self, extractor):
        assert await extractor.extract(IWXXMUS10) == {
            'issueTime': '2020-07-13T21:20:00Z',
            'locationIdentifier': 'KHOU',
            'geometry': {
                'type': 'Point',
                'coordinates': [29.6375, -95.2825]
            },
            'validPeriod': {
                'start': '2020-07-13T21:00:00Z',
                'end': '2020-07-14T18:00:00Z'
            }
        }


class TestTafCollectiveExtractor:

    @pytest.fixture
    def extractor(self):
        return TafCollectiveExtractor()

    @pytest.mark.asyncio
    async def test_extract_iwxxm30(self, extractor):
        assert await extractor.extract(COLLECTIVE_IWXXM30) == {
            'count': 2,
            'extracted': [
                {
                    'issueTime': '2020-06-15T17:29:00Z',
                    'locationIdentifier': 'KSBN',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [41.71, -86.32]
                    },
                    'validPeriod': {
                        'start': '2020-06-15T18:00:00Z',
                        'end': '2020-06-16T18:00:00Z'
                    }
                },
                {
                    'issueTime': '2020-06-15T17:29:00Z',
                    'locationIdentifier': 'KFWA',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [41.01, -85.2]
                    },
                    'validPeriod': {
                        'start': '2020-06-15T18:00:00Z',
                        'end': '2020-06-16T18:00:00Z'
                    }
                }
            ]
        }


IWXXM11 = b'''\
<iwxxm:TAF gml:id="TAF-RKSI-202007120600Z" status="AMENDMENT" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/1.1"
           xmlns:metce="http://def.wmo.int/metce/2013" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1"
           xmlns:sams="http://www.opengis.net/samplingSpatial/2.0" xmlns:sf="http://www.opengis.net/sampling/2.0" xmlns:xlink="http://www.w3.org/1999/xlink"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/1.1 http://schemas.wmo.int/iwxxm/1.1/taf.xsd">
  <iwxxm:issueTime>
    <gml:TimeInstant gml:id="ti-RKSI-202007120600Z">
      <gml:timePosition>2020-07-12T06:00:00Z</gml:timePosition>
    </gml:TimeInstant>
  </iwxxm:issueTime>
  <iwxxm:validTime>
    <gml:TimePeriod gml:id="Entire-timePeriod-RKSI-202007120600Z-202007131200Z">
      <gml:beginPosition>2020-07-12T06:00:00Z</gml:beginPosition>
      <gml:endPosition>2020-07-13T12:00:00Z</gml:endPosition>
    </gml:TimePeriod>
  </iwxxm:validTime>
  <iwxxm:baseForecast>
    <om:OM_Observation gml:id="RKSI-base-forecast">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeBaseForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="Base-timePeriod-RKSI-202007120600Z-202007120700Z">
          <gml:beginPosition>2020-07-12T06:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-12T07:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure>
        <metce:Process gml:id="p-49-2-taf">
          <gml:description>WMO No. 49 Volume 2 Meteorological Service for International Air Navigation APPENDIX 5 TECHNICAL SPECIFICATIONS RELATED TO FORECASTS</gml:description>
        </metce:Process>
      </om:procedure>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest>
        <sams:SF_SpatialSamplingFeature gml:id="samplePt-RKSI">
          <sf:type xlink:href="http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"/>
          <sf:sampledFeature>
            <saf:Aerodrome gml:id="uuid.0">
              <gml:identifier codeSpace="urn:uuid:"/>
              <saf:designator>RKSI</saf:designator>
              <saf:name>CHAJANG NI</saf:name>
              <saf:locationIndicatorICAO>RKSI</saf:locationIndicatorICAO>
              <saf:ARP>
                <gml:Point axisLabels="Lat Lon Altitude" gml:id="reference-Pt-RKSI" srsName="urn:ogc:def:crs:EPSG::4979" uomLabels="deg deg m">
                  <gml:pos>37.4666666667 126.45 22.9656</gml:pos>
                </gml:Point>
              </saf:ARP>
            </saf:Aerodrome>
          </sf:sampledFeature>
          <sams:shape>
            <gml:Point axisLabels="Lat Lon Altitude" gml:id="observed-Pt-RKSI" srsName="urn:ogc:crs:EPSG::4979" uomLabels="deg deg m">
              <gml:pos>37.4666666667 126.45 22.9656</gml:pos>
            </gml:Point>
          </sams:shape>
        </sams:SF_SpatialSamplingFeature>
      </om:featureOfInterest>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord cloudAndVisibilityOK="false" gml:id="RKSI-mafr-0">
          <iwxxm:prevailingVisibility uom="m">7000.0</iwxxm:prevailingVisibility>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">130</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">3.1</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:weather xlink:href="http://codes.wmo.int/306/4678/-RA" xlink:title="Light precipitation of rain"/>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="RKSI-acf-1">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/3" xlink:title="Broken"/>
                  <iwxxm:base uom="ft">3000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/4" xlink:title="Overcast"/>
                  <iwxxm:base uom="ft">10000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
          <iwxxm:temperature>
            <iwxxm:AerodromeAirTemperatureForecast>
              <iwxxm:maximumAirTemperature uom="Cel">24</iwxxm:maximumAirTemperature>
              <iwxxm:maximumAirTemperatureTime>
                <gml:TimeInstant gml:id="TX-RKSI-202007130700Z">
                  <gml:timePosition>2020-07-13T07:00:00Z</gml:timePosition>
                </gml:TimeInstant>
              </iwxxm:maximumAirTemperatureTime>
              <iwxxm:minimumAirTemperature uom="Cel">19</iwxxm:minimumAirTemperature>
              <iwxxm:minimumAirTemperatureTime>
                <gml:TimeInstant gml:id="TN-RKSI-202007122100Z">
                  <gml:timePosition>2020-07-12T21:00:00Z</gml:timePosition>
                </gml:TimeInstant>
              </iwxxm:minimumAirTemperatureTime>
            </iwxxm:AerodromeAirTemperatureForecast>
          </iwxxm:temperature>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:baseForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="RKSI-chg-1">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="BECMG-timePeriod-RKSI-202007120700Z-202007121500Z">
          <gml:beginPosition>2020-07-12T07:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-12T15:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure xlink:href="#p-49-2-taf"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-RKSI"/>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord changeIndicator="BECOMING" cloudAndVisibilityOK="false" gml:id="RKSI-cf-1">
          <iwxxm:prevailingVisibility uom="m">4000.0</iwxxm:prevailingVisibility>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">160</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">5.1</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="RKSI-acf-2">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2" xlink:title="Scattered"/>
                  <iwxxm:base uom="ft">1000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/3" xlink:title="Broken"/>
                  <iwxxm:base uom="ft">2500</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/4" xlink:title="Overcast"/>
                  <iwxxm:base uom="ft">8000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="RKSI-chg-2">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="BECMG-timePeriod-RKSI-202007121500Z-202007121900Z">
          <gml:beginPosition>2020-07-12T15:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-12T19:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure xlink:href="#p-49-2-taf"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-RKSI"/>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord changeIndicator="BECOMING" cloudAndVisibilityOK="false" gml:id="RKSI-cf-2">
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">130</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">7.7</iwxxm:meanWindSpeed>
              <iwxxm:windGustSpeed uom="m/s">12.9</iwxxm:windGustSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="RKSI-chg-3">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="BECMG-timePeriod-RKSI-202007121900Z-202007130200Z">
          <gml:beginPosition>2020-07-12T19:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-13T02:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure xlink:href="#p-49-2-taf"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-RKSI"/>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord changeIndicator="BECOMING" cloudAndVisibilityOK="false" gml:id="RKSI-cf-3">
          <iwxxm:prevailingVisibility uom="m">2500.0</iwxxm:prevailingVisibility>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">100</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">10.3</iwxxm:meanWindSpeed>
              <iwxxm:windGustSpeed uom="m/s">18.0</iwxxm:windGustSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:weather xlink:href="http://codes.wmo.int/306/4678/RA" xlink:title="Precipitation of rain"/>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="RKSI-acf-3">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/3" xlink:title="Broken"/>
                  <iwxxm:base uom="ft">1000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/3" xlink:title="Broken"/>
                  <iwxxm:base uom="ft">2500</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/4" xlink:title="Overcast"/>
                  <iwxxm:base uom="ft">7000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="RKSI-chg-4">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="BECMG-timePeriod-RKSI-202007130200Z-202007130800Z">
          <gml:beginPosition>2020-07-13T02:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-13T08:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure xlink:href="#p-49-2-taf"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-RKSI"/>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord changeIndicator="BECOMING" cloudAndVisibilityOK="false" gml:id="RKSI-cf-4">
          <iwxxm:prevailingVisibility uom="m">4000.0</iwxxm:prevailingVisibility>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">130</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">10.3</iwxxm:meanWindSpeed>
              <iwxxm:windGustSpeed uom="m/s">18.0</iwxxm:windGustSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:weather xlink:href="http://codes.wmo.int/306/4678/-RA" xlink:title="Light precipitation of rain"/>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="RKSI-acf-4">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2" xlink:title="Scattered"/>
                  <iwxxm:base uom="ft">1000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/3" xlink:title="Broken"/>
                  <iwxxm:base uom="ft">2500</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/4" xlink:title="Overcast"/>
                  <iwxxm:base uom="ft">8000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="RKSI-chg-5">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="BECMG-timePeriod-RKSI-202007130800Z-202007131200Z">
          <gml:beginPosition>2020-07-13T08:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-13T12:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-RKSI-202007120600Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-RKSI-202007120600Z-202007131200Z"/>
      <om:procedure xlink:href="#p-49-2-taf"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-RKSI"/>
      <om:result>
        <iwxxm:MeteorologicalAerodromeForecastRecord changeIndicator="BECOMING" cloudAndVisibilityOK="false" gml:id="RKSI-cf-5">
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">130</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">7.7</iwxxm:meanWindSpeed>
              <iwxxm:windGustSpeed uom="m/s">12.9</iwxxm:windGustSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
        </iwxxm:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
</iwxxm:TAF>
'''  # noqa: E501


IWXXM30 = b'''\
<MeteorologicalBulletin gml:id="uuid.f80d5b79-2821-4352-9d0b-1bdf3b9fcf49" xmlns="http://def.wmo.int/collect/2014" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://def.wmo.int/collect/2014 http://schemas.wmo.int/collect/1.2/collect.xsd"><meteorologicalInformation><TAF gml:id="uuid.430664ac-435a-4a15-8119-61fd45ea43ba" permissibleUsage="OPERATIONAL" reportStatus="NORMAL" xmlns="http://icao.int/iwxxm/3.0" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/3.0 https://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd"><issueTime><gml:TimeInstant gml:id="uuid.fd5b765c-0e03-44af-a020-6a822f0acc6a"><gml:timePosition>2020-06-15T17:29:00Z</gml:timePosition></gml:TimeInstant></issueTime><aerodrome><aixm:AirportHeliport gml:id="uuid.6ccc4302-fded-49a8-85b1-7fd22cb1eb36"><aixm:timeSlice><aixm:AirportHeliportTimeSlice gml:id="uuid.378f76e2-ca0d-4962-a39a-ccf8f247d819"><gml:validTime/><aixm:interpretation>SNAPSHOT</aixm:interpretation><aixm:locationIndicatorICAO>KSBN</aixm:locationIndicatorICAO><aixm:ARP><aixm:ElevatedPoint axisLabels="Lat Long" gml:id="uuid.3423aa30-fcfe-478c-b0da-b132d3df616b" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326"><gml:pos>41.71 -86.32</gml:pos></aixm:ElevatedPoint></aixm:ARP></aixm:AirportHeliportTimeSlice></aixm:timeSlice></aixm:AirportHeliport></aerodrome><validPeriod><gml:TimePeriod gml:id="uuid.b5bb3991-c7dc-43e8-aa11-1849bb41145f"><gml:beginPosition>2020-06-15T18:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></validPeriod><baseForecast><MeteorologicalAerodromeForecast cloudAndVisibilityOK="false" gml:id="uuid.6b1ab8a2-b948-444b-9eda-d0c77ea20c51"><phenomenonTime><gml:TimePeriod gml:id="uuid.8a08c161-6f5a-4217-ba3c-d77494bdab63"><gml:beginPosition>2020-06-15T17:29:00Z</gml:beginPosition><gml:endPosition>2020-06-16T05:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">60</meanWindDirection><meanWindSpeed uom="[kn_i]">8</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.e88296e6-c4f4-41a6-a448-c725d4aad748"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/0"/><base nilReason="http://codes.wmo.int/common/nill/inapplicable" uom="N/A" xsi:nil="true"/></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></baseForecast><changeForecast><MeteorologicalAerodromeForecast changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="uuid.5e95a607-3e61-4e39-96b4-7e95674597be"><phenomenonTime><gml:TimePeriod gml:id="uuid.a4ab7504-4ffa-4b69-9d87-3c60cb690614"><gml:beginPosition>2020-06-16T05:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T14:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">100</meanWindDirection><meanWindSpeed uom="[kn_i]">3</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.dd4c456f-daa0-4fd4-82c2-a84d2764c560"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1"/><base uom="[ft_i]">5000</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></changeForecast><changeForecast><MeteorologicalAerodromeForecast changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="uuid.96e4900a-6618-4e0a-9fb5-4cb72c7f01ed"><phenomenonTime><gml:TimePeriod gml:id="uuid.88705462-4b5a-45d5-8184-1c68897ed186"><gml:beginPosition>2020-06-16T14:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">150</meanWindDirection><meanWindSpeed uom="[kn_i]">4</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.219d3e54-ad87-485c-8ccc-488622e38281"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1"/><base uom="[ft_i]">4000</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></changeForecast><extension><USMetadata xmlns="http://www.weather.gov/iwxxm-us/3.0" xsi:schemaLocation="http://www.weather.gov/iwxxm-us/3.0 https://nws.weather.gov/schemas/iwxxm-us/3.0/taf.xsd"><procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01008013curr.pdf" xlink:title="NWS Instruction 10-813, Aviation Weather Services, Terminal Aerodrome Forecasts"/></USMetadata></extension></TAF></meteorologicalInformation><bulletinIdentifier>A_LTUS43KIWX151700_C_KIWX_202015172936.xml</bulletinIdentifier></MeteorologicalBulletin>
'''  # noqa: E501


IWXXMUS10 = b'''\
<iwxxm-us:TAF gml:id="TAF-KHOU-202007132120Z" status="AMENDMENT" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/1.1" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:metce="http://def.wmo.int/metce/2013" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:sams="http://www.opengis.net/samplingSpatial/2.0" xmlns:sf="http://www.opengis.net/sampling/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release http://nws.weather.gov/schemas/IWXXM-US/1.0/Release/schemas/usTaf.xsd">
  <iwxxm:issueTime>
    <gml:TimeInstant gml:id="ti-KHOU-202007132120Z">
      <gml:timePosition>2020-07-13T21:20:00Z</gml:timePosition>
    </gml:TimeInstant>
  </iwxxm:issueTime>
  <iwxxm:validTime>
    <gml:TimePeriod gml:id="Entire-timePeriod-KHOU-202007132100Z-202007141800Z">
      <gml:beginPosition>2020-07-13T21:00:00Z</gml:beginPosition>
      <gml:endPosition>2020-07-14T18:00:00Z</gml:endPosition>
    </gml:TimePeriod>
  </iwxxm:validTime>
  <iwxxm:baseForecast>
    <om:OM_Observation gml:id="KHOU-base-forecast">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeBaseForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="Base-timePeriod-KHOU-202007132100Z-202007140100Z">
          <gml:beginPosition>2020-07-13T21:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-14T01:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-KHOU-202007132120Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-KHOU-202007132100Z-202007141800Z"/>
      <om:procedure>
        <metce:Process gml:id="process-NWSI10-813">
          <gml:description>United States National Weather Service Instruction 10-813 Terminal Aerodrome Forecasts</gml:description>
        </metce:Process>
      </om:procedure>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest>
        <sams:SF_SpatialSamplingFeature gml:id="samplePt-KHOU">
          <sf:type xlink:href="http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"/>
          <sf:sampledFeature>
            <saf:Aerodrome gml:id="uuid.0">
              <gml:identifier codeSpace="urn:uuid:"/>
              <saf:designator>KHOU</saf:designator>
              <saf:name>Houston, Houston Hobby Airport</saf:name>
              <saf:locationIndicatorICAO>KHOU</saf:locationIndicatorICAO>
              <saf:ARP>
                <gml:Point axisLabels="Lat Lon Altitude" gml:id="reference-Pt-KHOU" srsName="urn:ogc:def:crs:EPSG::4979" uomLabels="deg deg m">
                  <gml:pos>29.6375 -95.2825 46</gml:pos>
                </gml:Point>
              </saf:ARP>
            </saf:Aerodrome>
          </sf:sampledFeature>
          <sams:shape>
            <gml:Point axisLabels="Lat Lon Altitude" gml:id="observed-Pt-KHOU" srsName="urn:ogc:crs:EPSG::4979" uomLabels="deg deg m">
              <gml:pos>29.6375 -95.2825 46</gml:pos>
            </gml:Point>
          </sams:shape>
        </sams:SF_SpatialSamplingFeature>
      </om:featureOfInterest>
      <om:result>
        <iwxxm-us:MeteorologicalAerodromeForecastRecord cloudAndVisibilityOK="false" gml:id="KHOU-mafr-0">
          <iwxxm:prevailingVisibility uom="m">11265.4</iwxxm:prevailingVisibility>
          <iwxxm:prevailingVisibilityOperator>ABOVE</iwxxm:prevailingVisibilityOperator>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">180</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">4.1</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="KHOU-acf-1">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1" xlink:title="Few"/>
                  <iwxxm:base uom="ft">5000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm-us:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:baseForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="KHOU-chg-1">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="FM-timePeriod-KHOU-202007140100Z-202007141000Z">
          <gml:beginPosition>2020-07-14T01:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-14T10:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-KHOU-202007132120Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-KHOU-202007132100Z-202007141800Z"/>
      <om:procedure xlink:href="#process-NWSI10-813"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-KHOU"/>
      <om:result>
        <iwxxm-us:MeteorologicalAerodromeForecastRecord changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="KHOU-cf-1">
          <iwxxm:prevailingVisibility uom="m">11265.4</iwxxm:prevailingVisibility>
          <iwxxm:prevailingVisibilityOperator>ABOVE</iwxxm:prevailingVisibilityOperator>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">200</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">3.6</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="KHOU-acf-2">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2" xlink:title="Scattered"/>
                  <iwxxm:base uom="ft">25000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm-us:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="KHOU-chg-2">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="FM-timePeriod-KHOU-202007141000Z-202007141600Z">
          <gml:beginPosition>2020-07-14T10:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-14T16:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-KHOU-202007132120Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-KHOU-202007132100Z-202007141800Z"/>
      <om:procedure xlink:href="#process-NWSI10-813"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-KHOU"/>
      <om:result>
        <iwxxm-us:MeteorologicalAerodromeForecastRecord changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="KHOU-cf-2">
          <iwxxm:prevailingVisibility uom="m">11265.4</iwxxm:prevailingVisibility>
          <iwxxm:prevailingVisibilityOperator>ABOVE</iwxxm:prevailingVisibilityOperator>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="true">
              <iwxxm:meanWindSpeed uom="m/s">2.1</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="KHOU-acf-3">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2" xlink:title="Scattered"/>
                  <iwxxm:base uom="ft">2500</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm-us:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
  <iwxxm:changeForecast>
    <om:OM_Observation gml:id="KHOU-chg-3">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/MeteorologicalAerodromeForecast"/>
      <om:phenomenonTime>
        <gml:TimePeriod gml:id="FM-timePeriod-KHOU-202007141600Z-202007141800Z">
          <gml:beginPosition>2020-07-14T16:00:00Z</gml:beginPosition>
          <gml:endPosition>2020-07-14T18:00:00Z</gml:endPosition>
        </gml:TimePeriod>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#ti-KHOU-202007132120Z"/>
      <om:validTime xlink:href="#Entire-timePeriod-KHOU-202007132100Z-202007141800Z"/>
      <om:procedure xlink:href="#process-NWSI10-813"/>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/MeteorologicalAerodromeForecast"/>
      <om:featureOfInterest xlink:href="#samplePt-KHOU"/>
      <om:result>
        <iwxxm-us:MeteorologicalAerodromeForecastRecord changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="KHOU-cf-3">
          <iwxxm:prevailingVisibility uom="m">11265.4</iwxxm:prevailingVisibility>
          <iwxxm:prevailingVisibilityOperator>ABOVE</iwxxm:prevailingVisibilityOperator>
          <iwxxm:surfaceWind>
            <iwxxm:AerodromeSurfaceWindForecast variableWindDirection="false">
              <iwxxm:meanWindDirection uom="deg">210</iwxxm:meanWindDirection>
              <iwxxm:meanWindSpeed uom="m/s">3.6</iwxxm:meanWindSpeed>
            </iwxxm:AerodromeSurfaceWindForecast>
          </iwxxm:surfaceWind>
          <iwxxm:cloud>
            <iwxxm:AerodromeCloudForecast gml:id="KHOU-acf-4">
              <iwxxm:layer>
                <iwxxm:CloudLayer>
                  <iwxxm:amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2" xlink:title="Scattered"/>
                  <iwxxm:base uom="ft">18000</iwxxm:base>
                </iwxxm:CloudLayer>
              </iwxxm:layer>
            </iwxxm:AerodromeCloudForecast>
          </iwxxm:cloud>
        </iwxxm-us:MeteorologicalAerodromeForecastRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm:changeForecast>
</iwxxm-us:TAF>
'''  # noqa: E501


COLLECTIVE_IWXXM30 = b'''\
<MeteorologicalBulletin gml:id="uuid.f80d5b79-2821-4352-9d0b-1bdf3b9fcf49" xmlns="http://def.wmo.int/collect/2014" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://def.wmo.int/collect/2014 http://schemas.wmo.int/collect/1.2/collect.xsd"><meteorologicalInformation><TAF gml:id="uuid.430664ac-435a-4a15-8119-61fd45ea43ba" permissibleUsage="OPERATIONAL" reportStatus="NORMAL" xmlns="http://icao.int/iwxxm/3.0" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/3.0 https://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd"><issueTime><gml:TimeInstant gml:id="uuid.fd5b765c-0e03-44af-a020-6a822f0acc6a"><gml:timePosition>2020-06-15T17:29:00Z</gml:timePosition></gml:TimeInstant></issueTime><aerodrome><aixm:AirportHeliport gml:id="uuid.6ccc4302-fded-49a8-85b1-7fd22cb1eb36"><aixm:timeSlice><aixm:AirportHeliportTimeSlice gml:id="uuid.378f76e2-ca0d-4962-a39a-ccf8f247d819"><gml:validTime/><aixm:interpretation>SNAPSHOT</aixm:interpretation><aixm:locationIndicatorICAO>KSBN</aixm:locationIndicatorICAO><aixm:ARP><aixm:ElevatedPoint axisLabels="Lat Long" gml:id="uuid.3423aa30-fcfe-478c-b0da-b132d3df616b" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326"><gml:pos>41.71 -86.32</gml:pos></aixm:ElevatedPoint></aixm:ARP></aixm:AirportHeliportTimeSlice></aixm:timeSlice></aixm:AirportHeliport></aerodrome><validPeriod><gml:TimePeriod gml:id="uuid.b5bb3991-c7dc-43e8-aa11-1849bb41145f"><gml:beginPosition>2020-06-15T18:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></validPeriod><baseForecast><MeteorologicalAerodromeForecast cloudAndVisibilityOK="false" gml:id="uuid.6b1ab8a2-b948-444b-9eda-d0c77ea20c51"><phenomenonTime><gml:TimePeriod gml:id="uuid.8a08c161-6f5a-4217-ba3c-d77494bdab63"><gml:beginPosition>2020-06-15T17:29:00Z</gml:beginPosition><gml:endPosition>2020-06-16T05:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">60</meanWindDirection><meanWindSpeed uom="[kn_i]">8</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.e88296e6-c4f4-41a6-a448-c725d4aad748"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/0"/><base nilReason="http://codes.wmo.int/common/nill/inapplicable" uom="N/A" xsi:nil="true"/></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></baseForecast><changeForecast><MeteorologicalAerodromeForecast changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="uuid.5e95a607-3e61-4e39-96b4-7e95674597be"><phenomenonTime><gml:TimePeriod gml:id="uuid.a4ab7504-4ffa-4b69-9d87-3c60cb690614"><gml:beginPosition>2020-06-16T05:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T14:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">100</meanWindDirection><meanWindSpeed uom="[kn_i]">3</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.dd4c456f-daa0-4fd4-82c2-a84d2764c560"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1"/><base uom="[ft_i]">5000</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></changeForecast><changeForecast><MeteorologicalAerodromeForecast changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="uuid.96e4900a-6618-4e0a-9fb5-4cb72c7f01ed"><phenomenonTime><gml:TimePeriod gml:id="uuid.88705462-4b5a-45d5-8184-1c68897ed186"><gml:beginPosition>2020-06-16T14:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">150</meanWindDirection><meanWindSpeed uom="[kn_i]">4</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.219d3e54-ad87-485c-8ccc-488622e38281"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1"/><base uom="[ft_i]">4000</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></changeForecast><extension><USMetadata xmlns="http://www.weather.gov/iwxxm-us/3.0" xsi:schemaLocation="http://www.weather.gov/iwxxm-us/3.0 https://nws.weather.gov/schemas/iwxxm-us/3.0/taf.xsd"><procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01008013curr.pdf" xlink:title="NWS Instruction 10-813, Aviation Weather Services, Terminal Aerodrome Forecasts"/></USMetadata></extension></TAF></meteorologicalInformation><meteorologicalInformation><TAF gml:id="uuid.4d77f421-db50-4355-8e41-ef32576403d9" permissibleUsage="OPERATIONAL" reportStatus="NORMAL" xmlns="http://icao.int/iwxxm/3.0" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://icao.int/iwxxm/3.0 https://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd"><issueTime><gml:TimeInstant gml:id="uuid.23fa0713-1c8c-450c-bed2-4acee78b5eb5"><gml:timePosition>2020-06-15T17:29:00Z</gml:timePosition></gml:TimeInstant></issueTime><aerodrome><aixm:AirportHeliport gml:id="uuid.4e773075-635d-48cf-beac-a2dabe033304"><aixm:timeSlice><aixm:AirportHeliportTimeSlice gml:id="uuid.196daf61-6b9a-4d65-8ce3-b2c9501b0cdf"><gml:validTime/><aixm:interpretation>SNAPSHOT</aixm:interpretation><aixm:locationIndicatorICAO>KFWA</aixm:locationIndicatorICAO><aixm:ARP><aixm:ElevatedPoint axisLabels="Lat Long" gml:id="uuid.c00b8314-c8ee-4643-923c-6b37a34a6683" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326"><gml:pos>41.01 -85.20</gml:pos></aixm:ElevatedPoint></aixm:ARP></aixm:AirportHeliportTimeSlice></aixm:timeSlice></aixm:AirportHeliport></aerodrome><validPeriod><gml:TimePeriod gml:id="uuid.7fb14cd7-2b8c-441a-bcd3-3517e7fb1408"><gml:beginPosition>2020-06-15T18:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></validPeriod><baseForecast><MeteorologicalAerodromeForecast cloudAndVisibilityOK="false" gml:id="uuid.94139a95-d1d4-4d7b-9be7-b715cb4ab683"><phenomenonTime><gml:TimePeriod gml:id="uuid.2df27717-0ccd-4a97-99aa-5362f53a71b3"><gml:beginPosition>2020-06-15T17:29:00Z</gml:beginPosition><gml:endPosition>2020-06-16T15:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">60</meanWindDirection><meanWindSpeed uom="[kn_i]">9</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.8074ccdb-85fa-4445-b276-0605808ae646"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/2"/><base uom="[ft_i]">3500</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></baseForecast><changeForecast><MeteorologicalAerodromeForecast changeIndicator="FROM" cloudAndVisibilityOK="false" gml:id="uuid.58aa3d99-eb91-43bf-8498-78fa11a8009e"><phenomenonTime><gml:TimePeriod gml:id="uuid.5b5a9b8e-48aa-4be8-b1f3-993beeab6312"><gml:beginPosition>2020-06-16T15:00:00Z</gml:beginPosition><gml:endPosition>2020-06-16T18:00:00Z</gml:endPosition></gml:TimePeriod></phenomenonTime><prevailingVisibility uom="m">10000</prevailingVisibility><prevailingVisibilityOperator>ABOVE</prevailingVisibilityOperator><surfaceWind><AerodromeSurfaceWindForecast variableWindDirection="false"><meanWindDirection uom="deg">80</meanWindDirection><meanWindSpeed uom="[kn_i]">5</meanWindSpeed></AerodromeSurfaceWindForecast></surfaceWind><cloud><AerodromeCloudForecast gml:id="uuid.9ca955d9-4444-4b33-8c37-12361e42b82f"><layer><CloudLayer><amount xlink:href="http://codes.wmo.int/bufr4/codeflag/0-20-008/1"/><base uom="[ft_i]">5000</base></CloudLayer></layer></AerodromeCloudForecast></cloud></MeteorologicalAerodromeForecast></changeForecast><extension><USMetadata xmlns="http://www.weather.gov/iwxxm-us/3.0" xsi:schemaLocation="http://www.weather.gov/iwxxm-us/3.0 https://nws.weather.gov/schemas/iwxxm-us/3.0/taf.xsd"><procedure xlink:href="https://www.nws.noaa.gov/directives/sym/pd01008013curr.pdf" xlink:title="NWS Instruction 10-813, Aviation Weather Services, Terminal Aerodrome Forecasts"/></USMetadata></extension></TAF></meteorologicalInformation><bulletinIdentifier>A_LTUS43KIWX151700_C_KIWX_202015172936.xml</bulletinIdentifier></MeteorologicalBulletin>
'''  # noqa: E501
