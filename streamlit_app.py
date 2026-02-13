#Learning to use streamlit for eventual webapp development
import streamlit as st
import pandas as pd
import numpy as np
#Required packages for importing and transforming data
import requests
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import psycopg2
import json
import ast
import datetime
import matplotlib.pyplot as plt

#Neon database URL secret
neon_url = os.environ["NEON_DATABASE_URL"]

#Creating engine to connect to database 
engine = create_engine(neon_url)

#Importing data from neon with SQL query
query = """
SELECT *
FROM data_processed
"""
processed_data = pd.read_sql(text(query), engine, index_col= 'id')

#Import samples data
samples_query = """
SELECT "id", "Heart Rate (bpm)" AS hr
FROM samples
"""
samples = pd.read_sql(text(samples_query), engine, index_col = 'id')

#Converting hr column to np.array
samples['hr'] = samples['hr'].apply(
     lambda x: np.array(x)
)

#Import heart rate zone data
zone_query = """
SELECT *
FROM training_zone_metadata
"""
hr_zones = pd.read_sql(text(zone_query), engine)

now = pd.Timestamp(datetime.datetime.now())
current_year, current_week, _ = now.isocalendar()


# Filter using isocalendar
current_week_data = processed_data[
    (processed_data['start_time'].dt.isocalendar().year == current_year) & 
    (processed_data['start_time'].dt.isocalendar().week == current_week)
]

current_week_data = current_week_data.join(samples)


curr_week_overview, extra = st.tabs(["Current Week Overview", "Extra"])
extra.write("Start working on this bit later")


with curr_week_overview:
    if st.button('press me plz'):
        st.dataframe(current_week_data)
        
        exercise_time, exercise_counts = st.columns(2)

        with exercise_time:
            st.title('Total Exercise Time by Sport')
            grup = current_week_data.groupby('detailed_sport_info')['duration'].sum()
            time_pie, ax = plt.subplots()
            ax.pie(grup.values, labels=grup.index)
            st.pyplot(time_pie)


        with exercise_counts:
            #Plotting total counts of sport done
            st.title('Total Exercise Counts')
            sport_counts = current_week_data['detailed_sport_info'].value_counts().reset_index()
            sport_counts.columns = ['Sport', 'Count']
            st.bar_chart(sport_counts, 
                        x = 'Sport', 
                        y = 'Count',
                        sort = False)
        
with extra:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")

