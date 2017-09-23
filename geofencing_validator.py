#!/usr/bin/python3

"""@package geofencing_validtor
geofencing_validtor - script for validating the 
address latitude and longitude is exactly correct
date Sep 21, 2017
version 1.0
"""

from src.logger import create_logger
from src.validator import Validator
from src.settings import LOG_FILE, LOG_LEVEL

import logging
import getopt
import sys
import os

usage = """
Usage::
    ./geofencing_validator.py -i|--input=<input csv file> -o|--output=<output csv file>
"""

logger = None

def main(args):
    input_file = None
    output_file = None

    logger = create_logger(LOG_FILE, LOG_LEVEL)
    logger.info("Geofencing validator logger was created.")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input=", "output="])
    except getopt.GetoptError as exc:
        logger.error("Got an error: \"{}\", while trying to get options"
                     .format(exc))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        else:
            logger.error("Incorrect parameter was set")
            sys.exit(usage)

    if input_file and output_file:
        validator = Validator(input_file, output_file)
        validator.process()
    else:
        logger.error("No input csv file or output file path in parameter")
        sys.exit(usage)


if __name__ == "__main__":
    main(sys.argv[1:])
