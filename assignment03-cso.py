# Importing relevant modules.
import requests
import urllib
import json

# Spliting the start and the end of the URL, omitting the report name so we can reuse the code. 
url_start = 'https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/'
url_end = '/JSON-stat/2.0/en'

# A function to request the data. 
def getalldata(report):
    response = requests.get(url_start+report+url_end)
    return response.json()

# A function to write the data to a json file. 
def getAllAsFile(report):
    with open("cso.json", "wt") as fp:
        print(json.dumps(getalldata(report)), file=fp)


# Running the program. 
if __name__ == "__main__":
    getAllAsFile('FIQ02')