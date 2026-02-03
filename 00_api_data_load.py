'''
00_api_data_load.py

Polar AccessLink API only provides data uploaded to Polar Flow within the last 30 days

This creates a redundancy as data from more than a month ago cannot be accessed

To avoid this I've developed the 00_api_data_load.py script, which will pull and upload exercise data into a seperate dataset 

This dataset will be updated whenever this script is run, adding new instances in

For now it will just handle the loading of data, processing will be added in another file for compartmentalization
'''

import requests
import os
user_id = os.environ.get("POLAR_USER_ID")
access_token = os.environ.get("POLAR_ACCESS_TOKEN")
client_id = os.environ.get("POLAR_CLIENT_ID")
client_secret_id = os.environ.get("POLAR_CLIENT_SECRET")


#Defining API headers and parameters to pull data
header = {
  'Accept': 'application/json',  
  'Authorization': f'Bearer {access_token}'
}

params = {'zones': 'True',
          'samples':'True'}

exercise_data = requests.get(f'https://www.polaraccesslink.com/v3/exercises',
                              headers = header,
                              params = params
                              ).json()

#Loading data as dataframe with id column as index
import pandas as pd
dataframe = pd.DataFrame(exercise_data).set_index('id')

#Path to load dataset
data_path = r'C:\Users\jessep.LAPTOP-7GPOPVDF\Desktop\Personal Projects\polar_data.csv'

#Try loading data from csv path, if it fails, create a csv
try:
    polar_data = pd.read_csv(data_path, index_col = 'id')

except:
    print('Creating data csv')
    dataframe.to_csv(data_path)

#Append any new data to the polar data csv
polar_data = pd.concat([polar_data, dataframe])

#Saving csv 
polar_data.to_csv(data_path)