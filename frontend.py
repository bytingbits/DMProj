import streamlit as st
import gdown
import os
import pandas as pd
import re

st.set_page_config(page_title="Fuzzy Association Rule Mining Dashboard", layout="wide")

@st.cache_data
def download_and_load_csv(id, output):
    gdown.download(f"https://drive.google.com/uc?id={id}", output, quiet=False)
    df = pd.read_csv(output)
    return df

#Loading required files
if not os.path.exists("rules.csv"):
    rules_df = download_and_load_csv("1D-A3WpSw8OtuVVM9BD1j8dLw3PORsQna", "rules.csv")

for col in ['antecedents', 'consequents']:
    rules_df[col] = rules_df[col].astype(str).apply(lambda x: re.sub(r"frozenset\(\{?(.*?)\}?\)", r"\1", x))


# Sidebar for global filters and settings
st.sidebar.header("Settings")
st.sidebar.title("Fuzzy Association Rule Mining Dashboard")
st.sidebar.markdown("An interactive dashboard for analyzing frequent itemsets, association rules, clustering, and predictions.")

#Association Rules Row
st.subheader("Association Rules")
c1, c2 = st.columns((2.5,7.5))
with c1:
   conf_val = st.slider("Confidence", 0.5, 1.0, (0.5, 1.0), step=0.01)
   lift_val = st.slider("Lift", 1.0, round(float(rules_df['lift'].max()), 1), (1.0, round(float(rules_df['lift'].max()), 1)), step=0.1)
    
filtered_rules = rules_df[
    (rules_df['confidence'] >= conf_val[0]) & (rules_df['confidence'] <= conf_val[1]) &
    (rules_df['lift'] >= lift_val[0]) & (rules_df['lift'] <= lift_val[1])
]  

top_rules = filtered_rules.sort_values(by="confidence", ascending=False).head(50)
top_rules = top_rules[['antecedents', 'consequents', 'confidence', 'lift']]

with c2:
    with st.container():
        st.markdown(
            """
            <div style='height: 400px; overflow-y: auto;'>
            """,
            unsafe_allow_html=True
        )

        if top_rules.empty:
            st.warning("No rules match the selected filters!")
        else:
            st.table(top_rules.reset_index(drop=True))

        st.markdown("</div>", unsafe_allow_html=True)
    



