
import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequency Histogram", layout="centered")

st.title("📊 Service Frequency Histogram")
st.markdown("Showing frequency distribution of all services from your dataset.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# Plot histogram
fig = px.histogram(
    df,
    x='frequency',
    nbins=50,
    title='Distribution of Service Frequencies',
    labels={'frequency': 'Service Frequency'},
    template='plotly_white',
    color_discrete_sequence=['teal']
)

fig.update_layout(
    bargap=0.1,
    xaxis_title='Frequency',
    yaxis_title='Number of Services'
)

st.plotly_chart(fig, use_container_width=True)
