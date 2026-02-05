# Exercise-Report-With-Polar-Accesslink-API
Creating a personalised exercise report using data imported via connecting to the Polar Accesslink API v3.

All data is stored in Neon SQL server

## Current Pipeline 
00_api_data_load
- Pulls data from polar api
- Pulls data from master dataset in neon
- Adds any new rows from polar API data to Neon
- Exports master dataset back to Neon
- All attributes datatype = Text for the time being
- Used in data_load workflow
- Automatically keeps neon data up to date

In Development
01_data_processing.py
- Takes master data from Neon
- Processes, cleans, and formats data
- Particular work needed for samples, heartrate zones, and training load pro columns as these are JSON files
- ^May need to turn these into their own seperate tables
- Also plan to create aggregate weekly summary tables
- Split master data into 'cardio' (running, biking, HIIT) vs 'non-cardio' (strength training) datasets
