import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#Load data module
from  streamlit_modules.load_data import load_data
processed_data, hr_zones, routes = load_data()

#Plotting module
import streamlit_modules.plots as plots

#Week_select automatically filters processed_data to the selected week
from streamlit_modules.select_week import week_select 




#Sidebar definitions
with st.sidebar:
    selected_week_data = week_select(processed_data)



# week_summary, individual = st.tabs(["Week Overview", "Training Explorer"])
individual, week_summary = st.tabs(["Training Explorer","Weekly Overview"])

#Current week overview code
with week_summary:
    st.session_state['active_tab'] = 'Week'
    #Plotting training zone proportions
    st.pyplot(plots.visualize_zone_times(selected_week_data))
    
    #Plotting total time by sport and total counts
    exercise_time, exercise_counts = st.columns(2)
    with exercise_time:
        st.title('Total Exercise Time by Sport')
        grup = selected_week_data.groupby('detailed_sport_info')['duration'].sum()
        time_pie, ax = plt.subplots()
        ax.pie(grup.values, labels=grup.index)
        st.pyplot(time_pie)

    with exercise_counts:
        #Plotting total counts of sport done
        st.title('Total Exercise Counts')
        sport_counts = selected_week_data['detailed_sport_info'].value_counts().reset_index()
        sport_counts.columns = ['Sport', 'Count']
        st.bar_chart(sport_counts, 
                    x = 'Sport', 
                    y = 'Count',
                    sort = False)

with individual:    
    st.title('Individual Session Explorer')

    #Display formatted session title options
    from streamlit_modules.select_activity import activity_options_selectbox
    selected_activity, selected_dataframe, activity_id = activity_options_selectbox(selected_week_data)

    #Summary statistics container
    stats = st.container(border = True)
    with stats:
        from streamlit_modules.select_activity import activity_summary
        summary = activity_summary(selected_activity = selected_activity)

    #Line graph container
    line_graph = st.container(border = True)
    with line_graph:
        # from streamlit_modules.plots import activity_line_graph_hr
        line_graph.header('Heart Rate Over Activity', text_alignment= 'center')

        hr_graph = plots.activity_line_graph_hr(selected_dataframe)
        st.pyplot(hr_graph)

    if selected_activity['has_route'] == 'True':
        map = st.container(border = True)
        with map:
            selected_route = routes[routes.index == activity_id].explode(column = 'route')

            # selected_route['latitude'] = selected_route['route']['latitude']
            selected_route = selected_route['route'].apply(pd.Series)

            map_style = 'light'
            st.map(selected_route, 
                latitude = 'latitude', 
                longitude = 'longitude',
                size = 1)




   