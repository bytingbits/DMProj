import streamlit as st
import os
import pandas as pd
import re
import numpy as np
import skfuzzy as fuzz
import plotly.graph_objects as go
from collections import Counter
import ast

st.set_page_config(page_title="Fuzzy Association Rule Mining Dashboard", layout="wide")

@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

rules_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/association_rules.csv")
itemsets_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/frequent_itemsets.csv")
fuzzy_df = load_csv("https://raw.githubusercontent.com/bytingbits/DMProj/refs/heads/main/fuzzified_transactions.csv")

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
    title_font_size=19,
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

with a2:
    time_options = fuzzy_df['time_window'].unique().tolist()
    selected_time = st.selectbox("Select Time Window", time_options)

    # Get the row for the selected time
    txn_row = fuzzy_df[fuzzy_df['time_window'] == selected_time].iloc[0]
    fuzzy_visits = txn_row['fuzzified_visits']
    fuzzy_visits = ast.literal_eval(txn_row['fuzzified_visits'])
    
    # Count most dominant membership label per service
    label_counts = Counter()
    for _, _, memberships in fuzzy_visits:
        dominant_label = max(memberships, key=memberships.get)  # L / M / H
        label_counts[dominant_label] += 1
    
    # Prepare chart data
    categories = ['L', 'M', 'H']
    colors = ['#ff9aa2', '#ffb7b2', '#ffdac1']
    counts = [label_counts.get(c, 0) for c in categories]
    names = ['Low', 'Medium', 'High']
    
    # Plot donut
    fig = go.Figure(data=[go.Pie(
        labels=names,
        values=counts,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    fig.update_layout(
        title=f'Fuzzy Membership Distribution – {selected_time}',
        showlegend=True,
        margin=dict(t=50, b=0, l=0, r=0),
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',  # transparent
        plot_bgcolor='rgba(0,0,0,0)',
        width=400,  # or 450 to match
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

def format_membership(mem):
    return f"L: {mem['L']:.2f}, M: {mem['M']:.2f}, H: {mem['H']:.2f}"

def render_transaction_table(txn_row):
    data = [{
        "Service": s,
        "Count": c,
        "Fuzzy Membership": format_membership(mem),
        "Label": max(mem, key=mem.get)  # 'L', 'M', or 'H'
    } for s, c, mem in txn_row['fuzzified_visits']]

    df_display = pd.DataFrame(data).sort_values(by="Count", ascending=False)
    st.dataframe(df_display, use_container_width=True)

txn_row = fuzzy_df[fuzzy_df['time_window'].astype(str) == selected_time].iloc[0]
render_transaction_table(txn_row)

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
    
b1, b2 = st.columns([1, 2])

with b1:
    st.subheader('1-Itemsets')
    st.dataframe(top1[['itemsets', 'support']], height=250, hide_index=True)
with b2:
    st.subheader('2-Itemsets')
    st.dataframe(top2[['itemsets', 'support']], height=250, hide_index=True)

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
  
#Prediction Row
st.subheader("Prediction")
d1, d2 = st.columns([1, 1])
def parse_antecedent_string(s):
    return [i.strip().strip("'") for i in s.split(",")]

all_services = sorted(set(
    service
    for row in rules_df['antecedents']
    for service in parse_antecedent_string(row)
))
with d1:
    st.subheader("Select Services (Max 2)")
    selected_services = st.multiselect(
        "Fuzzy Services",
        options=all_services
    )

    predict_clicked = st.button("Predict Next Service")

def predict_top_5_next_websites(user_session, rules):
    user_set = set(user_session)

    def is_match(ante_str):
        antecedent_set = set(parse_antecedent_string(ante_str))
        return antecedent_set.issubset(user_set)

    matching_rules = rules[rules['antecedents'].apply(is_match)]

    if not matching_rules.empty:
        top_5 = matching_rules.sort_values(by=["confidence", "lift"], ascending=False).head(5)
        return top_5[['consequents', 'confidence', 'lift']]

    return pd.DataFrame({"Message": ["No matching rules found."]})
    
with d2:
    st.subheader("Predicted Services")
    if predict_clicked and selected_services:
        predicted_df = predict_top_5_next_websites(selected_services, rules_df)
        st.dataframe(
            predicted_df.rename(columns={
                "consequents": "Predicted Services",
                "confidence": "Confidence",
                "lift": "Lift"
            }),
            use_container_width=True,
            height=250,
            hide_index=True
        )
    
    elif predict_clicked and not selected_services:
        st.warning("Please select 1 or 2 fuzzy services before predicting.")


