import streamlit as st
import pandas as pd

# --- Initialize Session State ---
if "fielder_data" not in st.session_state:
    st.session_state.fielder_data = pd.DataFrame(columns=["Who", "No of Balls", "where", "Active"])

# --- Header ---
st.title("📋 Fielding Position Tracker")

# --- Fielders Performance Metrics ---
with st.expander("General Fielders Performance"):
    runs_saved = st.number_input("Runs Saved", min_value=0, step=1)
    runs_given_away = st.number_input("Runs Given Away", min_value=0, step=1)
    drop_catches = st.number_input("Drop Catches", min_value=0, step=1)
    extras = st.number_input("Extras", min_value=0, step=1)
    run_scored_on_extra_ball = st.number_input("Run Scored on Extra Ball", min_value=0, step=1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Runs Saved", runs_saved)
    col2.metric("Runs Given Away", runs_given_away)
    col1.metric("Drop Catches", drop_catches)
    col2.metric("Extras", extras)
    col3.metric("Run Scored on Extra Ball", run_scored_on_extra_ball)

# --- Add New Entry ---
with st.expander("Add Fielding Error Entry"):
    who = st.text_input("Who?")
    noofballs = st.number_input("Number of Balls", min_value=0, step=1, key="input_balls")
    where = st.text_area("Where?")
    
    if st.button("Add Entry"):
        if who.strip() and where.strip():
            new_row = {
                "Who": who.strip(),
                "No of Balls": int(noofballs),
                "where": where.strip(),
                "Active": True
            }
            st.session_state.fielder_data = pd.concat(
                [st.session_state.fielder_data, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("✅ Fielder entry added.")
        else:
            st.error("Please fill in both 'Who' and 'Where' fields.")

# --- Filter Display ---
st.subheader("📌 Current Fielding Errors")
show_active = st.checkbox("Show only active entries", value=True)
display_df = st.session_state.fielder_data
if show_active:
    display_df = display_df[display_df["Active"] == True]

st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

# --- Edit Entries ---
if not st.session_state.fielder_data.empty:
    with st.expander("✏️ Edit an Entry"):
        edit_index = st.number_input("Entry index to edit", min_value=0,
                                     max_value=len(st.session_state.fielder_data) - 1, step=1)

        edited_row = st.session_state.fielder_data.iloc[edit_index]
        edited_who = st.text_input("Edit Who", value=edited_row["Who"])
        edited_balls = st.number_input("Edit No of Balls", value=int(edited_row["No of Balls"]), min_value=0)
        edited_where = st.text_area("Edit Where", value=edited_row["where"])
        active_status = st.checkbox("Still Active", value=bool(edited_row["Active"]))

        if st.button("Update Entry"):
            st.session_state.fielder_data.at[edit_index, "Who"] = edited_who
            st.session_state.fielder_data.at[edit_index, "No of Balls"] = edited_balls
            st.session_state.fielder_data.at[edit_index, "where"] = edited_where
            st.session_state.fielder_data.at[edit_index, "Active"] = active_status
            st.success("✅ Entry updated.")

# --- Summary Table ---
if not st.session_state.fielder_data.empty:
    st.subheader("Summary by Player")
    summary_df = (
        st.session_state.fielder_data.groupby("Who")
        .agg(
            Total_Balls=pd.NamedAgg(column="No of Balls", aggfunc="sum"),
            Times_Out=pd.NamedAgg(column="where", aggfunc="count"),
            Areas=pd.NamedAgg(column="where", aggfunc=lambda x: list(x))
        )
        .reset_index()
    )
    st.dataframe(summary_df, use_container_width=True)

    with st.expander("📁 Download Options"):
        csv_raw = st.session_state.fielder_data.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Raw Entries (CSV)", data=csv_raw, file_name="fielder_entries.csv", mime="text/csv")

        csv_summary = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Summary by Player (CSV)", data=csv_summary, file_name="fielder_summary.csv", mime="text/csv")

# --- Clear All ---
if st.button("🧹 Clear All Data"):
    st.session_state.fielder_data = pd.DataFrame(columns=["Who", "No of Balls", "where", "Active"])
    st.success("All data cleared.")
