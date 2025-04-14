import streamlit as st
import os
import pandas as pd
import re
import plotly.express as px

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
itemsets_df["label"] = itemsets_df["itemsets"].apply(lambda x: ", ".join(eval(x)))
itemsets_df['support'] = itemsets_df['support'].round(2)

top1 = itemsets_df[itemsets_df["length"] == 1].nlargest(10, "support")
top2 = itemsets_df[itemsets_df["length"] == 2].nlargest(10, "support")
top3 = itemsets_df[itemsets_df["length"] == 3].nlargest(10, "support")

def create_bubble(data, title):
    fig = px.scatter(
        data,
        x=[0]*len(data),  # Fake x to make it vertical-ish
        y="support",
        size="support",
        color="label",
        hover_name="label",
        title=title,
        size_max=60,
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(t=40, b=20, l=20, r=20),
    )
    fig.update_traces(marker=dict(opacity=0.6, line=dict(width=1, color='DarkSlateGrey')))
    return fig

b1, spacer1, b2, spacer2, b3 = st.columns([3, 0.5, 3, 0.5, 3])

with b1:
    st.plotly_chart(create_bubble(top1, "1-Itemsets"), use_container_width=True)

with b2:
    st.plotly_chart(create_bubble(top2, "2-Itemsets"), use_container_width=True)

with b3:
    st.plotly_chart(create_bubble(top3, "3-Itemsets"), use_container_width=True)

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
  



