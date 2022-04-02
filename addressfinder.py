from geopy.geocoders import Nominatim
import streamlit as st

@st.cache(hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None })
def getInputAddress(inputAddress):
    noValidAddress = True
    global location
    location = ""
    
    # find lat/long of entered addresses
    locator = Nominatim(user_agent=st.secrets["user_agent"])
    location = locator.geocode(inputAddress)

    return location
