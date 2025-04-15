import streamlit as st
import os
import pandas as pd
import re
import numpy as np
import skfuzzy as fuzz
import plotly.graph_objects as go

st.set_page_config(page_title="Fuzzy Association Rule Mining Dashboard", layout="wide")

@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

rules_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/association_rules.csv")
itemsets_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/frequent_itemsets.csv")

# Sidebar for global filters and settings
st.sidebar.title("Fuzzy Association Rule Mining Dashboard")
st.sidebar.markdown("An interactive dashboard for analyzing frequent itemsets, association rules, clustering, and predictions.")

#Fuzzification Row
st.subheader("Fuzzification")
a1, a2 = st.columns([6, 4])
# Parameters
low_params = [0, 0, 50]
medium_params = [25, 50, 75]
high_params = [50, 100, 100]

# Trimmed x-axis for better view
x = np.linspace(0, 100, 500)
y_low = fuzz.trimf(x, low_params)
y_med = fuzz.trimf(x, medium_params)
y_high = fuzz.trimf(x, high_params)

# Aesthetic color palette
colors = {
    "low": "#5DADE2",    # soft blue
    "medium": "#F5B041", # amber
    "high": "#58D68D",   # mint green
    "line": "rgba(120,120,120,0.5)"  # faint gray
}

# Base static membership curves
base_traces = [
    go.Scatter(x=x, y=y_low, mode='lines', name='Low', line=dict(color=colors["low"], width=3)),
    go.Scatter(x=x, y=y_med, mode='lines', name='Medium', line=dict(color=colors["medium"], width=3)),
    go.Scatter(x=x, y=y_high, mode='lines', name='High', line=dict(color=colors["high"], width=3)),
]

# Initial position
init_val = 10
μ_l0 = fuzz.trimf(np.array([init_val]), low_params)[0]
μ_m0 = fuzz.trimf(np.array([init_val]), medium_params)[0]
μ_h0 = fuzz.trimf(np.array([init_val]), high_params)[0]

# Initial dot traces + vertical line
init_traces = [
    go.Scatter(x=[init_val], y=[μ_l0], mode='markers+text', name='Low μ',
               marker=dict(color=colors["low"], size=10, line=dict(width=1, color='black')),
               text=["Low"], textposition="top center"),
    go.Scatter(x=[init_val], y=[μ_m0], mode='markers+text', name='Medium μ',
               marker=dict(color=colors["medium"], size=10, line=dict(width=1, color='black')),
               text=["Med"], textposition="top center"),
    go.Scatter(x=[init_val], y=[μ_h0], mode='markers+text', name='High μ',
               marker=dict(color=colors["high"], size=10, line=dict(width=1, color='black')),
               text=["High"], textposition="top center"),
    go.Scatter(x=[init_val, init_val], y=[0, 1], mode='lines',
               name='Current Visit Count',
               line=dict(color=colors["line"], dash='dot', width=2))
]

# Animation frames
frames = []
for val in range(1, 101, 2):
    μ_l = fuzz.trimf(np.array([val]), low_params)[0]
    μ_m = fuzz.trimf(np.array([val]), medium_params)[0]
    μ_h = fuzz.trimf(np.array([val]), high_params)[0]

    frames.append(go.Frame(
        data=[
            # Redraw membership lines
            go.Scatter(x=x, y=y_low, mode='lines', line=dict(color=colors["low"], width=3)),
            go.Scatter(x=x, y=y_med, mode='lines', line=dict(color=colors["medium"], width=3)),
            go.Scatter(x=x, y=y_high, mode='lines', line=dict(color=colors["high"], width=3)),
            # Dots with labels
            go.Scatter(x=[val], y=[μ_l], mode='markers+text',
                       marker=dict(color=colors["low"], size=10, line=dict(width=1, color='black')),
                       text=["Low"], textposition="top center"),
            go.Scatter(x=[val], y=[μ_m], mode='markers+text',
                       marker=dict(color=colors["medium"], size=10, line=dict(width=1, color='black')),
                       text=["Med"], textposition="top center"),
            go.Scatter(x=[val], y=[μ_h], mode='markers+text',
                       marker=dict(color=colors["high"], size=10, line=dict(width=1, color='black')),
                       text=["High"], textposition="top center"),
            # Vertical guide
            go.Scatter(x=[val, val], y=[0, 1], mode='lines',
                       line=dict(color=colors["line"], dash='dot', width=2)),
        ],
        name=str(val)
    ))

# Combine all into final figure
fig = go.Figure(data=base_traces + init_traces, frames=frames)

fig.update_layout(
    title='Triangular Membership Function',
    title_font_size=15,
    plot_bgcolor='white',
    xaxis=dict(title='Visit Count', range=[0, 100], gridcolor='lightgray'),
    yaxis=dict(title='Membership Value', range=[0, 1.1], gridcolor='lightgray'),
    font=dict(family="Arial", size=14),
    updatemenus=[{
        "type": "buttons",
        "showactive": False,
        "buttons": [{
            "label": "Play",
            "method": "animate",
            "args": [None, {
                "frame": {"duration": 200, "redraw": True},  # slower animation
                "fromcurrent": True,
                "transition": {"duration": 100, "easing": "linear"}
            }]
        }]
    }]
)

with a1:
    st.plotly_chart(fig, use_container_width=True)

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
    
b1, b2, b3 = st.columns([1, 1, 1])

with b1:
    st.subheader('1-Itemsets')
    st.dataframe(top1[['itemsets', 'support']], height=250, hide_index=True)
with b2:
    st.subheader('2-Itemsets')
    st.dataframe(top2[['itemsets', 'support']], height=250, hide_index=True)
with b3:
    st.subheader('3-Itemsets')
    st.dataframe(top3[['itemsets', 'support']], height=250, hide_index=True)

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
        st.dataframe(top_rules, height=250, hide_index=True)
  



