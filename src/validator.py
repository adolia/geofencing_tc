"""@package validator
validator - geofencing validator module,
validates the latitude and longitude is exactly correct

date Sep 21, 2017
version 1.0
"""

from .logger import LOGGER
from .settings import RESULT_LABEL

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

    def _err(self, msg, exc=False):
        """The Validator err private method
        Reports an error message and exit.

        @param self The Validator object pointer;
        @param msg An error message;
        @param exc If Exception occurs.
        """
        LOGGER.error(msg)
        if exc:
            LOGGER.debug("Exception:", exc_info=True)
        sys.exit(msg)

    def _validate_geolocation(self, geocode, index):
        """The Validator validate geolocation private method
        Validate address with id lat and long geocode values.

        @param self The Validator object pointer;
        @param geocode Geocode data dict [address, lat, long];
        @param index Input file row index.
        """
        return 'exactly correct'

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
