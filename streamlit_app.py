import streamlit as st
import pandas as pd
import requests
import time

SHEET_ID = "1DZVDm1ilkUGeQEJg5snnIk6cooVlOv6Nj9_FppdhEt8"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

THINGSPEAK_WRITE_KEY = "G595J63730YTM3SL"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def get_alert_level(bpm, spo2):
    if bpm < 50 or bpm > 120 or spo2 < 90:
        return 2  # Critical
    elif bpm < 60 or bpm > 100 or spo2 < 95:
        return 1  # Warning
    else:
        return 0  # Normal

def send_to_thingspeak(alert_level):
    params = {
        "api_key": THINGSPEAK_WRITE_KEY,
        "field3": alert_level
    }
    response = requests.get(THINGSPEAK_URL, params=params)
    return response.text

st.title("🏥 Health Monitoring Dashboard")

placeholder = st.empty()

while True:
    try:
        df = pd.read_csv(URL)
        last = df.iloc[-1]

        bpm = float(last['field1'])
        spo2 = float(last['field2'])

        alert = get_alert_level(bpm, spo2)
        result = send_to_thingspeak(alert)

        alert_labels = {
            0: ("✅ Normal", "green"),
            1: ("⚠️ Warning", "orange"),
            2: ("🚨 Critical", "red")
        }
        label, color = alert_labels[alert]

        with placeholder.container():
            col1, col2 = st.columns(2)
            with col1:
                st.metric("❤️ BPM", f"{bpm}")
            with col2:
                st.metric("🩸 SpO₂", f"{spo2} %")

            st.markdown(f"### Alert: :{color}[{label}]")
            st.write("ThingSpeak field3 updated:", result)
            st.write("Last update:", last['timestamp'])

    except Exception as e:
        st.warning(f"Error: {e}")

    time.sleep(15)
    st.rerun()
