"""@package validator
validator - geofencing validator module,
validates the latitude and longitude is exactly correct

date Sep 21, 2017
version 1.0
"""

from .logger import LOGGER

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
