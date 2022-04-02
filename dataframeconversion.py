import json
import pandas as pd
import streamlit as st

@st.cache()
def convertToDataFrame(addressType,address, arrPOI, distMatrix, mode):
    apiJson = json.loads(distMatrix)
    
    #create lists for columns to be populated
    colAddressType = []
    colAddr = []
    colPOIName = []
    colPOIAddress = []
    colDestDist_Meter = []
    colDestDuration_Sec = []
    colMode = []

    #loop through each POI destination found
    for i, poiAddress in enumerate(apiJson["destination_addresses"]):
        colAddressType.append(addressType)
        colMode.append(mode)
        colAddr.append(apiJson["origin_addresses"][0])
        colPOIName.append(arrPOI[i])
        colPOIAddress.append(poiAddress)

    #loop through each distance matrix result
    for poi in apiJson["rows"][0]["elements"]:
        colDestDist_Meter.append(poi['distance']['value'])
        colDestDuration_Sec.append(poi['duration']['value'])

    data = {
            'Address Type': addressType,
            'Address': colAddr,
            'POI': colPOIName,
            'POI Address': colPOIAddress,
            'Mode': colMode,
            'Distance (m)': colDestDist_Meter,
            'Duration (s)': colDestDuration_Sec
            }

    print(data)
    
    df = pd.DataFrame(data)
    
    return df

