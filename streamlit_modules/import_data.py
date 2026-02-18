
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

   #Import route data
    route_query = """
    SELECT *
    FROM routes
    """
    routes = pd.read_sql(text(route_query), engine, index_col = 'id')

    return processed_data, hr_zones, routes

def process_routes(data):
    import ast
    data_updated = data.copy()
    data_updated['route'] = data['route'].apply(ast.literal_eval)

    #Helper function to remove extra unneeded key,value pairs from route dictionary
    def remove_extra(row):
        row_adjusted = row
        for value in row_adjusted:
            for dic in value:
                dic['time'] = float(dic['time'][2:-1])
                del dic['satellites']
                del dic['fix']
        return row_adjusted
    
    #Applying remove extra function to each route 
    data_updated = data_updated.apply(lambda x: remove_extra(x))

    return data_updated