from __future__ import annotations

import logging
import re
from typing import Any, Dict, Mapping, Optional

from ngitws.logging import extra_fields
from ngitws.time import DateTimeConverter
from ngitws.typing import JsonObject
import pendulum


# These fields map to the output of this url:
# https://madis-data.ncep.noaa.gov/madisPublic1/cgi-bin/madisXmlPublicDir?rdr=&time=
# ${chr}&minbck=0&minfwd=0&recwin=0&dfltrsel=2&state=&latll=0.0&lonll=0.0&latur=90.0
# &lonur=0.0&stanam=&stasel=0&pvdrsel=1&varsel=1&qcsel=1&xml=3&csvmiss=0&nvars=TD
# &nvars=ALTSE&nvars=SLP&nvars=T&nvars=DD&nvars=FF&nvars=VIS&nvars=ELEV&nvars=LAT
# &nvars=LON&nvars=PCP1H&nvars=PCP3H&nvars=PCP6H&nvars=SKYCVLB&nvars=FFGUST
# &nvars=PRESWEA&nvars=SKYCOV&nvars=STALOC&nvars=T24MINT&nvars=T24MAXT&nvars=RAWMTR
#
# Where the first five fields are fixed regardless of parameters.
# The additional variables such as nvars=ALTSE are placed in the output CSV in the order
# they are in the url.  QC values immediately follow the variable
# Variable definitions are here: https://madis.ncep.noaa.gov/sfc_mesonet_variable_list.shtml
# QC definitions are here: https://madis.ncep.noaa.gov/madis_sfc_qc.shtml
# Generate a test url with this tool: https://madis-data.ncep.noaa.gov/public/sfcdumpguest.html
VAR_INDEX_MAP = {
    0: 'stationId',
    1: 'monthDayYear',
    2: 'hoursMinutes',
    3: 'dataProvider',
    4: 'subProvider',
    5: 'dewpoint',
    6: 'dewpoint_qc',
    7: 'altimeter',
    8: 'altimeter_qc',
    9: 'seaLevelPressure',
    10: 'seaLevelPressure_qc',
    11: 'temperature',
    12: 'temperature_qc',
    13: 'windDir',
    14: 'windDir_qc',
    15: 'windSpeed',
    16: 'windSpeed_qc',
    17: 'visibility',
    18: 'visibility_qc',
    19: 'elevation',
    20: 'elevation_qc',
    21: 'latitude',
    22: 'latitude_qc',  # not used
    23: 'longitude',
    24: 'longitude_qc',  # not used
    25: 'precipitationLastHour',
    26: 'precipitationLastHour_qc',
    27: 'precipitationLast3Hours',
    28: 'precipitationLast3Hours_qc',
    29: 'precipitationLast6Hours',
    30: 'precipitationLast6Hours_qc',
    31: 'windGust',
    32: 'windGust_qc',
    33: 'maxTemp24Hour',
    34: 'maxTemp24Hour_qc',
    35: 'minTemp24Hour',
    36: 'minTemp24Hour_qc',
    # A qc value exists for each of these but we don't use them. Current output sets qc to null.
    # There is no way to compute a single qc from six inputs.qc index is +1 of the value index
    37: 'skyLayerBase_1',
    39: 'skyLayerBase_2',
    41: 'skyLayerBase_3',
    43: 'skyLayerBase_4',
    45: 'skyLayerBase_5',
    47: 'skyLayerBase_6',
    # According to Kevin, probably no qc for this variable
    49: 'presentWeather',
    50: 'skyCover_1',
    51: 'skyCover_2',
    52: 'skyCover_3',
    53: 'skyCover_4',
    54: 'skyCover_5',
    55: 'skyCover_6',
    56: 'rawMessage'
}


class InvalidMadisCsvLineError(RuntimeError):
    """MADIS CSV line is malformed."""


