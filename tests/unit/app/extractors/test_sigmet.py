from app.extractors import SigmetExtractor
from ngitws.typing import JsonType
import pytest


class TestSigmetExtractor:

    @pytest.fixture
    def extractor(self):
        return SigmetExtractor()

    @pytest.mark.asyncio
    async def test_extract_sigmet_iwxxm30_domestic(self, extractor):
        assert await extractor.extract(SIGMET_IWXXM_30_US) == EXPECTED_SIGMET_IWXXM_30_US

    @pytest.mark.asyncio
    async def test_extract_sigmet_iwxxm30_international(self, extractor):
        assert await extractor.extract(SIGMET_IWXXM_30_INTL) == EXPECTED_SIGMET_IWXXM_30_INTL

    @pytest.mark.asyncio
    async def test_extract_airmet_iwxxm30_domestic(self, extractor):
        assert await extractor.extract(AIRMET_IWXXM_30_US) == EXPECTED_AIRMET_IWXXM_30_US

    @pytest.mark.asyncio
    async def test_extract_airmet_iwxxm30_international(self, extractor):
        assert await extractor.extract(AIRMET_IWXXM_30_INTL) == EXPECTED_AIRMET_IWXXM_30_INTL


EXPECTED_AIRMET_IWXXM_30_INTL = {
    'evolvingCondition': {
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [42.82, 13.05],
                [43.48, 13.3],
                [43.6, 11.72],
                [40.47, 14.67],
                [37.3, 14.8],
                [38.4, 16.77],
                [41.17, 15.07],
                [41.45, 14.3],
                [42.82, 13.05]
            ]]
        }
    },
    'issueTime': '2020-09-15T17:36:00Z',
    'issuingAirTrafficServicesRegion': 'LIRR',
    'issuingAirTrafficServicesUnit': 'LIRR',
    'originatingMeteorologicalWatchOffice': 'LIIB',
    'phenomenon': 'http://codes.wmo.int/49-2/AirWxPhenomena/MT_OBSC',
    'sequenceNumber': '18',
    'validPeriod': {
        'start': '2020-09-15T18:00:00Z',
        'end': '2020-09-15T22:00:00Z'
    }
}

EXPECTED_AIRMET_IWXXM_30_US: JsonType = {
    'evolvingCondition': {
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [22.5, -160.46],
                [22.22, -160.76],
                [21.89, -160.91],
                [21.44, -160.82],
                [21.16, -160.47],
                [21.17, -160.11],
                [21.1, -159.85],
                [21.08, -159.51],
                [21.14, -159.24],
                [21.3, -159.01],
                [21.15, -158.86],
                [20.89, -158.71],
                [20.62, -158.51],
                [20.56, -158.15],
                [20.52, -157.86],
                [20.31, -157.64],
                [20.17, -157.41],
                [19.93, -157.08],
                [19.73, -156.9],
                [19.46, -156.82],
                [19.23, -156.73],
                [18.86, -156.66],
                [18.58, -156.47],
                [18.3, -156.12],
                [18.15, -155.85],
                [18.15, -155.54],
                [18.32, -155.26],
                [18.47, -155.03],
                [18.64, -154.67],
                [18.86, -154.39],
                [19.24, -154.09],
                [19.69, -154.08],
                [20.07, -154.19],
                [20.55, -154.61],
                [20.94, -155.19],
                [21.27, -155.43],
                [21.52, -155.82],
                [21.66, -156.2],
                [21.89, -156.68],
                [21.97, -157.15],
                [22.27, -157.52],
                [22.46, -157.97],
                [22.35, -158.34],
                [22.55, -158.53],
                [22.66, -158.68],
                [22.87, -159.06],
                [22.98, -159.47],
                [22.88, -159.78],
                [22.76, -160.05],
                [22.63, -160.24],
                [22.5, -160.46]
            ]],
        }
    },
    'issueTime': '2020-10-05T21:35:00Z',
    'issuingAirTrafficServicesRegion': None,
    'issuingAirTrafficServicesUnit': 'HNL',
    'originatingMeteorologicalWatchOffice': 'PHFO',
    'phenomenon': 'http://codes.wmo.int/49-2/AirWxPhenomena/MT_OBSC',
    'sequenceNumber': '5',
    'validPeriod': {
        'start': '2020-10-05T22:00:00Z',
        'end': '2020-10-06T04:00:00Z'
    }
}

