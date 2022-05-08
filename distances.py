# find distance of entered address and POIs
import requests
import json
import streamlit as st

@st.cache(hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None})
def getDistanceMatrix(address, arrPOI, mode):

    arrPlaceID = []
    
    for POI in arrPOI:
        arrPlaceID.append(POI["place_id"])  
    
    apiParams = {
            "origins" : str(address.latitude) + "," + str(address.longitude),
            "destinations": "place_id:"+ "|place_id:".join(arrPlaceID),
            "mode": mode,
            "key" : st.secrets["gcp_api_key"]
        }

    # return place_id of nearest point of interest
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    response = requests.get(url, params=apiParams)

    return response.text
