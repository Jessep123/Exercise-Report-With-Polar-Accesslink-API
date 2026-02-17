'''
01_data_processing

This file is intended to develop functions/scripts that are used to process data after it is pulled in from Neon

'''
#Required packages for importing and transforming data
import requests
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import psycopg2
import json
import ast


#Neon database URL secret
neon_url = os.environ["NEON_DATABASE_URL"]

#Creating engine to connect to database 
engine = create_engine(neon_url)

#Importing data from neon with SQL query
query = """
SELECT *
FROM polar_data
"""
neon_data = pd.read_sql(text(query), engine)

data_processed = neon_data

#Removing heart_rate_zones column as is just metadata that has already been extracted in 00_api_data_load
data_processed = data_processed.drop('heart_rate_zones', axis = 1)

#Converting time units from object to time dtype
data_processed['upload_time'] = pd.to_datetime(neon_data['upload_time']).dt.tz_convert('Pacific/Auckland')
data_processed['start_time'] = pd.to_datetime(neon_data['start_time'])

#Extracting duration, in seconds, as integer. Removing first two characters (PT) in string
data_processed['duration'] = neon_data['duration'].str[2:-1].astype(float)

#Processing heartrate data

#Converting heartrate from object to dictionary dtype
data_processed['heart_rate'] = data_processed['heart_rate'].apply(ast.literal_eval)

#Mapping dictionary values to their own columns
data_processed['heart_rate_avg'] = data_processed['heart_rate'].apply(lambda x: x.get('average'))
data_processed['heart_rate_max'] = data_processed['heart_rate'].apply(lambda x: x.get('maximum'))

#Removing old heart_rate dictionary column
data_processed = data_processed.drop('heart_rate', axis = 1)

#Extracting route data
routes  = data_processed[['id', 'route']].copy()
routes_final = routes.dropna()

#Removing route column
data_processed = data_processed.drop('route', axis = 1)

#Processing training load data
#Converting training load from object to dictionary dtype
data_processed['training_load_pro'] = data_processed['training_load_pro'].apply(ast.literal_eval)

#Extracting cardio load data and loading it into its own columns
cardio_load = data_processed['training_load_pro'].apply(pd.Series)

#Rejoining training load columns to processed dataframe
data_processed = data_processed.join(cardio_load).drop('training_load_pro', axis = 1)

#Extracting samples data
samples  = data_processed[['id', 'samples']].copy()

#Changing samples into list format then exploding list
samples['samples'] = samples['samples'].apply(ast.literal_eval)
samples = samples.explode('samples')

#Changing each sample to series with dictionary keys as columns and values as data
samples_join = samples['samples'].apply(pd.Series)

#Joining series back to samples table and dropping old values
samples = samples.join(samples_join).drop('samples', axis = 1)

#Converting data to a numpy array
samples['data'] = samples['data'].apply(
    lambda x: np.array(x.split(','), dtype=float)
)

'''
Exercise sample types

List of the polar sample type definitions below

Sourced from polar AccessLink API documentation

Will be joined to samples table for more descriptive info
'''
sample_types = pd.Series({
    0: 'Heart Rate (bpm)',
    1:'Speed (km/h)',
    2:'Cadence (rpm)',
    3:'Altitude (m)',
    4:'Power (W)',
    5:'Power Pedaling Index (%)',
    6: 'Power left-right balance (%)',
    7: 'Air Pressure (hpa)',
    8: 'Running Cadence (spm)',
    9:'Temperature (c)',
    10: 'Distance (m)',
    11: 'RR Interval (ms)'
})

#Updating sample type to written name
samples['sample_type'] = samples['sample_type'].map(sample_types)

#Pivoting for smaller storage 
samples = samples.pivot_table(index = 'id', columns= 'sample_type', values = 'data').reset_index()

#Removing samples columns from data_processed
data_processed = data_processed.drop('samples', axis = 1)

#Loading data_processing into neon
#Controlling for duplicates
with engine.begin() as conn:
        data_processed.to_sql(
            "data_processed_stage",
            conn,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )

        conn.execute(text("""
            INSERT INTO data_processed
            SELECT *
            FROM data_processed_stage
            ON CONFLICT (id) DO NOTHING;
        """))

        conn.execute(text("DROP TABLE data_processed_stage;"))

#Converting np array columns to python list to export
array_cols = [
    'Altitude (m)',
    'Cadence (rpm)',
    'Distance (m)',
    'Heart Rate (bpm)',
    'Power (W)',
    'RR Interval (ms)',
    'Speed (km/h)',
    'Temperature (c)',
]

#Helper function to convert to list/none if empty
def to_py_list(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x   # already a list

for col in array_cols:
    samples[col] = samples[col].apply(to_py_list)

#Loading samples into neon
#Controlling for duplicates

with engine.begin() as conn:
        
        #Creating stage table with same schema as samples
        conn.execute(text('CREATE TABLE samples_stage (LIKE samples INCLUDING DEFAULTS INCLUDING CONSTRAINTS);'))

        samples.to_sql(
        "samples_stage",
        conn,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
        )

        conn.execute(text("""
            INSERT INTO samples
            SELECT *
            FROM samples_stage
            ON CONFLICT (id) DO NOTHING;
        """))

        conn.execute(text("DROP TABLE samples_stage;"))

#Uploading routes table into neon
with engine.begin() as conn:
        
        #Creating stage table with same schema as samples
        conn.execute(text('CREATE TABLE routes_stage (LIKE routes INCLUDING DEFAULTS INCLUDING CONSTRAINTS);'))

        routes_final.to_sql(
        "routes_stage",
        conn,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
        )

        conn.execute(text("""
            INSERT INTO routes
            SELECT *
            FROM routes_stage
            ON CONFLICT (id) DO NOTHING;
        """))

        conn.execute(text("DROP TABLE routes_stage;"))
