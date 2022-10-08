import requests as re
from xml.dom.minidom import parseString
import csv


## Variables

# Tags in scope
retrieveTags=['TrainStatus',
'TrainLatitude',
'TrainLongitude',
'TrainCode',
'TrainDate',
'PublicMessage',
'Direction'
]


# Trains data URL
url = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML"



## Functions

# A function to get XML data in "retrieveTags" into python list and return. 
def getData(selection):

    data = []

    # iterate through contents of root tag. 
    for trainDetail in trainDetails:

        # get node of our selection i.e. each retrieveTag (called seperately by for loop.)
        Node = trainDetail.getElementsByTagName(selection).item(0)
        detail = Node.firstChild.nodeValue.strip() # Get the value of each node. 

        data.append(detail) # Append the value of each node to data list. 

    return data # return data list for each retrieveTag. 


# A function to index only train codes from defined list, append them to a list and return that list. 
def indexList(full_list):
    
    d_list = []



    for y in dCodesTrains(trainDetails): # calling dCodesTrains function i.e. getting list of indexes (positions of traincodes beginning with D.)
        d_list.append(full_list[y]) # Getting the values of train data with traincodes beginning with D. Appending to list.

    return d_list  # returning to list. 


# A function to get index of train codes that begin with "D")
def dCodesTrains(trainDetails):
    
    codeData = []

    # Iterating through XML root tag. 
    for trainDetail in trainDetails:

            # Finding node for trainCodes.
            node = trainDetail.getElementsByTagName("TrainCode").item(0)
            trainCode = node.firstChild.nodeValue.strip() # Getting value of trainCode node.

            codeData.append(trainCode) # Appending all to list.

    index = []

    for i in codeData:
        if i.startswith("D") == True: # if trainCode starts with D,
            index.append(codeData.index(i)) # Append the index of that train to index list. 

    return index # return index.




## Main body code

# request to get data from url. 
page = re.get(url)


# parsing xml content into variable. Doc will be called for each specific retrieveTag later. 
doc = parseString(page.content)

# Test to see if data is read in - commented out.
#print (doc.toprettyxml(), end = " ")


# Writing full XML data to file as backup. 
with open("trainxml.xml","w") as xmlfp:
    doc.writexml(xmlfp)


# Getting root data for trains.
trainDetails = doc.getElementsByTagName("objTrainPositions")


# Writing indexed trains to CSV. 
with open("train_data.csv", "w", newline = '') as f:

    # creating variable for csv writer. 
    writer = csv.writer(f)

    # Getting train data for specific tags in variable. 
    for i in retrieveTags:
        
        # Getting details for all trains. Calling getData function - variable is each retrieveTag. 
        fullData = getData(i)
        
        # Getting details for trains with train code beginning with D. Calling indexList function. Calling in result from each getData result. 
        d_Data = indexList(fullData)

        # Writing rows of lists to CSV file. 
        writer.writerow(d_Data)

    