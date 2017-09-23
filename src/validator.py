"""@package validator
validator - geofencing validator module,
validates the latitude and longitude is exactly correct

date Sep 21, 2017
version 1.0
"""

from .logger import LOGGER
from .settings import RESULT_LABEL, VALIDATION_METHOD, THRESHOLDS,\
    REQUST_COUNT

import geocoder
import csv
import sys
import os


class Validator(object):
    """docstring for Validator
    Class for validating the latitude and longitude is exactly correct
    """

    def __init__(self, input_file, output_file):
        """The Validator constructor
        Initialize super class and all needed fields

        @param self The Validator object pointer;
        @param input_file Source csv file name;
        @param output_file Result csv file name.
        """
        super(Validator, self).__init__()
        self._input_file = input_file
        self._output_file = output_file

        LOGGER.info("Validator successfully created")

    def _err(self, msg, exc=False, exit=True):
        """The Validator err private method
        Reports an error message and exit.

        @param self The Validator object pointer;
        @param msg An error message;
        @param exc If Exception occurs;
        @param exit Flag to exit.
        """
        LOGGER.error(msg)
        if exc:
            LOGGER.debug("Exception:", exc_info=True)
        if exit:
            sys.exit(msg)

    def _request_geocoding(self, location, reverse=False):
        """The Validator request geocoding private method
        Requests geocoding by address using Google API.

        @param self The Validator object pointer;
        @param location Geo location to request;
        @param reverse Flag to do reverse geocoding request.
        """
        response = False
        geocode = None
        request_count = 0
        # This trick need, because, in some cases first request doesn't work
        while not response and request_count < REQUST_COUNT:
            if reverse:
                geocode = geocoder.google([location['latitude'],
                                           location['longitude']],
                                          method='reverse')
            else:
                geocode = geocoder.google(location['address'])
            response = geocode.ok
            request_count += 1
            if not geocode.ok:
                self._err("Got: {}, while trying to request location {}"
                          .format(geocode.json, location['address']),
                          exit=False)
        return geocode

    def _general_validation(self, geocode, location):
        """The Validator general validation private method
        General validation method - compare location lat and long
        values and got geocode with set thresholds.

        @param self The Validator object pointer;
        @param geocode The location geocode;
        @param location Location data dict [address, lat, long].
        """
        try:
            # Calculate difference between lats and longs
            ne_lat_diff = abs(
                geocode.bbox['northeast'][0] - location['latitude'])
            sw_lat_diff = abs(
                location['latitude'] - geocode.bbox['southwest'][0])
            ne_long_diff = abs(
                geocode.bbox['northeast'][1] - location['longitude'])
            sw_long_diff = abs(
                location['longitude'] - geocode.bbox['southwest'][1])

            if ((ne_lat_diff < THRESHOLDS['correct'] > sw_lat_diff) and
                (ne_long_diff < THRESHOLDS['correct'] > sw_long_diff)):
                return 'exactly correct'
            elif ((ne_lat_diff < THRESHOLDS['city'] > sw_lat_diff) and
                (ne_long_diff < THRESHOLDS['city'] > sw_long_diff)):
                return 'in same city'
            elif ((ne_lat_diff < THRESHOLDS['state'] > sw_lat_diff) and
                (ne_long_diff < THRESHOLDS['state'] > sw_long_diff)):
                return 'in same state/province'
            elif ((ne_lat_diff < THRESHOLDS['country'] > sw_lat_diff) and
                (ne_long_diff < THRESHOLDS['country'] > sw_long_diff)):
                return 'in same country'
            else:
                return 'totaly wrong'

        except Exception as exc:
            self._err("Got: {}, while trying to validate \"{}\" correctness"
                      .format(exc, location['address']), exit=False)
            return 'totaly wrong'

    def _accuracy_validation(self, geocode, location):
        """The Validator accuracy validation private method
        Accuracy validation method - get boundaries for every
        stage validation (city, state/province, country)
        Note: may affect the number of allowable requests.

        @param self The Validator object pointer;
        @param geocode The location geocode;
        @param location Location data dict [address, lat, long].
        """
        pass
    def _reverse_validation(self, geocode, location):
        """The Validator reverse validation private method
        Reverse validation method - get address by lat and long
        and compare (city, state/province, country)
        Note: may affect the number of allowable requests.

        @param self The Validator object pointer;
        @param geocode The location geocode;
        @param location Location data dict [address, lat, long].
        """
        pass

    def _validate_geolocation(self, location, index):
        """The Validator validate geolocation private method
        Validate address with lat and long geocode values.

        @param self The Validator object pointer;
        @param location Location data dict [address, lat, long];
        @param index Input file row index.
        """
        validation_result = 'totaly wrong'
        try:
            # request geocode of address
            geocode = self._request_geocoding(location)

            if VALIDATION_METHOD == 'general':
                validation_result = self._general_validation(geocode,
                                                             location)
            elif VALIDATION_METHOD == 'accuracy':
                validation_result = self._accuracy_validation(geocode,
                                                              location)
            elif VALIDATION_METHOD == 'accuracy':
                validation_result = self._reverse_validation(geocode,
                                                             location)
            else:
                self._err(
                "Got unsupported validation method: \"{}\""
                .format(VALIDATION_METHOD))

        except Exception as exc:
            self._err(
                "Got an error:\"{}\", while trying to request location: \"{}\""
                .format(exc, location['address']), exc=True, exit=False)
            return validation_result
        else:
            return validation_result

    """ Interface methods """

    def process(self):
        """The Validator process public method
        Process input csv file and validate addresses.

        @param self The Validator object pointer.
        """
        if not os.path.exists(self._input_file):
            self._err("Input file \"{}\" does not exist"
                      .format(self._input_file))

        try:
            # Read input csv file
            with open(self._input_file, 'r') as in_csv:
                reader = csv.DictReader(in_csv)

                # Open output file for writing
                with open(self._output_file, 'w') as out_file:
                    fieldnames = reader.fieldnames + [RESULT_LABEL]
                    writer = csv.DictWriter(out_file,
                                            fieldnames,
                                            quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    # process all rows in sequence and
                    # write result to the output file
                    for idx, row in enumerate(reader):
                        # Skipp comments
                        if '#' in row[fieldnames[0]]:
                            LOGGER.debug(
                                "Row [{}], contains comment was skipped"
                                .format(idx))
                            continue
                        row['latitude'] = float(row['latitude'])
                        row['longitude'] = float(row['longitude'])
                        row[RESULT_LABEL] = self._validate_geolocation(row,
                                                                       idx)
                        # Write geocode with result row to output file
                        writer.writerow(row)

        except IOError as ioe:
            self._err(
                "Got an error:\"{}\", while trying to read input file: \"{}\""
                .format(ioe, self._input_file), exc=True)
        except Exception as exc:
            self._err(
                "Got an error:\"{}\", while trying to process file: \"{}\""
                .format(exc, self._input_file), exc=True)
