#Learning to use streamlit for eventual webapp development
import streamlit as st
import pandas as pd
import numpy as np

st.write('testing testing 123')

x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)