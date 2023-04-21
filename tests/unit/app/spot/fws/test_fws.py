import os
import pytest

from app.spot.fws.fws import FwsParser, FwsApp, FwsProduct, InvalidProduct, InvalidTag, LegacyTag


class TestFwsParser():
    '''Test FWS daemon'''
    
    @pytest.fixture
    def parser(self):
        return FwsParser()

    def test_invalid_product(self,parser):
        filename = "products/invalid.fws"
        with open(os.path.join(os.path.dirname(__file__), filename)) as file:
            data: str = file.read()
        with pytest.raises(InvalidProduct) as exc:
            parser.parse(data)
        assert data in str(exc.value)

    def test_invalid_tag(self,parser):
        filename = "products/invalid_tag.fws"
        with open(os.path.join(os.path.dirname(__file__), filename)) as file:
            data: str = file.read()
        with pytest.raises(InvalidTag):
            parser.parse(data)

    def test_legacy_tag(self,parser):
        filename = "products/legacy_tag.fws"
        with open(os.path.join(os.path.dirname(__file__), filename)) as file:
            data: str = file.read()
        with pytest.raises(LegacyTag):
            parser.parse(data)

    def test_valid(self,parser):
        filename = "products/valid.fws"
        with open(os.path.join(os.path.dirname(__file__), filename)) as file:
            data: str = file.read()
        product = FwsProduct(parser.parse(data))
        assert product.id == EXPECTED_RESULT["id"]
        assert product.update == EXPECTED_RESULT["update"]
        assert product.forecaster == EXPECTED_RESULT["forecaster"]
        assert product.corrected == EXPECTED_RESULT["corrected"]
        # assert product.text == EXPECTED_RESULT["text"]


EXPECTED_RESULT = {
    'id': '9999999',
    'update': '0',
    'text': '''
SPOT FORECAST FOR GLAZE 1...USFS
NATIONAL WEATHER SERVICE PENDLETON OR
306 AM PDT WED MAY 27 2015

FORECAST IS BASED ON IGNITION TIME OF 1100 PDT ON MAY 27.
IF CONDITIONS BECOME UNREPRESENTATIVE...CONTACT THE NATIONAL WEATHER
SERVICE.

.DISCUSSION...AN UPPER LOW PRESSURE SYSTEM WILL MOVE TO THE SOUTHEAST
AND AWAY FROM THE BURN SITE TODAY AND TONIGHT. THIS WILL BE REPLACED
BY HIGH PRESSURE ALOFT WITH DRY CONDITIONS AND A WARMING TREND THROUGH
THE END OF THE WEEK. WINDS WILL BE LIGHT AND MOSTLY TERRAIN DRIVEN.

***THUNDERSTORMS IMPLY GUSTY AND ERRATIC WINDS***
***WINDS ARE 20 FOOT 10 MINUTE AVERAGES***
***CWR-CHANCE OF WETTING RAIN 0.10 OR GREATER***
***FORECAST IS VALID FOR 12 HOURS AFTER ISSUANCE***

.TODAY...

SKY/WEATHER.........PARTLY CLOUDY.
CWR.................0 PERCENT.
MAX TEMPERATURE.....74-76.
MIN HUMIDITY........28-30 PERCENT.
WIND (20 FT)........VARIABLE 0-4 MPH BECOMING NORTH 2-6 MPH IN THE
                    AFTERNOON.
RIDGETOP WIND.......VARIABLE 1-5 MPH BECOMING NORTHWEST 3-7
TRANSPORT WINDS.....VARIABLE WINDS 1-5 MPH BECOMING NORTHWEST 4-9
                    MPH IN THE AFTERNOON.

        TEMPERATURE     HUMIDITY     20-FT WIND (MPH)
0800        52             69           VRBL 1-5
1000        61             50           NW 1-5
1200        68             38           NW 2-6
1400        74             31           NW 2-6
1600        75             29           NW 2-6
1800        72             37           NW 2-6
2000        67             45           NW 1-5

.TONIGHT...

SKY/WEATHER.........MOSTLY CLEAR.
CWR.................0 PERCENT.
MIN TEMPERATURE.....40-42.
MAX HUMIDITY........88-90 PERCENT.
WIND (20 FT)........NORTHWEST 1-5 MPH BECOMING DRAINAGE 0-4 MPH AFTER
                    DARK.
RIDGETOP WIND.......NORTHWEST 2-6 MPH BECOMING SOUTHEAST 1-5 MPH
                    OVERNIGHT.
TRANSPORT WINDS.....NORTHWEST 3-7 MPH BECOMING SOUTHEAST 1-5 MPH
                    OVERNIGHT.

.THURSDAY...

SKY/WEATHER.........MOSTLY SUNNY THEN BECOMING PARTLY CLOUDY.
CWR.................0 PERCENT.
MAX TEMPERATURE.....79-81.
MIN HUMIDITY........25-27 PERCENT.
WIND (20 FT)........VARIABLE 0-4 MPH EARLY BECOMING NORTHWEST 2-6 MPH IN THE
                    AFTERNOON.
RIDGETOP WIND.......VARIABLE 1-5 MPH EARLY BECOMING NORTHWEST 3-7 MPH IN THE
                    AFTERNOON.
TRANSPORT WINDS.....VARIABLE 1-5 MPH EARLY BECOMING NORTHWEST 4-9 MPH IN THE
                    AFTERNOON.

$$

FORECASTER...ROGER CLOUTIER
REQUESTED BY...GUILLORY
TYPE OF REQUEST...PRESCRIBED
.TAG 9999999.0/BYZ


''',
    'forecaster': 'ROGER CLOUTIER',
    'corrected': False
}


