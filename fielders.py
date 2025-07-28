import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io



st.header("Fielders")

with st.expander("Click Here to input data"):
 
    runs_saved = st.number_input("Runs Saved", min_value=0, step=1)
    runs_given_away = st.number_input("Runs Given Away", min_value=0, step=1)
    drop_catches = st.number_input("Drop Catches", min_value=0, step=1)
    extras = st.number_input("Extras", min_value=0, step=1)
    run_scored_on_extra_ball = st.number_input("Run Scored on extra ball", min_value=0, step=1)
col1, col2,col3 = st.columns(3)

col1.metric("Runs Saved", runs_saved, border=True)
col2.metric("Runs Given Away", runs_given_away, border=True)
col1.metric("Drop Catches", drop_catches, border=True)
col2.metric("Extras", extras, border=True)
col3.metric("Run Scored on extra ball", run_scored_on_extra_ball, border=True)
