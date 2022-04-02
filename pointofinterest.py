import requests
import json
import streamlit as st

# return place_id of nearest location of point of interest
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None,})
def searchForPOI(livingAddress, poi):
    global returnList 
    returnList = []
    
    coordinates = str(livingAddress.latitude) + "," + str(livingAddress.longitude)
    
    for place in poi:
        apiParams = {
            "input" : place,
            "inputtype": "textquery",
            "locationbias" : "circle:1000@"+coordinates,
            "fields" : "name,place_id,formatted_address",
            "key" : st.secrets["gcp_api_key"]
        }
        
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        response = requests.get(url, params=apiParams)
        responseDict = json.loads(response.text)
        
        if(responseDict["status"] != "OK"):
            continue
        
        returnList.append(responseDict["candidates"][0])

    return returnList
