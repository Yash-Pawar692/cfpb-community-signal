import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

@st.cache_data
def load_themes():
    return pd.read_parquet(DATA / "theme_summary.parquet")

@st.cache_data
def load_zip3():
    return pd.read_parquet(DATA / "zip3_agg.parquet")

st.title("Theme Explorer")
st.write("Select a theme to see how it concentrates across communities.")

themes_df = load_themes()
zip3_df = load_zip3()

# Theme selector
choice = st.selectbox(
    "Select a theme",
    sorted(themes_df["theme_label"].unique())
)

row = themes_df[themes_df["theme_label"] == choice].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Complaints", int(row["complaint_count"]))
col2.metric("Avg Stress Score", round(float(row["avg_severity"]), 3))
col3.metric("Top State", row["top_state"])

st.divider()

st.subheader("ZIP-3 communities with this theme")
zip3_filtered = zip3_df[zip3_df["top_theme"] == choice].sort_values(
    "complaint_count", ascending=False
)

if zip3_filtered.empty:
    st.info("No ZIP-3 communities with enough volume to display for this theme.")
else:
    fig = px.bar(
        zip3_filtered.head(20),
        x="zip3",
        y="complaint_count",
        color="avg_severity",
        color_continuous_scale="Reds",
        labels={"zip3": "ZIP-3 Prefix", "complaint_count": "Complaints", "avg_severity": "Stress Score"},
    )
    st.plotly_chart(fig, width="stretch")
    st.dataframe(zip3_filtered, width="stretch")