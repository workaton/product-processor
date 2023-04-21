from contextlib import ExitStack
from unittest.mock import patch
from uuid import UUID
import xml.etree.ElementTree as etree  # noqa: N813 -- for lxml compatibility

from app.converters import ConversionInput, TcfConverter
from app.media_types import MediaTypes
import pytest
from tests.conftest import compare_xml
import time_machine


class TestTcfConverter:

    @pytest.mark.asyncio
    @time_machine.travel('2020-07-13T21:00:00Z')
    async def test_convert(self):
        converter = TcfConverter()
        with ExitStack() as stack:
            stack.enter_context(patch('uuid.uuid4', return_value=UUID('a36a2138-2c09-473e-bd0d-916531537b02')))
            results = await converter.convert([ConversionInput(TAC, MediaTypes.TEXT_PLAIN)])

        xml_tree = etree.fromstring(XML)
        for result in results:
            assert len(result.data) > 0
            result_tree = etree.fromstring(result.data)
            assert compare_xml(xml_tree, result_tree)


TAC = b'''\
\r\r\n
000\r\r\n
FAUS30 KKCI 132100\r\r\n
CFP04\r\r\n
CCFP 20200713_2100 20200714_0500\r\r\n
AREA 3 1 3 2 0 0 13 342 757 346 758 349 758 356 740 360 733 364 726 350 726 350 726 346 734 340 744 341 755 342 757 342 757 346 722\r\r\n
AREA 3 1 3 3 0 0 9 455 1003 453 1020 448 1033 451 1043 456 1034 460 1019 462 1000 459 998 455 1003 454 973\r\r\n
AREA 3 1 3 2 0 0 14 381 993 373 995 368 996 364 998 360 1002 361 1006 365 1007 370 1008 375 1007 383 1005 385 1001 385 996 385 994 381 993 381 971\r\r\n
AREA 2 1 3 1 0 0 12 463 934 469 925 467 919 462 920 453 928 447 941 444 949 442 956 446 958 451 949 457 942 463 934 475 893\r\r\n
AREA 3 1 3 2 0 0 17 407 997 416 993 424 993 431 1000 436 999 436 991 433 985 432 978 433 970 431 966 426 974 421 978 412 979 406 982 402 987 402 994 407 997 422 986\r\r\n
CANADA OFF\r\r\n
\r\r\n
'''  # noqa: E501

