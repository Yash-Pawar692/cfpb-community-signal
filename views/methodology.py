import streamlit as st

st.title("Methodology and Data Governance")

st.subheader("Data source")
st.write("""
This project uses the **CFPB Consumer Complaint Database**, published by the
Consumer Financial Protection Bureau. The data is public domain (CC0),
meaning it is free to use, share, and build on without restriction.

Consumers opt in to share their complaint narratives, and the CFPB removes
personal details before publishing. ZIP codes in narrative complaints are
truncated to 3 digits, so ZIP-3 is the finest geographic grain used here.
""")

st.subheader("NLP pipeline")
st.write("""
The pipeline runs in two passes.

The first pass uses **spaCy** to extract named entities (organisations, money
amounts, dates) and **scikit-learn TF-IDF with NMF** to surface recurring
complaint themes from the text.

The second pass uses the **Claude Haiku 4.5 API** to classify each narrative
into a structured schema: a behavioural category, an emotional intensity score,
and a resolution expectation. A SHA-256 cache means each narrative is only
classified once.

The severity score is a transparent lexicon-based signal: it counts how many
distress-related words appear in the narrative and normalises the result to 0-1.
The full word list is published in the repository.
""")

st.subheader("Data classification")
st.write("""
| Tier | What it covers | Where it lives |
|------|---------------|----------------|
| P1 Public | Aggregated state and ZIP-3 outputs, this app | GitHub repo and this app |
| P2 Internal | Raw API pull, intermediate enriched table, Claude cache | Colab only, not committed |
| P3 Restricted | Anthropic API key | Colab Secrets only, never written to code |
""")

st.subheader("Privacy decisions")
st.write("""
All outputs are aggregated. No individual complaint narratives are stored or
displayed in this app. Communities with fewer than 20 complaints are suppressed
to avoid exposing thin, potentially re-identifiable groups.

The raw narrative text is processed once in a private Colab environment and
then discarded. Only the numeric aggregates travel to the deployed app.
""")

st.subheader("Limitations")
st.write("""
- Complaints are self-reported and unverified
- Only consumers who opt in to share narratives are included, so the sample is not representative of all complaints
- The severity score is a simple lexicon signal, not a validated clinical measure
- Geographic coverage depends on complaint volume; low-population states have fewer data points
- This is a portfolio prototype, not a production system
""")