import json

from app.extractors import CapExtractor
import pytest


class TestCapExtractor:

    @pytest.fixture
    def extractor(self):
        return CapExtractor()

    @pytest.mark.asyncio
    async def test_extract_cap12(self, extractor):
        assert json.loads(json.dumps(await extractor.extract(CAP_XML))) == {
            'alert': {
                'identifier': 'NWS-IDP-PROD-4655545-3804602',
                'note': None,
                'msgType': 'Update',
                'code': 'IPAWSv1.0',
                'references': [
                    {
                        'identifier': 'NWS-IDP-PROD-4654219-3804043',
                        'sender': 'w-nws.webmaster@noaa.gov',
                        'sent': '2020-12-29T04:09:00-08:00'
                    }
                ],
                'sent': '2020-12-29T13:53:00-08:00',
                'sender': 'w-nws.webmaster@noaa.gov',
                'scope': 'Public',
                'status': 'Actual',
                'info': {
                    'language': 'en-US',
                    'event': 'Beach Hazards Statement',
                    'headline': 'Beach Hazards Statement issued December 29 at 1:53PM PST until December 30 at 10:00PM PST by NWS San Francisco CA',  # noqa: E501
                    'eventCode': [
                        {'valueName': 'SAME', 'value': 'NWS'},
                        {'valueName': 'NationalWeatherService', 'value': 'BHS'}
                    ],
                    'effective': '2020-12-29T13:53:00-08:00',
                    'expires': '2020-12-29T23:00:00-08:00',
                    'onset': '2020-12-29T18:00:00-08:00',
                    'eventEndingTime': '2020-12-30T22:00:00-08:00',
                    'certainty': 'Likely',
                    'severity': 'Moderate',
                    'urgency': 'Expected',
                    'category': 'Met',
                    'responseType': 'Avoid',
                    'senderName': 'NWS San Francisco CA',
                    'web': 'http://www.weather.gov',
                    'description': '...Very Long Period Swell will Bring Dangerous Sneaker Waves...\n\n..A very long period WNW swell will impact the Sonoma to Big Sur\ncoast tonight through Wednesday evening. Initial forerunner waves\nof 21 to 23 seconds will begin to arrive along the Sonoma coast\nlate this afternoon before spreading southward during the evening\nhours. Wave heights will rise by Wednesday morning to 5 to 9 feet\nat a periodicity of 18 to 20 seconds. This will result in a high\nrisk of sneaker waves. The largest energetic sneaker waves will\narrive irregularly every few minutes to as infrequently as once\nevery 30 minutes during otherwise deceptively calmer seas, and\nconsequently may catch those on coastal jetties, rocks, piers, or\nshorelines offguard and may injure them or knock them into the\ncold, turbulent ocean. Beachcombing is not advised during this\ntimeframe. In addition, strong rip currents will accompany the\nenergetic wave train, particularly at WNW facing beaches. These\ntypes of events claim lives each year so extreme vigilance is\nadvised if visiting the coast.\n\n* WHAT...A long period WNW swell with initial periods in excess of\n20 seconds will bring a threat of dangerous sneaker waves and\nstrong rip currents to area beaches.\n\n* WHERE...Entire coast from Sonoma southward through Big Sur,\nexcluding the sheltered northern portion of the Monterey Bay.\nThe main impacts will be felt at W-WNW beaches,including but\nnot limited to: Ocean beach, Montara state beach, Halfmoon Bay\nstate beach, Manresa state beach, Marina state beach.\n\n* WHEN...From 6 PM PST this evening through Wednesday evening.\n\n* IMPACTS...Potential sneaker waves will create dangerous\nconditions at area beaches. Steep beaches will have a higher\nrisk of sneaker wave activity with greater wave run-up onto\nbeaches. Occasionally larger waves will also wash over jetties\nand rock outcroppings that normally stay dry.',  # noqa: E501
                    'instruction': 'A Beach Hazard Statement for sneaker waves means that conditions\nare present to support an increased danger of unsuspecting beach\ngoers being swept into the sea by a wave. People walking along\nthe beach should never turn their back to the sea. Fisherman\nshould avoid fishing from rocks or jetties. Beachcombing is not\nadvised.',  # noqa: E501
                    'area': {
                        'areaDesc': 'San Francisco Peninsula Coast; Coastal North Bay Including Point Reyes National Seashore; San Francisco; Northern Monterey Bay; Southern Monterey Bay and Big Sur Coast',  # noqa: E501
                        'geocode': [
                            {'valueName': 'UGC', 'value': 'CAZ509'},
                            {'valueName': 'UGC', 'value': 'CAZ505'},
                            {'valueName': 'UGC', 'value': 'CAZ006'},
                            {'valueName': 'UGC', 'value': 'CAZ529'},
                            {'valueName': 'UGC', 'value': 'CAZ530'},
                            {'valueName': 'SAME', 'value': '006081'},
                            {'valueName': 'SAME', 'value': '006087'},
                            {'valueName': 'SAME', 'value': '006041'},
                            {'valueName': 'SAME', 'value': '006097'},
                            {'valueName': 'SAME', 'value': '006075'},
                            {'valueName': 'SAME', 'value': '006053'}
                        ]
                    },
                    'parameter': [
                        {'valueName': 'BLOCKCHANNEL', 'value': 'CMAS'},
                        {'valueName': 'BLOCKCHANNEL', 'value': 'EAS'},
                        {'valueName': 'BLOCKCHANNEL', 'value': 'NWEM'},
                        {'valueName': 'NWSheadline', 'value': 'BEACH HAZARDS STATEMENT REMAINS IN EFFECT FROM 6 PM PST THIS EVENING THROUGH WEDNESDAY EVENING'},  # noqa: E501
                        {'valueName': 'PIL', 'value': 'MTRCFWMTR'},
                        {'valueName': 'VTEC', 'value': '/O.CON.KMTR.BH.S.0016.201230T0200Z-201231T0600Z/'},
                        {'valueName': 'eventEndingTime', 'value': '2020-12-30T22:00:00-08:00'}
                    ]
                }
            },
            'localTimeZoneOffset': '-08:00'
        }