XML = b'''\
<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<uswx:ConvectiveGuidanceForecast xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:om="http://www.opengis.net/om/2.0" xmlns:saf="http://icao.int/saf/1.1" xmlns:uswx="http://nws.weather.gov/schemas/USWX/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://nws.weather.gov/schemas/USWX/1.0 https://nws.weather.gov/schemas/uswx/1.0/cwfg.xsd" automated="false" gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><uswx:issuingMetWatchOffice gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><saf:name>Aviation Weather Center, Kansas City MO</saf:name><saf:type>MWO</saf:type><saf:designator>KKCI</saf:designator></uswx:issuingMetWatchOffice><uswx:convectiveGuidanceForecast gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><om:type xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MesoscaleConvectiveSystemForecastTypes/TCF" /><om:phenomenonTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-14T05:00:00Z</gml:timePosition></gml:TimeInstant></om:phenomenonTime><om:resultTime><gml:TimeInstant gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:timePosition>2020-07-13T21:00:00Z</gml:timePosition></gml:TimeInstant></om:resultTime><om:procedure xlink:href="https://aviationweather.gov/tcf/help" /><om:observedProperty xlink:href="https://aviationweather.gov/tcf/help" /><om:featureOfInterest><gml:FeatureCollection gml:id="uuid.a36a2138-2c09-473e-bd0d-916531537b02"><gml:boundedBy><gml:Envelope axisLabels="Lat Long" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326"><gml:lowerCorner>24.23 -123.42</gml:lowerCorner><gml:upperCorner>49.0 -67.01</gml:upperCorner></gml:Envelope></gml:boundedBy></gml:FeatureCollection></om:featureOfInterest><om:result><uswx:ConvectiveGuidanceForecastRecord numberOfConvectiveFeatures="5"><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MaximumConvectionTopHeights/FL350-FL390" /><uswx:coverageWithInPolygon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ConvectionCoverages/Sparse" /><uswx:forecastConfidence xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ForecastGuidanceConfidences/High" /><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:posList count="15" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2">34.2 -75.7 34.6 -75.8 34.9 -75.8 35.6 -74.0 36.0 -73.3 36.4 -72.6 35.0 -72.6 35.0 -72.6 34.6 -73.4 34.0 -74.4 34.1 -75.5 34.2 -75.7 34.2 -75.7 34.6 -72.2 34.2 -75.7</gml:posList></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MaximumConvectionTopHeights/FL300-FL340" /><uswx:coverageWithInPolygon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ConvectionCoverages/Sparse" /><uswx:forecastConfidence xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ForecastGuidanceConfidences/High" /><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:posList count="11" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2">45.5 -100.3 45.3 -102.0 44.8 -103.3 45.1 -104.3 45.6 -103.4 46.0 -101.9 46.2 -100.0 45.9 -99.8 45.5 -100.3 45.4 -97.3 45.5 -100.3</gml:posList></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MaximumConvectionTopHeights/FL350-FL390" /><uswx:coverageWithInPolygon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ConvectionCoverages/Sparse" /><uswx:forecastConfidence xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ForecastGuidanceConfidences/High" /><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:posList count="16" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2">38.1 -99.3 37.3 -99.5 36.8 -99.6 36.4 -99.8 36.0 -100.2 36.1 -100.6 36.5 -100.7 37.0 -100.8 37.5 -100.7 38.3 -100.5 38.5 -100.1 38.5 -99.6 38.5 -99.4 38.1 -99.3 38.1 -97.1 38.1 -99.3</gml:posList></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MaximumConvectionTopHeights/FL400" /><uswx:coverageWithInPolygon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ConvectionCoverages/Medium" /><uswx:forecastConfidence xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ForecastGuidanceConfidences/High" /><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:posList count="14" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2">46.3 -93.4 46.9 -92.5 46.7 -91.9 46.2 -92.0 45.3 -92.8 44.7 -94.1 44.4 -94.9 44.2 -95.6 44.6 -95.8 45.1 -94.9 45.7 -94.2 46.3 -93.4 47.5 -89.3 46.3 -93.4</gml:posList></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures><uswx:mcsFeatures><uswx:MesoscaleConvectiveSystemFeature><uswx:maximumTop xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/MaximumConvectionTopHeights/FL350-FL390" /><uswx:coverageWithInPolygon xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ConvectionCoverages/Sparse" /><uswx:forecastConfidence xlink:href="https://codes.nws.noaa.gov/NWSI-10-811/ForecastGuidanceConfidences/High" /><uswx:mcsPolygon><gml:exterior><gml:LinearRing><gml:posList count="19" srsName="http://www.opengis.net/def/crs/EPSG/0/4326" axisLabels="Lat Long" srsDimension="2">40.7 -99.7 41.6 -99.3 42.4 -99.3 43.1 -100.0 43.6 -99.9 43.6 -99.1 43.3 -98.5 43.2 -97.8 43.3 -97.0 43.1 -96.6 42.6 -97.4 42.1 -97.8 41.2 -97.9 40.6 -98.2 40.2 -98.7 40.2 -99.4 40.7 -99.7 42.2 -98.6 40.7 -99.7</gml:posList></gml:LinearRing></gml:exterior></uswx:mcsPolygon></uswx:MesoscaleConvectiveSystemFeature></uswx:mcsFeatures></uswx:ConvectiveGuidanceForecastRecord></om:result></uswx:convectiveGuidanceForecast></uswx:ConvectiveGuidanceForecast>
'''  # noqa: E501
