import streamlit as st

overview    = st.Page("views/overview.py",    title="Overview",     default=True)
themes      = st.Page("views/themes.py",      title="Theme Explorer")
methodology = st.Page("views/methodology.py", title="Methodology")

pg = st.navigation([overview, themes, methodology])
st.set_page_config(page_title="CFPB Community Signal", layout="wide")
pg.run()