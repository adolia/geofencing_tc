# GEOFENCING VALIDATION Tool Deployment and Verification Guide

### Description
In this challenge we developed a tool to validate whether certain latitude and longitude points, given from csv file, are really in a certain city or state as designated by an address, given from csv file too.

## Prerequisites
* Python 3.6.2
* requests==2.18.4
* geocoder==1.32.1

## Local Deployment
### Python dependencies
The application has been developed and tested with `Python 3.6.2`.
All the dependencies could be solved by typing the following command under root directory of this submission:

```
$ pip3 install -r requirements.txt
```
Ensure that there’s no error for each python dependency.

### Options
All the configurable options are located in the file `src/settings.py`.
Here is a brief introduction on these parameters.

* `LOG_FILE` The path to the logging file. The default value is `log/geofencing_validator.log`.
* `LOG_LEVEL` The tool logging level value. The default value is `INFO`.
* `RESULT_LABEL` The label for the validation result. The default value is `validation_result`.
* `RESULT_VALUES` Predefined result values list. The default options is `['exactly correct', 'in same city', 'in same state/province', 'in same country', 'totaly wrong']`.
Note: if changed will affect to results in output file.
* `REQUEST_COUNT` Number of requests for one address if previous was failed. Default value is `5`.
This trick was added, because in some cases, first request was failed.
* `REQUEST_TIMEOUT` Timeout before next try in case of failed request. The default value is `5` seconds.
* `VALIDATION_METHOD` Value to use one of supported validation methods. Supported methods are `['general', 'accuracy', 'reverse']`. The dafault value is `'general'`.
* `THRESHOLDS` The thresholds dictionary with values to compare latitide and longitude. Thresholds used to validate whether certain latitude and longitude points are really in a certain boundary.
Note: Used only by 'general' validation method.
* `TOLERANCE` The tolerance dictionary with values to accurate region of interest. Tolerance used to clarify region of interest for current boundary.
Note: Used by 'accuracy' and 'reverse' validation methods.

Note: that you can to adjust the `VALIDATION_METHOD`, `THRESHOLDS` and `TOLERANCE` in `settings.py` properly to make the tool more accurate for result calculation.

For more datails check [Validation description](#documentation)

## Production Build and Installation
### Usage
```
./geofencing_validator.py -i|--input=<input csv file> -o|--output=<output csv file>
```

To start the application execute the following command under the root directory of this submission:

```
$ python3 geofencing_validator.py -i ./samples/location-for-dev.csv  -o ./samples/output_general.csv
```
## Verification

* After application was finished, check if there are no errors in console and in log file.
* If succes, you can see `input.csv file successfully procesed, results was saved to output.csv` message in the log file.
* Than check if the results were saved to the output file.
* You can try to use different validation methods and adjust thresholds properly to improve result accuracy.

## Documentation
### Validation methods description
* `General method` - the simpliest method, which is only request address geo location
  and than calculate extended location range, using threshold values (THRESHOLDS), compares given from file
  latitude and longitude values with extended range and checks if this point lies in address boundary.
  For example:
  ```
  (location.latitude - THRESHOLDS['correct']) < latitude < (location.latitude + THRESHOLDS['correct'])
  (location.longitude - THRESHOLDS['correct']) < longitude < (location.longitude + THRESHOLDS['correct'])
  ```
  It processes values in a sequence from correct to totaly wrong result.
* `Accuracy method` - this method is used to determine if given latitude and longitude point is
  located in the boundary, with some extention for correct and city results (Tolerance), of address.
    For example:
  ```
  (location['southwest'].latitude - TOLERANCE['correct']) < latitude < (location['northeast'].latitude + TOLERANCE['correct'])
  (location['southwest'].longitude - TOLERANCE['correct']) < longitude < (location['northeast'].longitude + TOLERANCE['correct'])
  ```
  It performs additional request to get boundaries for city, state and country if needed. And than check
  if given point is located in boundary.
* `Reverse method` - this method treat exactly correct results identically to the accuracy method.
  But for other results it makes additional request of reverse geocoding by given latitude and longitude
  and then checks if given and requested addresses contains the same city, state and country values.

## Thresholds description
### Preface
One degree of latitude covers about 10^7/90 = 111,111 meters. ("About," because the meter's length has changed a little bit in the meantime. But that doesn't matter.) Furthermore, a degree of longitude (east-west) is about the same or less in length than a degree of latitude, because the circles of latitude shrink down to the earth's axis as we move from the equator towards either pole. Therefore, it's always safe to figure that the sixth decimal place in one decimal degree has 111,111/10^6 = about 1/9 meter = about 4 inches of precision.

Accordingly, if your accuracy needs are, say, give or take 10 meters, than 1/9 meter is nothing: you lose essentially no accuracy by using six decimal places. If your accuracy need is sub-centimeter, then you need at least seven and probably eight decimal places, but more will do you little good.

Thirteen decimal places will pin down the location to 111,111/10^13 = about 1 angstrom, around half the thickness of a small atom.

### Help distances table
Using these ideas we can construct a table of what each digit in a decimal degree signifies:

| Decimal Places  | Aprox. Distance | Say What?                     |
|-----------------|-----------------|-------------------------------|
| tens digit      | 1000 kilometers | 620 miles                     |
| units digit     | 100 kilometers  | 62 miles                      |
| 1               | 10 kilometers   | 6.2 miles                     |
| 2               | 1 kilometer     | 0.62 miles                    |
| 3               | 100 meters      | About 328 feet                |
| 4               | 10 meters       | About 33 feet                 |
| 5               | 1 meter         | About 3 feet                  |
| 6               | 10 centimeters  | About 4 inches                |
| 7               | 1.0 centimeter  | About 1/2 an inch             |
| 8               | 1.0 millimeter  | The width of paperclip wire.  |
| 9               | 0.1 millimeter  | The width of a strand of hair.|

### Threshold values
Threshold dictionary is used only by general validation method, it containes:
* `correct` - threshold to determine whether certain latitude and longitude exactly correct
* `city` - threshold to determine whether certain latitude and longitude in same city as address
* `state` - threshold to determine whether certain latitude and longitude in same state/province as address
* `country` - threshold to determine whether certain latitude and longitude in same country as address

Toleranse dictionary is used by accuracy and reverse methods, it containes:
* `correct` - value to extend address location boundary in case of exactly correct
* `city` - value to extend address location boundary in case of address in the same city

Note: Depending on how we set this thresholds and tolerance, labels exactly correct / in same city may get swapped. If tolerance is little higher, we may get exactly correct, because we extend a range in which the latitude and longitude may be located.


## Notes
* Author: `Aleksey Dolia`
* Email: `aleksey.dolia@gmail.com`