class MadisObservationGenerator:
    """Metadata extractor for MADIS CSV products."""

    MISSING_VALUES_PATTERN = re.compile(r'^-99999.000000|999999.000000|^\s*$')

    # If METAR data providers are added to the madis-csv-pull script, they must also be added here to prevent METAR
    # observations from being misclassified as MESONET.
    METAR_DATA_PROVIDERS = ['ASOS', 'OTHER-MTR', 'NonFedAWOS']

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def create_observation(self, madis_csv: str) -> MadisObservation:
        obs_values: Dict[str, Any] = {}
        csv_values = madis_csv.split(',')
        # There should really be 57 variables here, but for some reason we seem to be getting an extra consistently
        if len(csv_values) not in (57, 58):
            self.__logger.warning(f'CSV input has: {len(csv_values)} columns, 57 or 58 expected')

        for i, value in enumerate(csv_values):
            # Discard values in the input that have no associated key in the varIndexMap
            if i in VAR_INDEX_MAP:
                # Filter missing values indicated by -9999 and white space; set the output value to None
                if not self.MISSING_VALUES_PATTERN.match(value):
                    obs_values[VAR_INDEX_MAP[i]] = value.strip()
                else:
                    obs_values[VAR_INDEX_MAP[i]] = None

        station_id = obs_values.get('stationId')
        if not station_id:
            raise InvalidMadisCsvLineError(f'MADIS observation has no station ID: {madis_csv}')

        with extra_fields({'station_id': station_id}):
            if 'monthDayYear' not in obs_values or 'hoursMinutes' not in obs_values:
                raise InvalidMadisCsvLineError(
                    f'MADIS observation from {station_id} has missing observation time fields: {madis_csv}'
                )

            # Each record must have a data provider, latitude, longitude, and elevation or it will be skipped.
            # This protects against records that may be in the process of qc and not all the values are present,
            # but will have them in a subsequent data pull.
            data_provider = obs_values.get('dataProvider')
            if data_provider is None:
                raise InvalidMadisCsvLineError(
                    f'MADIS observation from {station_id} has missing data provider: {madis_csv}'
                )
            if obs_values.get('latitude') is None:
                raise InvalidMadisCsvLineError(
                    f'MADIS observation from {station_id} has missing latitude: {madis_csv}'
                )
            if obs_values.get('longitude') is None:
                raise InvalidMadisCsvLineError(
                    f'MADIS observation from {station_id} has missing longitude: {madis_csv}'
                )
            if obs_values.get('elevation') is None:
                raise InvalidMadisCsvLineError(
                    f'MADIS observation from {station_id} has missing elevation: {madis_csv}'
                )

            try:
                # See note for METAR_DATA_PROVIDERS above about adding additional MADIS data providers.
                if data_provider in self.METAR_DATA_PROVIDERS:
                    return MetarObservation(obs_values)
                if data_provider == 'MARITIME':
                    return MaritimeObservation(obs_values)
                return MesonetObservation(obs_values)
            except Exception as ex:
                raise InvalidMadisCsvLineError(f'Failed to parse MADIS observation ({str(ex)}: {madis_csv}', ex)