CAP_XML = b'''\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2" xmlns:ns2="http://gov.fema.ipaws.services/caprequest" xmlns:ns4="http://gov.fema.ipaws.services/IPAWS_CAPService/" xmlns:ns3="http://gov.fema.ipaws.services/capresponse">
    <identifier>NWS-IDP-PROD-4655545-3804602</identifier>
    <sender>w-nws.webmaster@noaa.gov</sender>
    <sent>2020-12-29T13:53:00-08:00</sent>
    <status>Actual</status>
    <msgType>Update</msgType>
    <scope>Public</scope>
    <code>IPAWSv1.0</code>
    <note></note>
    <references>w-nws.webmaster@noaa.gov,NWS-IDP-PROD-4654219-3804043,2020-12-29T04:09:00-08:00</references>
    <info>
        <language>en-US</language>
        <category>Met</category>
        <event>Beach Hazards Statement</event>
        <responseType>Avoid</responseType>
        <urgency>Expected</urgency>
        <severity>Moderate</severity>
        <certainty>Likely</certainty>
        <eventCode>
            <valueName>SAME</valueName>
            <value>NWS</value>
        </eventCode>
        <eventCode>
            <valueName>NationalWeatherService</valueName>
            <value>BHS</value>
        </eventCode>
        <effective>2020-12-29T13:53:00-08:00</effective>
        <onset>2020-12-29T18:00:00-08:00</onset>
        <expires>2020-12-29T23:00:00-08:00</expires>
        <senderName>NWS San Francisco CA</senderName>
        <headline>Beach Hazards Statement issued December 29 at 1:53PM PST until December 30 at 10:00PM PST by NWS San Francisco CA</headline>
        <description>...Very Long Period Swell will Bring Dangerous Sneaker Waves...

..A very long period WNW swell will impact the Sonoma to Big Sur
coast tonight through Wednesday evening. Initial forerunner waves
of 21 to 23 seconds will begin to arrive along the Sonoma coast
late this afternoon before spreading southward during the evening
hours. Wave heights will rise by Wednesday morning to 5 to 9 feet
at a periodicity of 18 to 20 seconds. This will result in a high
risk of sneaker waves. The largest energetic sneaker waves will
arrive irregularly every few minutes to as infrequently as once
every 30 minutes during otherwise deceptively calmer seas, and
consequently may catch those on coastal jetties, rocks, piers, or
shorelines offguard and may injure them or knock them into the
cold, turbulent ocean. Beachcombing is not advised during this
timeframe. In addition, strong rip currents will accompany the
energetic wave train, particularly at WNW facing beaches. These
types of events claim lives each year so extreme vigilance is
advised if visiting the coast.

* WHAT...A long period WNW swell with initial periods in excess of
20 seconds will bring a threat of dangerous sneaker waves and
strong rip currents to area beaches.

* WHERE...Entire coast from Sonoma southward through Big Sur,
excluding the sheltered northern portion of the Monterey Bay.
The main impacts will be felt at W-WNW beaches,including but
not limited to: Ocean beach, Montara state beach, Halfmoon Bay
state beach, Manresa state beach, Marina state beach.

* WHEN...From 6 PM PST this evening through Wednesday evening.

* IMPACTS...Potential sneaker waves will create dangerous
conditions at area beaches. Steep beaches will have a higher
risk of sneaker wave activity with greater wave run-up onto
beaches. Occasionally larger waves will also wash over jetties
and rock outcroppings that normally stay dry.</description>
        <instruction>A Beach Hazard Statement for sneaker waves means that conditions
are present to support an increased danger of unsuspecting beach
goers being swept into the sea by a wave. People walking along
the beach should never turn their back to the sea. Fisherman
should avoid fishing from rocks or jetties. Beachcombing is not
advised.</instruction>
        <web>http://www.weather.gov</web>
        <parameter>
            <valueName>BLOCKCHANNEL</valueName>
            <value>CMAS</value>
        </parameter>
        <parameter>
            <valueName>BLOCKCHANNEL</valueName>
            <value>EAS</value>
        </parameter>
        <parameter>
            <valueName>BLOCKCHANNEL</valueName>
            <value>NWEM</value>
        </parameter>
        <parameter>
            <valueName>NWSheadline</valueName>
            <value>BEACH HAZARDS STATEMENT REMAINS IN EFFECT FROM 6 PM PST THIS EVENING THROUGH WEDNESDAY EVENING</value>
        </parameter>
        <parameter>
            <valueName>PIL</valueName>
            <value>MTRCFWMTR</value>
        </parameter>
        <parameter>
            <valueName>VTEC</valueName>
            <value>/O.CON.KMTR.BH.S.0016.201230T0200Z-201231T0600Z/</value>
        </parameter>
        <parameter>
            <valueName>eventEndingTime</valueName>
            <value>2020-12-30T22:00:00-08:00</value>
        </parameter>
        <area>
            <areaDesc>San Francisco Peninsula Coast; Coastal North Bay Including Point Reyes National Seashore; San Francisco; Northern Monterey Bay; Southern Monterey Bay and Big Sur Coast</areaDesc>
            <geocode>
                <valueName>UGC</valueName>
                <value>CAZ509</value>
            </geocode>
            <geocode>
                <valueName>UGC</valueName>
                <value>CAZ505</value>
            </geocode>
            <geocode>
                <valueName>UGC</valueName>
                <value>CAZ006</value>
            </geocode>
            <geocode>
                <valueName>UGC</valueName>
                <value>CAZ529</value>
            </geocode>
            <geocode>
                <valueName>UGC</valueName>
                <value>CAZ530</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006081</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006087</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006041</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006097</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006075</value>
            </geocode>
            <geocode>
                <valueName>SAME</valueName>
                <value>006053</value>
            </geocode>
        </area>
    </info>
</alert>
'''  # noqa: E501
