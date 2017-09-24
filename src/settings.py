"""@package settings
settings - module contains all geofencing configurable options
This module contains all the configurable options of the geofencing validator tool.

date Sep 23, 2017
version 1.0

Copyright (c) 2017 Topcoder Inc. All Rights Reserved.
"""

# The path to the tool log file
LOG_FILE = 'log/geofencing_validator.log'

# The log level value
LOG_LEVEL = 'INFO'

# The label for the validation result
RESULT_LABEL = 'validation_result'

# Result values
# Note: if changed will affect to results in output file
RESULT_VALUES = ('exactly correct',
                 'in same city',
                 'in same state/province',
                 'in same country',
                 'totaly wrong')

""" 
 Value to use one of supported validation methods
 Supported methods: general, accuracy, reverse
 Note: accuracy may affect the number of allowable requests
 because this method uses additional requests for city, state/province and country
"""
VALIDATION_METHOD = 'general'

# Number of requests for one address if previous was failed
# This trick was added, because in some cases, first request failed
REQUST_COUNT = 5

# Timeout before next try
REQUEST_TIMEOUT = 5

"""
Thresholds used to validate whether certain latitude and longitude points
are really in a certain city or state as designated by an address

Thresholds set the maximum value of difference between given
latitude and longitude points and requestred address latitude and longitude

Latitude coordinate precision by the actual cartographic scale they purport:

tens digit      1000 kilometers     620 miles
units digit     100 kilometers      62 miles

Decimal Places   Aprox. Distance    Say What?
1                10 kilometers      6.2 miles
2                1 kilometer        0.62 miles
3                100 meters         About 328 feet
4                10 meters          About 33 feet
5                1 meter            About 3 feet
6                10 centimeters     About 4 inches
7                1.0 centimeter     About 1/2 an inch
8                1.0 millimeter     The width of paperclip wire.

Note: thresholds used only by general validation method
"""
THRESHOLDS = {
    'correct': 1E-2,    # Matching tolerance for exactly correct
    'city': 0.1,        # Matching tolerance for in same city
    'state': 4,         # Matching tolerance for in same state/province
    'country': 35       # Matching tolerance for in same country
}

# Tolerance thresholds set the tolerance for correct and city values
# comparison city vlue only for accuracy validation method
# correct for both accuracy and reverse methods
TOLERANCE = {
    'correct': 5E-3,    # Tolerance to extend boundary for exactly correct
    'city': 2E-2        # Tolerance to extend boundary for in same city
}