EXPECTED_SIGMET_IWXXM_30_US = {
    'evolvingCondition': {
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [26.67, -78.79],
                [26.22, -83.86],
                [24.01, -83.31],
                [23.9, -78.24],
                [26.67, -78.79]
            ]],
        },
        'directionOfMotion': {'unit': 'deg', 'value': '0'},
        'speedOfMotion': {'unit': '[kn_i]', 'value': '5'}
    },
    'issueTime': '2020-09-10T14:55:00Z',
    'issuingAirTrafficServicesRegion': None,
    'issuingAirTrafficServicesUnit': 'MKCE',
    'originatingMeteorologicalWatchOffice': 'KKCI',
    'phenomenon': None,
    'sequenceNumber': None,
    'validPeriod': {
        'start': '2020-09-10T14:55:00Z',
        'end': '2020-09-10T20:55:00Z'
    }
}

EXPECTED_SIGMET_IWXXM_30_INTL = {
    'evolvingCondition': {
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [35.0, -66.0],
                [28.25, -62.0],
                [31.0, -56.5],
                [35.0, -59.25],
                [35.0, -66.0]
            ]],
        },
        'directionOfMotion': {'unit': 'deg', 'value': '90'},
        'speedOfMotion': {'unit': '[kn_i]', 'value': '30'}
    },
    'issueTime': '2020-09-16T10:10:00Z',
    'issuingAirTrafficServicesRegion': 'KZNY',
    'issuingAirTrafficServicesUnit': 'KZNY',
    'originatingMeteorologicalWatchOffice': 'KKCI',
    'phenomenon': 'http://codes.wmo.int/49-2/SigWxPhenomena/FRQ_TS',
    'sequenceNumber': 'DELTA 9',
    'validPeriod': {
        'start': '2020-09-16T10:10:00Z',
        'end': '2020-09-16T14:10:00Z'
    }
}