_EXPECTED_RESULT = {
    'id': '2309648',
    'update': '0',
    'text': '''Spot Forecast for De Soto Dantzler area...USDA Forest Service
National Weather Service New Orleans LA
1136 AM CDT Mon Apr 17 2023

If conditions become unrepresentative, contact the National Weather
Service.

We can be reached at (985) 649-0357 if you have questions or concerns
with this forecast.

.DISCUSSION...Drier air continues to work into the region and
with highs today expected in the 70s min rh values are expected
to fall below 30 for much of the region and could even approach
20 in a few areas. However, recent rainfall and lackluster winds 
should help limit the overall fire weather concerns. This cooler 
and drier air will last through around midweek before moisture 
returns with our next system.

.REST OF TODAY...

Sky/weather.........Sunny (0-10 percent). 
Chance of pcpn......0 percent. 
Max temperature.....Around 75. 
Min humidity........21 percent. 
Dewpoint............46 decreasing to 33. 
Max apparent temp...75. 
Wind (20 ft)........Light winds becoming north 5 to 7 mph in the 
                    late morning and afternoon. 
Mixing height (m)...91-1463 meters AGL. 
Transport winds.....North 5 to 14 mph. 
Transport winds m/s.North 2 to 6 meters/second. 
LVORI...............3. 
Rainfall amount.....0.00 inches. 

TIME (CDT)      7AM 8AM 9AM 10A 11A 12P 1PM 2PM 3PM 4PM 5PM 
Sky (%).........3   5   5   4   3   1   2   4   3   2   2   
Weather cov.....                                            
Weather type....                                            
Tstm cov........                                            
Chc of pcpn (%).0   0   0   0   0   0   0   0   0   0   0   
Temp............46  52  60  66  65  68  71  72  73  75  73  
Dewpoint........45  48  45  43  34  34  33  32  32  32  32  
RH..............96  86  58  43  31  28  25  23  22  21  22  
Aparnt tmp (F)..46  52  60  66  65  68  71  72  73  75  73  
20 FT wind dir..WNW NNW N   N   N   N   N   NNW NNW NNW NNW 
20 FT wind spd..2   3   5   6   7   7   7   7   8   8   7   
20 FT wind gust.6   9   13  15  13  12  12  12  12  12  12  
Mix hgt (km)....0.1 0.1 0.1 1.0 1.0 1.0 1.4 1.4 1.4 1.5 1.5 
Transp wind dir.NW  NW  NW  N   N   N   NNW NNW NNW NNW NNW 
Transp wind spd.5   5   5   14  14  14  13  13  13  13  13  
Trans wind dir..NW  NW  NW  N   N   N   NNW NNW NNW NNW NNW 
Trans spd (m/s).2   2   2   6   6   6   6   6   6   6   6   
LVORI...........4   3   3   1   1   1   1   1   1   1   1   

.TONIGHT...

Sky/weather.........Mostly clear (0-10 percent). 
Chance of pcpn......0 percent. 
Min temperature.....Around 49. 
Max humidity........74 percent. 
Dewpoint............34 increasing to 43. 
Max apparent temp...73. 
Wind (20 ft)........North winds around 5 mph early in the evening 
                    becoming light. 
Mixing height (m)...91-1463 meters AGL. 
Transport winds.....Northwest 7 to 13 mph shifting to the north 
                    around 3 mph overnight, then shifting to the 
                    northeast after 3 am. 
Transport winds m/s.North around 6 meters/second decreasing to 1 to 
                    4 meters/second in the evening and overnight, 
                    then shifting to the northeast around 1 
                    meters/second after 3 am. 
LVORI...............3. 
Rainfall amount.....0.00 inches. 

TIME (CDT)      6PM 7PM 8PM 9PM 10P 11P MID 1AM 2AM 3AM 4AM 5AM 
Sky (%).........0   0   2   1   2   2   1   1   9   14  8   4   
Weather cov.....                                                
Weather type....                                                
Tstm cov........                                                
Chc of pcpn (%).0   0   0   0   0   0   0   0   0   0   0   0   
Temp............73  69  64  60  58  56  55  53  52  51  50  50  
Dewpoint........34  43  44  44  44  44  44  43  43  43  42  42  
RH..............24  39  48  55  59  64  66  69  71  74  74  74  
Aparnt tmp (F)..73  69  64  60  58  56  55  53  52  51  50  50  
20 FT wind dir..NNW NNW NNW NW  NW  NW  NW  NNW N   N   NE  NE  
20 FT wind spd..6   3   3   2   2   2   2   2   2   2   2   2   
20 FT wind gust.10  10  8   7   6   6   6           3   3   3   
Mix hgt (km)....1.5 0.2 0.2 0.2 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 
Transp wind dir.NNW NNW NNW NNW NNW NNW NNW N   N   N   ENE ENE 
Transp wind spd.13  10  10  10  7   7   7   3   3   3   3   3   
Trans wind dir..NNW NNW NNW NNW NNW NNW NNW N   N   N   ENE ENE 
Trans spd (m/s).6   4   4   4   3   3   3   1   1   1   1   1   
LVORI...........1   2   2   3   3   3   3   3   3   3   4   3   

.TUESDAY...

Sky/weather.........Sunny (15-25 percent). 
Chance of pcpn......0 percent. 
Max temperature.....Around 78. 
Min humidity........30 percent. 
Dewpoint............44. 
Max apparent temp...78. 
Wind (20 ft)........Light winds becoming south 5 to 8 mph late in 
                    the morning. 
Mixing height (m)...91-1311 meters AGL. 
Transport winds.....East 3 to 6 mph shifting to the southeast 9 to 
                    10 mph in the late morning and afternoon. 
Transport winds m/s.Southeast 3 to 4 meters/second. 
LVORI...............3. 
Rainfall amount.....0.00 inches. 

TIME (CDT)      6AM 7AM 8AM 9AM 10A 11A 12P 1PM 2PM 3PM 4PM 5PM 
Sky (%).........4   7   1   1   3   3   2   4   9   14  39  37  
Weather cov.....                                                
Weather type....                                                
Tstm cov........                                                
Chc of pcpn (%).0   0   0   0   0   0   0   0   0   0   0   0   
Temp............50  50  55  62  68  72  75  76  77  78  77  75  
Dewpoint........42  42  44  46  45  44  44  43  43  44  43  45  
RH..............74  74  66  56  43  37  33  31  30  30  30  34  
Aparnt tmp (F)..50  50  55  62  68  72  75  76  77  78  77  75  
20 FT wind dir..ENE ENE E   ESE SE  SE  SSE S   S   S   S   S   
20 FT wind spd..2   2   2   3   5   6   6   6   7   8   9   8   
20 FT wind gust.        5   6   8   9   9   10  10  10  12  10  
Mix hgt (km)....0.1 0.1 0.1 0.1 0.7 0.7 0.7 1.3 1.3 1.3 1.0 1.0 
Transp wind dir.ENE E   E   E   SE  SE  SE  SSE SSE SSE S   S   
Transp wind spd.3   6   6   6   9   9   9   10  10  10  10  10  
Trans wind dir..ENE E   E   E   SE  SE  SE  SSE SSE SSE S   S   
Trans spd (m/s).1   3   3   3   4   4   4   4   4   4   4   4   
LVORI...........3   3   3   3   2   2   2   2   2   2   2   2   

$$
Forecaster...FRYE
Requested by...Mark Jamieson
Type of request...PRESCRIBED
.TAG 2309648.0/LIX
.DELDT 04/17/23
.FormatterVersion 2.0.0


''',
    'forecaster': 'FRYE',
    'corrected': False
}
