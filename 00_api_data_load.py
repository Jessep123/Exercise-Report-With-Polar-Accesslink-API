'''
00_api_data_load.py

Polar AccessLink API only provides data uploaded to Polar Flow within the last 30 days

This creates a redundancy as data from more than a month ago cannot be accessed

To avoid this I've developed the 00_api_data_load.py script, which will pull and upload exercise data into a Neon PostGres SQL server 

This online dataset will be updated whenever this script is run, adding new instances in

For now it will just handle the loading of data, processing will be added in another file for compartmentalization

Any processing/transformations will occur in 01_data_processing.py.

This script just uploads and refreshes the SQL master data as is
'''

#Needed to import data from polar API
import requests
import os
import pandas as pd

#Secrets/access tokens required for script
access_token = os.environ.get("POLAR_ACCESS_TOKEN")
neon_url = os.environ["NEON_DATABASE_URL"]

#Defining header/params for accessing polar data
exercises_header = {
  'Accept': 'application/json',  
  'Authorization': f'Bearer {access_token}'
}
params = {'zones': 'True',
          'samples':'True'}

#Importing data from polar API
exercise_data = requests.get(f'https://www.polaraccesslink.com/v3/exercises',
                              headers = exercises_header,
                              params = params
                              ).json()

polar_data = pd.DataFrame(exercise_data)


#Importing neon dataset
from sqlalchemy import create_engine, text
import psycopg2
from sqlalchemy import text


engine = create_engine(neon_url)


#SQL Query
query = """
SELECT *
FROM polar_data
"""
neon_data = pd.read_sql(text(query), engine)

polar_data["id"] = polar_data["id"].astype(str).str.strip()
neon_data["id"] = neon_data["id"].astype(str).str.strip()

#Isolate any new rows from the polar API
new_data = polar_data[~polar_data["id"].isin(neon_data["id"])]

#Exporting data back to neon if there are new rows
if len(new_data) != 0:

    engine.dispose()  # close old pooled connections
    engine = create_engine(os.environ["NEON_DATABASE_URL"])

    #Converting columns to text for simplicities sake
    for col in new_data.columns:
        new_data[col] = new_data[col].where(new_data[col].isna(), new_data[col].astype(str))
        
    with engine.begin() as conn:
        new_data.to_sql(
            "polar_data_stage",
            conn,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )

        conn.execute(text("""
            INSERT INTO polar_data
            SELECT *
            FROM polar_data_stage
            ON CONFLICT (id) DO NOTHING;
        """))

        conn.execute(text("DROP TABLE polar_data_stage;"))