AIRMET_IWXXM_30_INTL = b'''\
<?xml version="1.0" encoding="UTF-8"?>\n<iwxxm:AIRMET xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/3.0" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd" gml:id="uuid.fb62ee73-5b40-3d2a-981b-6ce965de8b3c" reportStatus="NORMAL" permissibleUsage="OPERATIONAL" translatedBulletinID="WAIY32LIRR151736" translatedBulletinReceptionTime="2020-09-11T15:51:46Z" translationTime="2020-09-11T15:51:46Z">\n  <iwxxm:issueTime>\n    <gml:TimeInstant gml:id="uuid.1f70ae7e-0322-30c7-8f8a-fb3f5e39ce51">\n      <gml:timePosition>2020-09-15T17:36:00Z</gml:timePosition>\n    </gml:TimeInstant>\n  </iwxxm:issueTime>\n  <iwxxm:issuingAirTrafficServicesUnit>\n    <aixm:Unit gml:id="uuid.c4c151ed-50ef-39eb-8d36-e626dcacf7f4">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.ceccc355-8d2e-3a7a-9b1a-ddf350980e8d">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>LIRR FIC</aixm:name>\n          <aixm:type>FIC</aixm:type>\n          <aixm:designator>LIRR</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:issuingAirTrafficServicesUnit>\n  <iwxxm:originatingMeteorologicalWatchOffice>\n    <aixm:Unit gml:id="uuid.37a98667-49ba-365a-ae8d-ead3b3d687ed">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.e0847324-47a4-36b7-91e7-553ea432b416">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>LIIB MWO</aixm:name>\n          <aixm:type>MWO</aixm:type>\n          <aixm:designator>LIIB</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:originatingMeteorologicalWatchOffice>\n  <iwxxm:issuingAirTrafficServicesRegion>\n    <aixm:Airspace gml:id="uuid.258e8b98-70cd-32a7-a567-984c4eac1549">\n      <aixm:timeSlice>\n        <aixm:AirspaceTimeSlice gml:id="uuid.37bfdaf4-da0d-3cf9-999a-ae8f6eb8f753">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:type>FIR</aixm:type>\n          <aixm:designator>LIRR</aixm:designator>\n          <aixm:name>ROMA FIR</aixm:name>\n        </aixm:AirspaceTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Airspace>\n  </iwxxm:issuingAirTrafficServicesRegion>\n  <iwxxm:sequenceNumber>18</iwxxm:sequenceNumber>\n  <iwxxm:validPeriod>\n    <gml:TimePeriod gml:id="uuid.320ebce9-308c-37f2-9a7e-c0e2fb8b686a">\n      <gml:beginPosition>2020-09-15T18:00:00Z</gml:beginPosition>\n      <gml:endPosition>2020-09-15T22:00:00Z</gml:endPosition>\n    </gml:TimePeriod>\n  </iwxxm:validPeriod>\n  <iwxxm:phenomenon xlink:href="http://codes.wmo.int/49-2/AirWxPhenomena/MT_OBSC"/>\n  <iwxxm:analysis>\n    <iwxxm:AIRMETEvolvingConditionCollection gml:id="uuid.5300d31e-04e5-35d0-862d-16cc5a54b787" timeIndicator="FORECAST">\n      <iwxxm:phenomenonTime xlink:href="#uuid.320ebce9-308c-37f2-9a7e-c0e2fb8b686a"/>\n      <iwxxm:member>\n        <iwxxm:AIRMETEvolvingCondition gml:id="uuid.64073211-7c20-34b1-9b56-8f4ea3998924" intensityChange="NO_CHANGE">\n          <iwxxm:geometry>\n            <aixm:AirspaceVolume gml:id="uuid.886265dc-c233-3b76-ad8e-323ce1b47ea9">\n              <aixm:horizontalProjection>\n                <aixm:Surface gml:id="uuid.acdfa6fd-20f3-3ada-9859-175e6c68c60a" srsDimension="2" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">\n                  <gml:polygonPatches>\n                    <gml:PolygonPatch>\n                      <gml:exterior>\n                        <gml:LinearRing>\n                          <gml:posList count="9">42.82 13.05 43.48 13.30 43.60 11.72 40.47 14.67 37.30 14.80 38.40 16.77 41.17 15.07 41.45 14.30 42.82 13.05</gml:posList>\n                        </gml:LinearRing>\n                      </gml:exterior>\n                    </gml:PolygonPatch>\n                  </gml:polygonPatches>\n                </aixm:Surface>\n              </aixm:horizontalProjection>\n            </aixm:AirspaceVolume>\n          </iwxxm:geometry>\n        </iwxxm:AIRMETEvolvingCondition>\n      </iwxxm:member>\n    </iwxxm:AIRMETEvolvingConditionCollection>\n  </iwxxm:analysis>\n</iwxxm:AIRMET>\n
'''  # noqa: E501

