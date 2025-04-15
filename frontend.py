import streamlit as st
import os
import pandas as pd
import re
import numpy as np

st.set_page_config(page_title="Fuzzy Association Rule Mining Dashboard", layout="wide")

@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

rules_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/association_rules.csv")
itemsets_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/frequent_itemsets.csv")

# Sidebar for global filters and settings
st.sidebar.title("Fuzzy Association Rule Mining Dashboard")
st.sidebar.markdown("An interactive dashboard for analyzing frequent itemsets, association rules, clustering, and predictions.")

#Itemsets Row
st.subheader("Frequent Itemsets")
itemsets_df['support'] = itemsets_df['support'].round(2)

def get_diverse_top_n(df, length, n=10):
    subset = df[df["length"] == length].copy()
    subset["support_bin"] = pd.qcut(subset["support"], q=min(n, len(subset)), duplicates='drop')
    
    diverse_sample = (
        subset.groupby("support_bin", group_keys=False)
        .apply(lambda x: x.sample(2, random_state=42))
        .reset_index(drop=True)
    )
    
    return diverse_sample

top1 = get_diverse_top_n(itemsets_df, length=1, n=10)
top2 = get_diverse_top_n(itemsets_df, length=2, n=10)
top3 = get_diverse_top_n(itemsets_df, length=3, n=10)
    
b1, spacer1, b2, spacer2, b3 = st.columns([2, 0.1, 3.4, 0.1, 4.4])

with b1:
    st.subheader('1-Itemsets')
    top1.index = [''] * len(top1)
    st.dataframe(top1[['itemsets', 'support']].reset_index(drop=True) , height=250)
with b2:
    st.subheader('2-Itemsets')
    top2.index = [''] * len(top2)
    st.dataframe(top2[['itemsets', 'support']].reset_index(drop=True), height=250)
with b3:
    st.subheader('3-Itemsets')
    top3.index = [''] * len(top3)
    st.dataframe(top3[['itemsets', 'support']].reset_index(drop=True), height=250)

#Association Rules Row
st.subheader("Association Rules")
c1, spacer, c2 = st.columns([2.5, 0.5, 7])
with c1:
   st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
   conf_val = st.slider("Confidence", 0.5, 1.0, (0.5, 1.0), step=0.01)
   lift_val = st.slider("Lift", 1.0, round(float(rules_df['lift'].max()), 1), (1.0, round(float(rules_df['lift'].max()), 1)), step=0.1)
    
filtered_rules = rules_df[
    (rules_df['confidence'] >= conf_val[0]) & (rules_df['confidence'] <= conf_val[1]) &
    (rules_df['lift'] >= lift_val[0]) & (rules_df['lift'] <= lift_val[1])
]  

top_rules = filtered_rules.sort_values(by="confidence", ascending=False).head(20)
top_rules = top_rules[['antecedents', 'consequents', 'confidence', 'lift']]
top_rules['confidence'] = top_rules['confidence'].round(2)
top_rules['lift'] = top_rules['lift'].round(2)

with c2:
     if top_rules.empty:
        st.warning("No rules match the selected filters!")
     else:
        top_rules.index = [''] * len(top_rules)
        st.dataframe(top_rules, height=250)
  



