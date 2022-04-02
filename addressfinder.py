from geopy.geocoders import Nominatim
import streamlit as st

@st.cache(allow_output_mutation=True)
def getInputAddress(inputAddress):
    noValidAddress = True
    global location
    location = ""
    
    # find lat/long of entered addresses
    locator = Nominatim(user_agent=st.secrets["user_agent"])
    location = locator.geocode(inputAddress)

    return location