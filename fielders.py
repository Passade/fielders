import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

# --- Initialize Session State ---
if "fielder_data" not in st.session_state:
    st.session_state.fielder_data = pd.DataFrame(columns=["Who", "No of Balls", "where"])

# --- Header ---
st.header("Over Summaries")

# --- Fielders Performance Metrics ---
with st.expander("Fielders"):
    runs_saved = st.number_input("Runs Saved", min_value=0, step=1)
    runs_given_away = st.number_input("Runs Given Away", min_value=0, step=1)
    drop_catches = st.number_input("Drop Catches", min_value=0, step=1)
    extras = st.number_input("Extras", min_value=0, step=1)
    run_scored_on_extra_ball = st.number_input("Run Scored on extra ball", min_value=0, step=1)

# --- Metrics Display ---
col1, col2, col3 = st.columns(3)

col1.metric("Runs Saved", runs_saved, border=True)
col2.metric("Runs Given Away", runs_given_away, border=True)
col1.metric("Drop Catches", drop_catches, border=True)
col2.metric("Extras", extras, border=True)
col3.metric("Run Scored on extra ball", run_scored_on_extra_ball, border=True)

# --- Fielder Position Errors ---
with st.expander("Fielders in wrong Position"):

    who = st.text_input("Who?")
    noofballs = st.number_input("Number of Balls", min_value=0, step=1)
    where = st.text_area("Where?")

    if st.button("Generate Excel"):
        new_row = {
            "Who": who.strip(),
            "No of Balls": int(noofballs),
            "where": where.strip(),
        }
        st.session_state.fielder_data = pd.concat(
            [st.session_state.fielder_data, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Fielder entry added.")

# --- Display Over Summary Table ---
if not st.session_state.fielder_data.empty:
    over_df = st.session_state.fielder_data.sort_values("Who")
    st.subheader("📋 Over Summary Table")
    st.dataframe(over_df, use_container_width=True)

    # --- Download Options ---
    with st.expander("Download Options"):
        # CSV Download
        csv = over_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", data=csv, file_name="fielder_summary.csv", mime="text/csv")

        

# --- Clear Session State (Optional Reset Button) ---
if st.button("Clear Data"):
    st.session_state.fielder_data = pd.DataFrame(columns=["Who", "No of Balls", "where"])
    st.success("All data cleared.")
