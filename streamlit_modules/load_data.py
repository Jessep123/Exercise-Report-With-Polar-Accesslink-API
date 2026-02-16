import streamlit as st
import streamlit_modules.import_data as import_data
import streamlit_modules.hr_zones_summary as hr_zones_summary

@st.cache_data
def load_data():
    processed_data, hr_zones = import_data.import_data()
    processed_data = hr_zones_summary.add_zones(processed_data, hr_zones)
    return processed_data, hr_zones