class MadisObservation:

    FEED: str

    def as_dict(self) -> JsonObject:
        return {
            'feed': self.FEED,
            'timestamp': DateTimeConverter().write_as_string(self.__timestamp),
            'observationTime': int(self.__timestamp.format('x')),
            'stationId': self.__stationId,
            'geometry': {
                'type': 'Point',
                'coordinates': [self.__longitude, self.__latitude]
            },
            'dataProvider': self.__dataProvider,
            'subProvider': self.__subProvider,
            'dewpoint': self.__dewpoint.as_dict(),
            'elevation': self.__elevation.as_dict(),
            'seaLevelPressure': self.__seaLevelPressure.as_dict(),
            'altimeter': self.__altimeter.as_dict(),
            'temperature': self.__temperature.as_dict(),
            'windDir': self.__windDir.as_dict(),
            'windSpeed': self.__windSpeed.as_dict(),
            'windGust': self.__windGust.as_dict(),
            'visibility': self.__visibility.as_dict(),
            'presentWeather': self.__presentWeather
        }

    def __init__(self, obs_values: Mapping[str, str]):
        self.__dataProvider = obs_values.get('dataProvider')
        self.__subProvider = obs_values.get('subProvider')
        self.__stationId = obs_values.get('stationId')

        self.__logger = logging.getLogger(__name__)

        obs_time = f'{obs_values.get("monthDayYear")} {obs_values.get("hoursMinutes")}'
        try:
            self.__timestamp = pendulum.from_format(obs_time, 'MM/DD/YYYY HH:mm', tz='UTC')
        except Exception as ex:
            month_day_year = obs_values.get('monthDayYear')
            hours_minutes = obs_values.get('hoursMinutes')
            raise RuntimeError(
                f'Cannot parse observation time "{month_day_year} {hours_minutes}": {str(ex)}',
                ex
            )

        self.__dewpoint = MadisVariable(
            self._convert_float(obs_values.get('dewpoint')),
            'kelvin',
            obs_values.get('dewpoint_qc')
        )
        self.__elevation = MadisVariable(
            self._convert_float(obs_values.get('elevation')),
            'meter',
            obs_values.get('elevation_qc')
        )
        self.__seaLevelPressure = MadisVariable(
            self._convert_float(obs_values.get('seaLevelPressure')),
            'pascal',
            obs_values.get('seaLevelPressure_qc')
        )
        self.__altimeter = MadisVariable(
            self._convert_float(obs_values.get('altimeter')),
            'pascal',
            obs_values.get('altimeter_qc')
        )
        self.__longitude = self._convert_float(obs_values.get('longitude'))
        self.__latitude = self._convert_float(obs_values.get('latitude'))
        self.__temperature = MadisVariable(
            self._convert_float(obs_values.get('temperature')),
            'kelvin',
            obs_values.get('temperature_qc')
        )
        self.__windDir = MadisVariable(
            self._convert_float(obs_values.get('windDir')),
            'degree',
            obs_values.get('windDir_qc')
        )
        self.__windSpeed = MadisVariable(
            self._convert_float(obs_values.get('windSpeed')),
            'meter/sec',
            obs_values.get('windSpeed_qc')
        )
        self.__windGust = MadisVariable(
            self._convert_float(obs_values.get('windGust')),
            'meter/sec',
            obs_values.get('windGust_qc')
        )
        self.__visibility = MadisVariable(
            self._convert_float(obs_values.get('visibility')),
            'meter',
            obs_values.get('visibility_qc')
        )
        self.__presentWeather = obs_values.get('presentWeather')

    @staticmethod
    def _convert_float(value: Optional[str]) -> Optional[float]:
        if value is None:
            return None
        return round(float(value), 2)


class MaritimeObservation(MadisObservation):

    FEED = 'MADIS_MARITIME'

    def __init__(self, obs_values: Mapping[str, str]):
        super().__init__(obs_values)

        self.__precipitation_last_hour = MadisVariable(
            self._convert_float(obs_values.get('precipitationLastHour')),
            'meter',
            obs_values.get('precipitationLastHour_qc')
        )
        self.__precipitation_last_6_hours = MadisVariable(
            self._convert_float(obs_values.get('precipitationLast6Hours')),
            'meter',
            obs_values.get('precipitationLast6Hours_qc')
        )

    def as_dict(self) -> JsonObject:
        return {**super().as_dict(), **{
            'precipitationLastHour': self.__precipitation_last_hour.as_dict(),
            'precipitationLast6Hours': self.__precipitation_last_6_hours.as_dict()
        }}


