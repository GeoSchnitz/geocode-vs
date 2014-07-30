geocode-vs
==========

### Purpose

Getting a unified way to access the most important geocoding APIs (Nominatim, Google, MapQuest, HERE, OpenCage) to compare and evaluate.

### Usage

Just run the script by providing a .txt file with each location to geocode on a new line, e.g.:

    cat places.txt  
    Berlin  
    Amsterdam  
    Montpellier
    ...
    python geocode-vs.py places.txt
  
The script will access `API.json` for API keys (if neccessary) and will output `cities.csv` as well as `outliers.txt`. Don't forget to update your `API.json` to get access to the MapQuest, HERE and OpenCage geocoding results. The `outliers.txt` is some kind of shoot from the hip for evaluating the quality of the data. Outliers will be summarized in the console and simply mean that the coordinates for a location are not within the standard deviation of all 5 providers. This is by no means a real measure for quality, just a hint or a reminder to implement some real quality measurement.

### Files

`API.json` - credentials for the geocoding APIs  
`cities.csv` - main output; CSV with header; example results included  
`cities.txt` - input file; each location on new line; examples included  
`console_output.txt` - example for console output  
`outliers.txt` - supposed outliers   

### Version

* querying APIs works
* generating a CSV works
* getting (somewhat questionable) descriptive statistics works

ToDo:
* well-thought quality control
* optimized output
* arguments, e.g. choice of providers
* error/exception handling
* simplification/refactoring

