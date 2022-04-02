import streamlit as st
import pandas as pd
import altair as alt
import addressfinder as addrfinder
import pointofinterest as poi
import distances as dist
import dataframeconversion as dfConv

st.set_page_config(
    page_title = "Locompare",
    page_icon="📍",
    layout="wide"
)

st.title("📍 LOCOMPARE")
st.subheader("**Compare 2 addresses to see which one is better for your points of interest.**")
#inputCol, resultsCol = st.columns(2)

def render_chart(df):   
    duration = alt.Chart(df).mark_bar(size=15).encode(
        x = alt.X("Duration (min):Q", title="Minutes Away"),
        y = "Address:O",
        row = "Mode:O",
        color = alt.Color("POI",title="Point Of Interest")
    ).properties(width=800
    ).configure_view(
        strokeWidth=0
    )

    #distance = alt.Chart(df).mark_bar(size=15).encode(
    #    x = alt.X("Distance (mi):Q", title="Miles Away"),
    #    y = "Address:O",
    #    row = "Mode:O",
    #    color = alt.Color("POI",title="Point Of Interest")
    #).properties(width=800
    #).configure_view(
    #    strokeWidth=0
    #)

    st.altair_chart(duration)
    #st.altair_chart(distance)

#df = pd.read_csv('results.csv')
#df["Duration (min)"] = df["Duration (s)"]/60
# meters to km to miles
#df["Distance (mi)"] = (df["Distance (m)"]/1000)*0.621371
#df
#render_chart(df)

with st.form(key="userInputForm"):
    st.write("**Step 1: Enter 2 addresses to compare**")
    step1WarningMsg = st.empty()
    addr1, addr2 = st.columns(2)
    with addr1:
        addr1 = st.text_input("Enter the first address you want to compare", placeholder="Ex: Current living address", key="addr1")
    with addr2:
        addr2 = st.text_input("Enter the second address you want to compare", placeholder="Ex: New living address", key="addr2")
        #st.sidebar.text_input("Enter the second address you want to compare", placeholder="Potential new living address")
    st.write("---")
    st.write("**Step 2: Enter up to 3 points of interest you care about**")
    step2WarningMsg = st.empty()
    poiInput1, poiInput2, poiInput3, poiInput4, poiInput5 = st.columns(5)
    with poiInput1:
        poiInput1Txt = st.text_input("1st point of interest", placeholder="ex: Starbucks, Target, lake").strip()
    with poiInput2:
        poiInput2Txt = st.text_input("2nd point of interest", placeholder="optional").strip()
    with poiInput3: 
        poiInput3Txt = st.text_input("3rd point of interest", placeholder="optional").strip()
    with poiInput4: 
        poiInput4Txt = st.text_input("4th point of interest", placeholder="optional").strip()
    with poiInput5: 
        poiInput5Txt = st.text_input("5th point of interest", placeholder="optional").strip()

    st.write("**Step 3: Enter your preferred transport mode**")
    mode = str(st.selectbox("Pick one", ['driving','walking', 'bicycling']))
    submitBtn = st.form_submit_button("Compare")

if submitBtn:
    if not addr1 or not addr2:
        step1WarningMsg.error("Please enter 2 addresses to compare for **Step 1**.")
        st.stop()
    elif not poiInput1Txt.strip():
        step2WarningMsg.error("Please enter at least 1 point of interest for **Step 2**.")
        st.stop()

    with st.spinner("Crunching Numbers"):
        livingAddress1 = addrfinder.getInputAddress(addr1)
        livingAddress2 = addrfinder.getInputAddress(addr2)
    
        if not livingAddress1: 
            st.error(f"We did not find anything for {addr1}.. please try re-entering it.")
            st.stop()
        elif not livingAddress2: 
            st.error(f"We did not find anything for {addr2}.. please try re-entering it.")
            st.stop()
        
        arrPOI = [poiInput1Txt]
        if poiInput2Txt and (poiInput2Txt not in arrPOI):
            arrPOI.append(poiInput2Txt)
        if poiInput3Txt and (poiInput3Txt not in arrPOI):
            arrPOI.append(poiInput3Txt)
        if poiInput4Txt and (poiInput4Txt not in arrPOI):
            arrPOI.append(poiInput4Txt)
        if poiInput5Txt and (poiInput5Txt not in arrPOI):
            arrPOI.append(poiInput5Txt)
        
        address1WithPOI = poi.searchForPOI(livingAddress1, arrPOI)
        address2WithPOI = poi.searchForPOI(livingAddress2, arrPOI)
        
        if(not address1WithPOI or not address2WithPOI):
            st.error("We did not find valid points of interest... please enter new ones.")
            st.stop()
        
        livingAddrArr = [livingAddress1, livingAddress2] 
        addressWithPOIArr = [address1WithPOI,address2WithPOI]

        distArr = []
        
        def callDistApi(livingAddrArr,addressWithPOIArr,mode):
            distArr.append(dist.getDistanceMatrix(livingAddrArr, addressWithPOIArr, mode))

        for i, addr in enumerate(livingAddrArr):        
                callDistApi(livingAddrArr[i], addressWithPOIArr[i], mode)

        resultMsg = st.empty()
        
        st.write(livingAddress1)
        st.write(arrPOI)
        st.write(distArr[0])
        st.write(mode)
        
        dfAddr1Results = dfConv.convertToDataFrame('current',livingAddress1, arrPOI, distArr[0], mode)
        dfAddr2Results = dfConv.convertToDataFrame('new',livingAddress2, arrPOI, distArr[1], mode)

        #union two result dfs
        df = pd.concat([dfAddr1Results, dfAddr2Results])
        #sec to mins
        df["Duration (min)"] = df["Duration (s)"]/60
        # meters to km to miles
        df["Distance (mi)"] = (df["Distance (m)"]/1000)*0.621371
        #finalDf.to_csv('results.csv')
        df = df[["Address","POI","POI Address", "Mode", "Duration (min)","Distance (mi)"]]

        st.write(df)
        render_chart(df)
        dfGroupBy = df.groupby(["Address"], as_index=False).sum()
        dfMinAddr = dfGroupBy[dfGroupBy["Duration (min)"] == dfGroupBy["Duration (min)"].min()]
        betterAddr = str(dfMinAddr['Address'].iloc[0])
        resultMsg.success(f"Here's what I found: **{betterAddr} is better.**")
            
    #rec1["Duration (min)"].min("Duration (min)")
    #st.write(rec2[rec1["Duration (min)"]=="Duration (min)"])
    
