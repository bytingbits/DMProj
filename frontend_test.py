import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequency Histogram", layout="centered")

st.title("🔍 Service Frequency Histogram")
st.markdown("Visualizing service frequencies with top & bottom 2.5% highlighted.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# Extract frequency column
frequencies = df['frequency']

# Calculate thresholds for top and bottom 2.5%
lower_thresh = frequencies.quantile(0.025)
upper_thresh = frequencies.quantile(0.975)

# Categorize data into 3 segments
low_values = frequencies[frequencies < lower_thresh]
mid_values = frequencies[(frequencies >= lower_thresh) & (frequencies <= upper_thresh)]
high_values = frequencies[frequencies > upper_thresh]

# Plot with Plotly
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=low_values,
    name='Bottom 2.5%',
    marker_color='blue',
    opacity=0.75
))

fig.add_trace(go.Histogram(
    x=mid_values,
    name='Middle 95%',
    marker_color='gray',
    opacity=0.75
))

fig.add_trace(go.Histogram(
    x=high_values,
    name='Top 2.5%',
    marker_color='red',
    opacity=0.75
))

# Layout and overlay style
fig.update_layout(
    barmode='overlay',
    title='Service Frequency Distribution',
    xaxis_title='Frequency',
    yaxis_title='Count',
    legend_title='Percentile Groups',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