AIRMET_IWXXM_30_US = b'''\
<?xml version="1.0" encoding="UTF-8"?>\n<iwxxm:AIRMET xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/3.0" xmlns:iwxxm-us="http://www.weather.gov/iwxxm-us/3.0" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd http://www.weather.gov/iwxxm-us/3.0 https://nws.weather.gov/schemas/iwxxm-us/3.0/iwxxm-us.xsd" gml:id="uuid.20e2cb54-23dc-3ed8-aeb4-b20ab5b82f00" translationFailedTAC="AIRMET SIERRA UPDATE 5 FOR IFR VALID UNTIL 060400&#10;&#10;.&#10;&#10;NO SIGNIFICANT IFR EXP.&#10;&#10;&#10;&#10;=HNLT WA 052200&#10; &#10;AIRMET TANGO UPDATE 3 FOR TURB VALID UNTIL 060400&#10;\\.&#10;NO SIGNIFICANT TURB EXP.&#10;&#10;&#10;&#10;=HNLZ WA 052200&#10; &#10;AIRMET ZULU UPDATE 3 FOR ICE AND FZLVL VALID UNTIL 060400&#10;\\.&#10;NO SIGNIFICANT ICE EXP.&#10;\\.&#10;FZLVL...160.&#10;\\.&#10;" reportStatus="NORMAL" permissibleUsage="OPERATIONAL" translatedBulletinID="WAHW31HNL052135" translatedBulletinReceptionTime="2020-10-05T17:55:02Z" translationTime="2020-10-05T17:55:02Z" translationCentreDesignator="" translationCentreName="">\n  <!-- unparsed_component(s)=\'=HNLT WA 052200\n \nAIRMET TANGO UPDATE 3 FOR TURB VALID UNTIL 060400 =HNLZ WA 052200\n \nAIRMET ZULU UPDATE 3 FOR ICE AND FZLVL VALID UNTIL 060400\' -->\n  <iwxxm:issueTime>\n    <gml:TimeInstant gml:id="uuid.4c34bdfe-7fc5-3374-8d06-b048ef025a07">\n      <gml:timePosition>2020-10-05T21:35:00Z</gml:timePosition>\n    </gml:TimeInstant>\n  </iwxxm:issueTime>\n  <iwxxm:issuingAirTrafficServicesUnit>\n    <aixm:Unit gml:id="uuid.00a3f5df-ca30-3d87-bd68-627c95a77a22">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.9ee89205-f774-333e-94bc-6de92f654084">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>HNL FIC</aixm:name>\n          <aixm:type>FIC</aixm:type>\n          <aixm:designator>HNL</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:issuingAirTrafficServicesUnit>\n  <iwxxm:originatingMeteorologicalWatchOffice>\n    <aixm:Unit gml:id="uuid.93c1ed17-5255-344d-9694-c12356e10cfa">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.82f9dedd-eb22-3892-933e-61b5d39b5735">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>PHFO MWO</aixm:name>\n          <aixm:type>MWO</aixm:type>\n          <aixm:designator>PHFO</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:originatingMeteorologicalWatchOffice>\n  <iwxxm:issuingAirTrafficServicesRegion xlink:href="https://nws.weather.gov/schemas/iwxxm-us/Airspace/AOR-FA/HFO"/>\n  <iwxxm:sequenceNumber>5</iwxxm:sequenceNumber>\n  <iwxxm:validPeriod>\n    <gml:TimePeriod gml:id="uuid.54b1f80b-f188-389d-aa01-3215bff2dac0">\n      <gml:beginPosition>2020-10-05T22:00:00Z</gml:beginPosition>\n      <gml:endPosition>2020-10-06T04:00:00Z</gml:endPosition>\n    </gml:TimePeriod>\n  </iwxxm:validPeriod>\n  <iwxxm:phenomenon xlink:href="http://codes.wmo.int/49-2/AirWxPhenomena/MT_OBSC"/>\n  <iwxxm:analysis>\n    <iwxxm:AIRMETEvolvingConditionCollection gml:id="uuid.f6732e79-3054-3e4c-87a4-8b15e7088c33" timeIndicator="FORECAST">\n      <iwxxm:phenomenonTime xlink:href="#uuid.4c34bdfe-7fc5-3374-8d06-b048ef025a07"/>\n      <iwxxm:member nilReason="http://codes.wmo.int/common/nil/nothingOfOperationalSignificance"/>\n      <iwxxm:member nilReason="http://codes.wmo.int/common/nil/nothingOfOperationalSignificance"/>\n      <iwxxm:member nilReason="http://codes.wmo.int/common/nil/nothingOfOperationalSignificance"/>\n      <iwxxm:member>\n        <iwxxm:AIRMETEvolvingCondition gml:id="uuid.28c038e2-4c32-3390-add2-9f6754c22417">\n          <iwxxm:geometry>\n            <aixm:AirspaceVolume gml:id="uuid.018f2644-f585-3a93-8c18-dc2da597fb4d">\n              <aixm:horizontalProjection>\n                <aixm:Surface gml:id="uuid.3e9bea64-8a42-31c5-b635-863c118d4ce7" srsDimension="2" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">\n                  <gml:polygonPatches>\n                    <gml:PolygonPatch>\n                      <gml:exterior>\n                        <gml:LinearRing>\n                          <gml:posList count="51">22.50 -160.46 22.22 -160.76 21.89 -160.91 21.44 -160.82 21.16 -160.47 21.17 -160.11 21.10 -159.85 21.08 -159.51 21.14 -159.24 21.30 -159.01 21.15 -158.86 20.89 -158.71 20.62 -158.51 20.56 -158.15 20.52 -157.86 20.31 -157.64 20.17 -157.41 19.93 -157.08 19.73 -156.90 19.46 -156.82 19.23 -156.73 18.86 -156.66 18.58 -156.47 18.30 -156.12 18.15 -155.85 18.15 -155.54 18.32 -155.26 18.47 -155.03 18.64 -154.67 18.86 -154.39 19.24 -154.09 19.69 -154.08 20.07 -154.19 20.55 -154.61 20.94 -155.19 21.27 -155.43 21.52 -155.82 21.66 -156.20 21.89 -156.68 21.97 -157.15 22.27 -157.52 22.46 -157.97 22.35 -158.34 22.55 -158.53 22.66 -158.68 22.87 -159.06 22.98 -159.47 22.88 -159.78 22.76 -160.05 22.63 -160.24 22.50 -160.46</gml:posList>\n                        </gml:LinearRing>\n                      </gml:exterior>\n                    </gml:PolygonPatch>\n                  </gml:polygonPatches>\n                </aixm:Surface>\n              </aixm:horizontalProjection>\n            </aixm:AirspaceVolume>\n          </iwxxm:geometry>\n          <iwxxm:extension>\n            <iwxxm-us:AIRMETEvolvingConditionExtension>\n              <iwxxm-us:freezingLevel>\n                <iwxxm-us:flightLevel gml:id="uuid.e0755df2-10c1-333b-83d5-b06f330acd80">\n                  <aixm:lowerLimit uom="FT">16000</aixm:lowerLimit>\n                  <aixm:lowerLimitReference>MSL</aixm:lowerLimitReference>\n                </iwxxm-us:flightLevel>\n                <iwxxm-us:multipleLevels>false</iwxxm-us:multipleLevels>\n              </iwxxm-us:freezingLevel>\n            </iwxxm-us:AIRMETEvolvingConditionExtension>\n          </iwxxm:extension>\n        </iwxxm:AIRMETEvolvingCondition>\n      </iwxxm:member>\n    </iwxxm:AIRMETEvolvingConditionCollection>\n  </iwxxm:analysis>\n</iwxxm:AIRMET>
'''  # noqa: E501

