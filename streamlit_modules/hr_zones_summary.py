#Function for processing heart rate zones data
def add_zones(data, hr_zones):
       import pandas as pd

       #Isolating/exploding heartrate numpy array
       current_week_hr = data['hr']
       current_week_hr = current_week_hr.explode()

       #Creating list to define bin ranges for heartrate zones
       bins = list(hr_zones['lower']) + [hr_zones['upper'].iloc[-1]]

       #Extracting zone labels 
       labels = hr_zones['zone']

       #Cutting to classify each row in a zone
       cutted = pd.cut(current_week_hr, 
              bins,
              labels = labels,
              right = False).to_frame()
       

       #Pivotting to get a table with total counts of each hr zone as columns
       pivot = (cutted.groupby(level=0)['hr']
                      .value_counts()
                      .unstack(fill_value=0)
                      )
       
       pivot.columns = pivot.columns.astype(str)

       final = data.merge(
       pivot,
       left_index=True,
       right_index=True,
       how="left"
       )


       return final