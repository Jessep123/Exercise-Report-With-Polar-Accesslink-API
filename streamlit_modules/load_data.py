import streamlit as st
import streamlit_modules.import_data as import_data
from streamlit_modules.import_data import process_routes

import streamlit_modules.hr_zones_summary as hr_zones_summary

@st.cache_data
def load_data():
    processed_data, hr_zones, routes = import_data.import_data()
    processed_data = hr_zones_summary.add_zones(processed_data, hr_zones)
    routes = process_routes(routes)
    return processed_data, hr_zones, routes