SIGMET_IWXXM_30_US = b'''\
<?xml version="1.0" encoding="UTF-8"?>\n<iwxxm:SIGMET xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/3.0" xmlns:iwxxm-us="http://www.weather.gov/iwxxm-us/3.0" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd http://www.weather.gov/iwxxm-us/3.0 https://nws.weather.gov/schemas/iwxxm-us/3.0/iwxxm-us.xsd" gml:id="uuid.53c10d9d-df99-39d6-80d5-f8f6b4a16ca6" reportStatus="NORMAL" permissibleUsage="OPERATIONAL" translatedBulletinID="WSUS31MKCE101455" translatedBulletinReceptionTime="2020-09-09T11:15:32Z" translationTime="2020-09-09T11:15:32Z" translationCentreDesignator="" translationCentreName="">\n  <iwxxm:issueTime>\n    <gml:TimeInstant gml:id="uuid.643a8189-9832-335d-9ca5-6ef3c46d1f9d">\n      <gml:timePosition>2020-09-10T14:55:00Z</gml:timePosition>\n    </gml:TimeInstant>\n  </iwxxm:issueTime>\n  <iwxxm:issuingAirTrafficServicesUnit>\n    <aixm:Unit gml:id="uuid.5f7e3c69-79ef-384c-b2b9-8397c41dddfa">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.384c3b01-9f5a-3527-8580-b64bb48281b2">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>MKCE FIC</aixm:name>\n          <aixm:type>FIC</aixm:type>\n          <aixm:designator>MKCE</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:issuingAirTrafficServicesUnit>\n  <iwxxm:originatingMeteorologicalWatchOffice>\n    <aixm:Unit gml:id="uuid.a902e336-84db-3702-bbf8-39e499949719">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.840455fe-f9ff-3210-a437-58db44d2a2cf">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>KKCI MWO</aixm:name>\n          <aixm:type>MWO</aixm:type>\n          <aixm:designator>KKCI</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:originatingMeteorologicalWatchOffice>\n  <iwxxm:issuingAirTrafficServicesRegion xlink:href="https://nws.weather.gov/schemas/iwxxm-us/Airspace/SECTORS/EAST"/>\n  <iwxxm:sequenceNumber nilReason="http://codes.wmo.int/common/nil/missing"/>\n  <iwxxm:validPeriod>\n    <gml:TimePeriod gml:id="uuid.ea83053d-5976-3c08-97f9-8136896a283a">\n      <gml:beginPosition>2020-09-10T14:55:00Z</gml:beginPosition>\n      <gml:endPosition>2020-09-10T20:55:00Z</gml:endPosition>\n    </gml:TimePeriod>\n  </iwxxm:validPeriod>\n  <iwxxm:phenomenon nilReason="http://codes.wmo.int/common/nil/template"/>\n  <iwxxm:analysis>\n    <iwxxm:SIGMETEvolvingConditionCollection gml:id="uuid.a8dbf13b-acde-3a04-acc4-06b8d42e52e7" timeIndicator="FORECAST">\n      <iwxxm:phenomenonTime>\n        <gml:TimePeriod gml:id="uuid.a33cf573-b860-30ce-9eb9-4de7b81f6cd5">\n          <gml:beginPosition>2020-09-10T14:55:00Z</gml:beginPosition>\n          <gml:endPosition>2020-09-10T16:55:00Z</gml:endPosition>\n        </gml:TimePeriod>\n      </iwxxm:phenomenonTime>\n      <iwxxm:member>\n        <iwxxm:SIGMETEvolvingCondition gml:id="uuid.c2ca31d9-4b86-35ea-be2a-2f35333e947f">\n          <iwxxm:geometry>\n            <aixm:AirspaceVolume gml:id="uuid.5e17aed0-77b5-32fb-b8f7-b0d4482a4243">\n              <aixm:upperLimit uom="FL">450</aixm:upperLimit>\n              <aixm:upperLimitReference>STD</aixm:upperLimitReference>\n              <aixm:horizontalProjection>\n                <aixm:Surface gml:id="uuid.a36a072b-88e6-3de5-9440-85e6f77c89d9" srsDimension="2" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">\n                  <gml:polygonPatches>\n                    <gml:PolygonPatch>\n                      <gml:exterior>\n                        <gml:LinearRing>\n                          <gml:posList count="5">26.67 -78.79 26.22 -83.86 24.01 -83.31 23.90 -78.24 26.67 -78.79</gml:posList>\n                        </gml:LinearRing>\n                      </gml:exterior>\n                    </gml:PolygonPatch>\n                  </gml:polygonPatches>\n                </aixm:Surface>\n              </aixm:horizontalProjection>\n              <aixm:extension>\n                <iwxxm-us:AffectedStates gml:id="uuid.e8d8b260-2e86-3e50-aa5b-98362cd3b63d">\n                  <iwxxm-us:stateIDs>FL</iwxxm-us:stateIDs>\n                </iwxxm-us:AffectedStates>\n              </aixm:extension>\n            </aixm:AirspaceVolume>\n          </iwxxm:geometry>\n          <iwxxm:directionOfMotion uom="deg">0</iwxxm:directionOfMotion>\n          <iwxxm:speedOfMotion uom="[kn_i]">5</iwxxm:speedOfMotion>\n          <iwxxm:extension>\n            <iwxxm-us:SIGMETWeatherHazards tag="36E" isSevere="true">\n              <iwxxm-us:weatherPhenomenon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/SIGMETWeatherPhenomena/AreaSvrEmbeddedTS"/>\n              <iwxxm-us:maxWindGusts uom="[kn_i]">115</iwxxm-us:maxWindGusts>\n              <iwxxm-us:tornadicPhenomena>EXPECTED</iwxxm-us:tornadicPhenomena>\n            </iwxxm-us:SIGMETWeatherHazards>\n          </iwxxm:extension>\n        </iwxxm:SIGMETEvolvingCondition>\n      </iwxxm:member>\n    </iwxxm:SIGMETEvolvingConditionCollection>\n  </iwxxm:analysis>\n  <iwxxm:extension>\n    <iwxxm-us:ConvectionGeometry xlink:href="http://nws.weather.gov/codes/NWSI10-811/2013/SIGMETConvectionGeometry/AREA_OF_THUNDERSTORMS/"/>\n  </iwxxm:extension>\n</iwxxm:SIGMET>\n
'''  # noqa: E501

