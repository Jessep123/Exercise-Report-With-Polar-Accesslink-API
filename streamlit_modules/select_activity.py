import streamlit as st
import pandas as pd

def activity_options(data: pd.DataFrame):
    #Helper function for dictionary expression
    def activity_string(entry):
        import time

        #Using below map to change names of exercises into something nicer to look at
        sport_map = {'RUNNING': 'Run',
                'INDOOR_CYCLING': 'Watt bike',
                'STRENGTH_TRAINING': 'Weights',
                'HIIT': 'HIIT',
                'HIKING': 'Hike'}
        activity_title = sport_map[entry[1]]

        #Formatting date to display day
        formatted_date = entry[2].strftime('%a %d %b')

        minutes = time.strftime('%H:%M:%S', time.gmtime(entry[3]))

        #Returning formatted f string for dictionary expression
        return f'{activity_title:<10} - {formatted_date} - {minutes}'
    
    data = data.sort_values(by = 'start_time', ascending=False)

    activity_options = {activity_string(entry)
            : entry[0]
            for entry in zip(data.index, data['detailed_sport_info'], data['start_time'], data['duration'])
            }
    
    return activity_options

#Function to executre above processing and create formatted selection box
def activity_options_selectbox(data: pd.DataFrame):
    activity_dic = activity_options(data = data)
    selected_activity = st.selectbox('Select Activity', options = list(activity_dic.keys()))

    activity_id = activity_dic[selected_activity]

    return data.loc[activity_id], data[data.index == activity_id]


def activity_summary(selected_activity: pd.DataFrame):   
        row = st.columns(3)

        #Markdown colour based on HR number
        def hr_colour(hr):
            if hr < 119:
                colour = 'grey'
            elif hr >=119 and hr <= 139:
                colour = 'blue'
            elif hr > 139 and hr <= 158:
                colour = 'green'
            elif hr > 158 and hr <= 178:
                colour = 'orange'
            elif hr > 179:
                colour = 'red'
            return colour

        #Avergage heartrate tile
        col1_tile = row[0].container(height=120)
        col1_tile.markdown('#### Average HR', text_alignment  = 'center')
        col1_tile.markdown(f':{hr_colour(selected_activity['heart_rate_avg'])}[{selected_activity['heart_rate_avg']}]', 
                           text_alignment= 'center')
        #Max heartrate tile
        col2_tile = row[1].container(height=120)
        col2_tile.markdown('#### Max HR', text_alignment  = 'center')
        col2_tile.markdown(f':{hr_colour(selected_activity['heart_rate_max'])}[{selected_activity['heart_rate_max']}]', 
                           text_alignment= 'center')
        #Cardio load tile
        col3_tile = row[2].container(height=120)
        col3_tile.markdown('#### Cardio Load', text_alignment  = 'center')
        col3_tile.markdown(f'{selected_activity['heart_rate_max']}', 
                           text_alignment= 'center')