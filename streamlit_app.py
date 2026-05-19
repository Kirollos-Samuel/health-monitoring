import json
import pathlib
import time

import streamlit as st

st.title("IoT Dashboard")

DATA_FILE = pathlib.Path("latest_data.json")
DEFAULT_DATA = {"field1": None, "field2": None}


def load_data() -> dict:
    if not DATA_FILE.exists():
        return DEFAULT_DATA.copy()
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


while True:
    data = load_data()
    st.metric("Temperature", data.get("field1"))
    st.metric("Humidity", data.get("field2"))
    time.sleep(5)
    st.rerun()
