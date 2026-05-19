import streamlit as st
import pandas as pd
import time

SHEET_ID = "1DZVDm1ilkUGeQEJg5snnIk6cooVlOv6Nj9_FppdhEt8"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

st.title("🏥 Health Monitoring Dashboard")

placeholder = st.empty()

while True:
    df = pd.read_csv(URL)
    last = df.iloc[-1]
    
    with placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌡️ Temperature", f"{last['field1']} °C")
        with col2:
            st.metric("❤️ Heart Rate", f"{last['field2']} BPM")
        st.write("**Channel:**", last['channel'])
        st.write("**Last update:**", last['timestamp'])
    
    time.sleep(10)
    st.rerun()
