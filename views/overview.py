import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

@st.cache_data
def load_state():
    return pd.read_parquet(DATA / "state_agg.parquet")

st.title("Consumer Financial Stress by State")
st.write("Complaint volume and average stress signal rolled up to state level. Darker states have higher average distress scores across complaints.")

state_df = load_state()

fig = px.choropleth(
    state_df,
    locations="state",
    locationmode="USA-states",
    color="avg_severity",
    scope="usa",
    color_continuous_scale="Reds",
    hover_data=["complaint_count", "top_theme"],
    labels={"avg_severity": "Avg Stress Score", "complaint_count": "Complaints"},
)
fig.update_layout(
    geo=dict(bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=0, r=0, t=20, b=0),
    coloraxis_colorbar=dict(title="Stress Score")
)
st.plotly_chart(fig, width="stretch")

st.divider()
st.subheader("State-level data table")
st.dataframe(
    state_df.sort_values("complaint_count", ascending=False),
    width="stretch"
)