<h2>Sima XML parser</h2>

<h3>Installation</h3>
`pip install -r requirements.txt`

<h3>Start</h3>
`python main.py`

<h3>Functionality</h3>
This service:
- downloads a large xml file from the source
- performs preprocessing using Linux egrep (optimal option in terms of resources)
- saves results to cache
- writes the results that are not in the cache at the time of launch to the output XLS file

<h3>Stack</h3>
- XlsxWriter
- pymongo (for cache)