SIGMET_IWXXM_30_INTL = b'''\
<?xml version="1.0" encoding="UTF-8"?>\n<iwxxm:SIGMET xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:aixm="http://www.aixm.aero/schema/5.1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:iwxxm="http://icao.int/iwxxm/3.0" xsi:schemaLocation="http://icao.int/iwxxm/3.0 http://schemas.wmo.int/iwxxm/3.0/iwxxm.xsd" gml:id="uuid.5c1b1d9c-5061-3df7-8145-7c70eeed7d23" reportStatus="NORMAL" permissibleUsage="OPERATIONAL" translatedBulletinID="WSNT04KZNY161010" translatedBulletinReceptionTime="2020-09-11T15:09:21Z" translationTime="2020-09-11T15:09:21Z">\n  <iwxxm:issueTime>\n    <gml:TimeInstant gml:id="uuid.0dc61d9b-50b0-38d1-b38b-b57e964b3658">\n      <gml:timePosition>2020-09-16T10:10:00Z</gml:timePosition>\n    </gml:TimeInstant>\n  </iwxxm:issueTime>\n  <iwxxm:issuingAirTrafficServicesUnit>\n    <aixm:Unit gml:id="uuid.dfc68d25-737f-3301-abd2-f3eea88ef5db">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.a9379832-4410-3ccb-80e8-3616289ba06b">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>KZNY FIC</aixm:name>\n          <aixm:type>FIC</aixm:type>\n          <aixm:designator>KZNY</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:issuingAirTrafficServicesUnit>\n  <iwxxm:originatingMeteorologicalWatchOffice>\n    <aixm:Unit gml:id="uuid.a902e336-84db-3702-bbf8-39e499949719">\n      <aixm:timeSlice>\n        <aixm:UnitTimeSlice gml:id="uuid.840455fe-f9ff-3210-a437-58db44d2a2cf">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:name>KKCI MWO</aixm:name>\n          <aixm:type>MWO</aixm:type>\n          <aixm:designator>KKCI</aixm:designator>\n        </aixm:UnitTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Unit>\n  </iwxxm:originatingMeteorologicalWatchOffice>\n  <iwxxm:issuingAirTrafficServicesRegion>\n    <aixm:Airspace gml:id="uuid.88bdfa9c-69b4-32f2-8c8d-065c9fa0a42d">\n      <aixm:timeSlice>\n        <aixm:AirspaceTimeSlice gml:id="uuid.03f0c1d7-32d5-3de8-81ac-046af5ddc34f">\n          <gml:validTime/>\n          <aixm:interpretation>SNAPSHOT</aixm:interpretation>\n          <aixm:type>FIR</aixm:type>\n          <aixm:designator>KZNY</aixm:designator>\n          <aixm:name>NEW YORK OCEANIC FIR</aixm:name>\n        </aixm:AirspaceTimeSlice>\n      </aixm:timeSlice>\n    </aixm:Airspace>\n  </iwxxm:issuingAirTrafficServicesRegion>\n  <iwxxm:sequenceNumber>DELTA 9</iwxxm:sequenceNumber>\n  <iwxxm:validPeriod>\n    <gml:TimePeriod gml:id="uuid.fa2fde9d-4e56-30c3-b83d-67a84288bb90">\n      <gml:beginPosition>2020-09-16T10:10:00Z</gml:beginPosition>\n      <gml:endPosition>2020-09-16T14:10:00Z</gml:endPosition>\n    </gml:TimePeriod>\n  </iwxxm:validPeriod>\n  <iwxxm:phenomenon xlink:href="http://codes.wmo.int/49-2/SigWxPhenomena/FRQ_TS"/>\n  <iwxxm:analysis>\n    <iwxxm:SIGMETEvolvingConditionCollection gml:id="uuid.7811092e-1f31-3f2d-bf8b-3a5f7aa60705" timeIndicator="OBSERVATION">\n      <iwxxm:phenomenonTime xlink:href="#uuid.0dc61d9b-50b0-38d1-b38b-b57e964b3658"/>\n      <iwxxm:member>\n        <iwxxm:SIGMETEvolvingCondition gml:id="uuid.50e9f1ac-5844-3ee6-9f20-b5df8e79eefb" intensityChange="WEAKEN">\n          <iwxxm:geometry>\n            <aixm:AirspaceVolume gml:id="uuid.f53976a4-3974-3f09-a758-8faa9ccb5ae0">\n              <aixm:upperLimit uom="FL">400</aixm:upperLimit>\n              <aixm:upperLimitReference>STD</aixm:upperLimitReference>\n              <aixm:horizontalProjection>\n                <aixm:Surface gml:id="uuid.9d8a10a9-d688-358d-bd42-97f8691c26f4" srsDimension="2" axisLabels="Lat Long" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">\n                  <gml:polygonPatches>\n                    <gml:PolygonPatch>\n                      <gml:exterior>\n                        <gml:LinearRing>\n                          <gml:posList count="5">35.00 -66.00 28.25 -62.00 31.00 -56.50 35.00 -59.25 35.00 -66.00</gml:posList>\n                        </gml:LinearRing>\n                      </gml:exterior>\n                    </gml:PolygonPatch>\n                  </gml:polygonPatches>\n                </aixm:Surface>\n              </aixm:horizontalProjection>\n            </aixm:AirspaceVolume>\n          </iwxxm:geometry>\n          <iwxxm:directionOfMotion uom="deg">90</iwxxm:directionOfMotion>\n          <iwxxm:speedOfMotion uom="[kn_i]">30</iwxxm:speedOfMotion>\n        </iwxxm:SIGMETEvolvingCondition>\n      </iwxxm:member>\n    </iwxxm:SIGMETEvolvingConditionCollection>\n  </iwxxm:analysis>\n</iwxxm:SIGMET>\n
'''  # noqa: E501
