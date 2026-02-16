
def import_data():
    #Required packages for importing and transforming data
    import requests
    import os
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine, text
    import psycopg2

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

    #Joining processed data and samples
    processed_data = processed_data.join(samples)

    #Import heart rate zone data
    zone_query = """
    SELECT "lower_limit" AS lower, "upper_limit" AS upper, training_zone AS zone
    FROM training_zone_metadata
    """
    hr_zones = pd.read_sql(text(zone_query), engine)

    return processed_data, hr_zones