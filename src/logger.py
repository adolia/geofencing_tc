"""@package Logger
Logger - package for adress geodata validation logging

date Sep 21, 2017
version 1.0
"""
import logging

# See: "Configuring Logging for a Library" in python standard logging howto,
# e.g. https://docs.python.org/2/howto/logging.html#library-config.
LOGGER = logging.getLogger("geofencing_validator")
LOGGER.addHandler(logging.NullHandler())

def set_loglevel(level):
    """Set Logger Level function
    @param level: Log level, e.g. logging.INFO and logging.WARN.
    """
    LOGGER.setLevel(level)

def create_logger(log_file, log_level):
    """ Function for creating logger

    @param log_file Log file name;
    @param log_level Log level, e.g. INFO and WARN.
    """
    logging.basicConfig(filename = log_file,
                        level = logging.INFO,
                        format = "%(asctime)s [pid=%(process)d] [%(levelname)s] %(message)s",
                        datefmt='%a %d %b %H:%M:%S %Y')

    num_lvl = getattr(logging, log_level.upper(), None)
    set_loglevel(num_lvl)

    return LOGGER