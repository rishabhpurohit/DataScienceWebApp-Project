import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
data_url = (
r"C:\Users\Purohit\Desktop\WebApp Project\Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in NYC")
st.markdown("This app is a Streamlit dashboard that can be used to analyze motor vehicle collisions")

st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(data_url, nrows =nrows , parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'])
    lowercase= lambda x: str(x).lower()
    data.rename(lowercase,axis='columns',inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data

data = load_data(100000)


st.header("Where are the most number of people injured in NYC?")
injured_people = st.slider("Numbaer of persons injured in vehicle collisions",0,19)
st.map(data.query("injured_persons >= @injured_people")[['latitude','longitude']].dropna(how="any"))


st.header("How many collisions occured in a given time  of a day?")
hour = st.slider("Hour to look at",0,23)
data = data[data['date/time'].dt.hour ==hour]


st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour,(hour+1) % 24))
midpoint = (np.average(data['latitude']),np.average(data['longitude']))
cols = ['date/time','latitude','longitude']

st.write(pdk.Deck(
    #map_style="mapbox://styles/mapbox/light-v9",
    #initial_view_state={
        #"latitude": midpoint[0],
        #"longitude": midpoint[1],
        #"zoom":11,
        #"pitch": 50,
    #}, #streamlit run app.py
    layers = [
        pdk.Layer(
        type="HexagonLayer",
        data = data[cols],
        get_position=['longitude','latitude'],
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))




if st.checkbox("Show Raw Data",False):
    st.subheader("Raw Data")
    st.write(data)
