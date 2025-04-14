import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequency Histogram", layout="centered")

st.title("📊 Service Frequency Histogram")
st.markdown("Visualizing distribution of all services from the dataset.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# Optional: toggle log scale
log_y = st.checkbox("🔍 Use log scale for Y-axis", value=True)

# Plot histogram with more bins
fig = px.histogram(
    df,
    x='Frequency',
    nbins=200,  # More bins for better granularity
    title='Distribution of Service Frequencies',
    labels={'Frequency': 'Service Frequency'},
    template='plotly_dark',
    color_discrete_sequence=['cyan']
)

fig.update_layout(
    bargap=0.1,
    xaxis_title='Frequency',
    yaxis_title='Number of Services',
    yaxis_type='log' if log_y else 'linear'  # toggle between log/linear
)

st.plotly_chart(fig, use_container_width=True)
