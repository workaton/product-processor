from app.extractors import AirepExtractor
import pytest


class TestAirepExtractor:

    @pytest.fixture
    def extractor(self):
        return AirepExtractor()

    @pytest.mark.asyncio
    async def test_extract_iwxxmus10(self, extractor):
        assert await extractor.extract(IWXXMUS10) == {}


IWXXMUS10 = b'''\
<?xml version="1.0" encoding="utf-8"?><!-- Original TAC:
000
UAUS31 KWBC 131709
ARP UAL1738 3816N 09429W 1700 F390 MS55 292/049KT TB LGT=
 -->
<iwxxm-us:AircraftReport gml:id="uuid.c85f0489-f0f6-4975-986a-58143c21a428" xmlns:aixm="http://www.aixm.aero/schema/5.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/1.1" xmlns:iwxxm-us="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release" xmlns:metce="http://def.wmo.int/metce/2013" xmlns:om="http://www.opengis.net/om/2.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nws.weather.gov/schemas/IWXXM-US/1.0/Release http://nws.weather.gov/schemas/IWXXM-US/1.0/Release/schemas/aircraftreport.xsd">
  <iwxxm-us:flightLevelUnknownFlag>false</iwxxm-us:flightLevelUnknownFlag>
  <iwxxm-us:observation>
    <om:OM_Observation gml:id="uuid.3c141ca3-598a-46fd-803c-dde45502aefc">
      <om:type xlink:href="http://codes.wmo.int/49-2/observation-type/IWXXM/1.0/AircraftReportObservation"/>
      <om:phenomenonTime>
        <gml:TimeInstant gml:id="uuid.34b23eff-2f11-4be5-821f-477d3a77a75d">
          <gml:timePosition>2020-07-09T16:00:00</gml:timePosition>
        </gml:TimeInstant>
      </om:phenomenonTime>
      <om:resultTime xlink:href="#uuid.34b23eff-2f11-4be5-821f-477d3a77a75d"/>
      <om:procedure>
        <metce:Process gml:id="uuid.ce0997eb-d33f-46cc-9bed-7e90971a8aa7">
          <gml:description>ICAO Annex 3 Meteorological Service for International Air Navigation, Chapter 5 &quot;Aircraft observations and reports&quot;</gml:description>
        </metce:Process>
      </om:procedure>
      <om:observedProperty xlink:href="http://codes.wmo.int/49-2/observables-property/AircraftReport" xlink:title="ICAO Annex 3 Meteorological Service for International Air Navigation, Chapter 5 Aircraft observations and reports"/>
      <om:featureOfInterest>
        <gml:DynamicFeature gml:id="uuid.bacc34fe-2e55-4e6a-a4ed-954d378520bc">
          <gml:description>Aircraft observation of meteorological phenomena at a given time and location</gml:description>
          <gml:location>
            <gml:MultiPoint gml:id="uuid.43252420-445e-4c84-8e22-356aa2182afd">
              <gml:pointMember>
                <gml:Point axisLabels="Lat Long" gml:id="uuid.50788e5b-7b8d-44b7-b6bd-39443ce22f3a" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">
                  <gml:pos>40.6667 -89.7833</gml:pos>
                </gml:Point>
              </gml:pointMember>
            </gml:MultiPoint>
          </gml:location>
        </gml:DynamicFeature>
      </om:featureOfInterest>
      <om:result>
        <iwxxm-us:AircraftMeteorlogicalObservationRecord gml:id="uuid.af3082df-1f76-4f85-a190-49cdfdf5fbe1">
          <iwxxm-us:variableDirection>false</iwxxm-us:variableDirection>
          <iwxxm-us:remarks/>
          <iwxxm-us:windSpeed uom="m/s">10.80</iwxxm-us:windSpeed>
          <iwxxm-us:windDirection uom="deg">276</iwxxm-us:windDirection>
          <iwxxm-us:turbulence>
            <iwxxm-us:turbulence gml:id="uuid.6b47901c-f1e5-4b9a-a89b-07e33a531612">
              <iwxxm-us:turbRangeStart xlink:href="http://codes.wmo.int/bufr4/codeflag/0-11-030/" xlink:title="LGT-MOD"/>
            </iwxxm-us:turbulence>
          </iwxxm-us:turbulence>
          <iwxxm-us:temperature uom="K">233.15</iwxxm-us:temperature>
          <iwxxm-us:cloudCover>
            <iwxxm-us:Clouds gml:id="uuid.ce73e9f0-2e5d-4ea8-89af-fd91f4d2217e"/>
          </iwxxm-us:cloudCover>
        </iwxxm-us:AircraftMeteorlogicalObservationRecord>
      </om:result>
    </om:OM_Observation>
  </iwxxm-us:observation>
  <iwxxm-us:aircraftReference>KWBC</iwxxm-us:aircraftReference>
  <iwxxm-us:flightLevel>
    <iwxxm-us:VerticalLevel gml:id="uuid.8ffbe053-f277-496e-ab84-d41cde5c6de9">
      <iwxxm-us:verticalLevelReference>STD</iwxxm-us:verticalLevelReference>
      <iwxxm-us:verticalLevel uom="[ft_i]">34000</iwxxm-us:verticalLevel>
    </iwxxm-us:VerticalLevel>
  </iwxxm-us:flightLevel>
  <iwxxm-us:reportType xlink:href="http://codes.nws.noaa.gov/FMH-12/1998/ReportType/SPECIAL"/>
</iwxxm-us:AircraftReport>
'''  # noqa: E501
