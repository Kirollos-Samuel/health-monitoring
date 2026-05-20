import streamlit as st
import pandas as pd
import requests
import pickle
import numpy as np
import time

# Load ML model
model = pickle.load(open("patient_risk_random_forest.pkl", "rb"))

SHEET_ID = "1DZVDm1ilkUGeQEJg5snnIk6cooVlOv6Nj9_FppdhEt8"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

THINGSPEAK_WRITE_KEY = "G595J63730YTM3SL"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def get_alert_level(label):
    mapping = {
        "Normal": 0,
        "Dangerous": 1,
        "Critical": 2
    }
    return mapping.get(label, 0)

def send_to_thingspeak(alert_level):
    params = {
        "api_key": THINGSPEAK_WRITE_KEY,
        "field3": alert_level
    }
    response = requests.get(THINGSPEAK_URL, params=params)
    return response.text

st.title("🏥 Health Monitoring Dashboard")

placeholder = st.empty()
last_alert = None

while True:
    try:
        df = pd.read_csv(URL)
        last = df.iloc[-1]

        # Input order: BPM, Temperature, SpO₂
        bpm = float(last['field1'])
        spo2 = float(last['field2'])
        temp = 36.8  # placeholder until temp field is added

        # Predict
        features = np.array([[bpm, temp, spo2]])
        prediction = model.predict(features)[0]
        alert = get_alert_level(prediction)

        # Only write to ThingSpeak when alert changes
        if alert != last_alert:
            send_to_thingspeak(alert)
            last_alert = alert

        alert_styles = {
            "Normal":    ("✅ Normal",    "green"),
            "Dangerous": ("⚠️ Dangerous", "orange"),
            "Critical":  ("🚨 Critical",  "red")
        }
        label, color = alert_styles[prediction]

        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("❤️ BPM", f"{bpm}")
            with col2:
                st.metric("🩸 SpO₂", f"{spo2} %")
            with col3:
                st.metric("🌡️ Temp", f"{temp} °C")

            st.markdown(f"### Prediction: :{color}[{label}]")
            st.write("Last update:", last['timestamp'])

    except Exception as e:
        st.warning(f"Error: {e}")

    time.sleep(60)
    st.rerun()