class MesonetObservation(MadisObservation):

    FEED = 'MADIS_MESONET'

    def __init__(self, obs_values: Mapping[str, str]):
        super().__init__(obs_values)

        self.__max_temp_24_hours = MadisVariable(
            self._convert_float(obs_values.get('maxTemp24Hour')),
            'kelvin',
            obs_values.get('maxTemp24Hour_qc')
        )
        self.__min_temp_24_hours = MadisVariable(
            self._convert_float(obs_values.get('minTemp24Hour')),
            'kelvin',
            obs_values.get('minTemp24Hour_qc')
        )
        self.__precipitation_last_3_hours = MadisVariable(
            self._convert_float(obs_values.get('precipitationLast3Hours')),
            'meter',
            obs_values.get('precipitationLast3Hours_qc')
        )
        self.__sky_cover = [obs_values.get(f'skyCover_{i}') for i in range(1, 7)]
        self.__sky_layer_base = [self._convert_float(obs_values.get(f'skyLayerBase_{i}')) for i in range(1, 7)]

    def as_dict(self) -> JsonObject:
        return {**super().as_dict(), **{
            'maxTemp24Hour': self.__max_temp_24_hours.as_dict(),
            'minTemp24Hour': self.__min_temp_24_hours.as_dict(),
            'precipitationLast3Hours': self.__precipitation_last_3_hours.as_dict(),
            'skyCover': self.__sky_cover,
            'skyLayerBase': self.__sky_layer_base,
            'skyLayerBaseUnit': 'meter'
        }}


class MetarObservation(MadisObservation):

    FEED = 'MADIS_METAR'

    def __init__(self, obs_values: Mapping[str, str]):
        super().__init__(obs_values)

        self.__max_temp_24_hour = MadisVariable(
            self._convert_float(obs_values.get('maxTemp24Hour')),
            'kelvin',
            obs_values.get('maxTemp24Hour_qc')
        )
        self.__min_temp_24_hour = MadisVariable(
            self._convert_float(obs_values.get('minTemp24Hour')),
            'kelvin',
            obs_values.get('minTemp24Hour_qc')
        )
        self.__precipitation_last_hour = MadisVariable(
            self._convert_float(obs_values.get('precipitationLastHour')),
            'meter',
            obs_values.get('precipitationLastHour_qc')
        )
        self.__precipitation_last_3_hours = MadisVariable(
            self._convert_float(obs_values.get('precipitationLast3Hours')),
            'meter',
            obs_values.get('precipitationLast3Hours_qc')
        )
        self.__precipitation_last_6_hours = MadisVariable(
            self._convert_float(obs_values.get('precipitationLast6Hours')),
            'meter',
            obs_values.get('precipitationLast6Hours_qc')
        )
        self.__raw_message = obs_values.get('rawMessage')
        self.__sky_cover = [obs_values.get(f'skyCover_{i}') for i in range(1, 7)]
        self.__sky_layer_base = [self._convert_float(obs_values.get(f'skyLayerBase_{i}')) for i in range(1, 7)]

    def as_dict(self) -> JsonObject:
        return {**super().as_dict(), **{
            'rawMessage': self.__raw_message,
            'maxTemp24Hour': self.__max_temp_24_hour.as_dict(),
            'minTemp24Hour': self.__min_temp_24_hour.as_dict(),
            'precipitationLastHour': self.__precipitation_last_hour.as_dict(),
            'precipitationLast3Hours': self.__precipitation_last_3_hours.as_dict(),
            'precipitationLast6Hours': self.__precipitation_last_6_hours.as_dict(),
            'skyCover': self.__sky_cover,
            'skyLayerBase': self.__sky_layer_base,
            'skyLayerBaseUnit': 'meter'
        }}


class MadisVariable:

    def __init__(self, value: Any, unit: str, qc: Optional[str]):
        self.__value = value
        self.__unit = unit
        self.__qc = qc

    def as_dict(self) -> JsonObject:
        return {
            'value': self.__value,
            'unit': self.__unit,
            'qc': self.__qc
        }
