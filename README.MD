# Sima XML parser

## Installation
`pip install -r requirements.txt`

## Start
`python main.py`

## Functionality
This service:
- downloads a large xml file from the source
- performs preprocessing using Linux egrep (optimal option in terms of resources)
- saves results to cache
- writes the results that are not in the cache at the time of launch to the output XLS file

## Stack
- XlsxWriter
- pymongo (for cache)
