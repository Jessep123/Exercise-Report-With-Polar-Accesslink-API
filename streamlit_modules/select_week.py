import streamlit as st
import pandas as pd

def week_select(processed_data: pd.DataFrame, label: str = "Select Week"):
    start_date = processed_data['start_time'].min()
    end_date = processed_data['start_time'].max()

    # Generate the weekly range ending on Sunday (W-SUN)
    week_range = pd.period_range(start=start_date, end=end_date, freq='W-SUN').sort_values(ascending=False)

    #Dictionary with formatted week options for easier selection
    week_options  = {
        f"{week.start_time.strftime('%d %B %Y')} - {week.end_time.strftime('%d %B %Y')}": week
        for week in week_range
        }

    #Selection box for week
    selected_label = st.selectbox(label, options = list(week_options.keys()))

    #Extracted period range value from week_options to filter dataframe
    selected_week = week_options[selected_label]

    #Filtering dataframe based on selected week
    selected_week_data = processed_data[
    (processed_data['start_time'] >= selected_week.start_time) & 
    (processed_data['start_time'] <= selected_week.end_time)
    ]

    return selected_week_data