import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="All Service Frequencies", layout="wide")

st.title("📊 All Service Frequencies Bar Chart")
st.markdown("Visualizing frequency of every single service in the dataset.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# Plot all services as a bar chart
fig = px.bar(
    df,
    x='Service',
    y='Frequency',
    title='Frequency of All Services (Descending Order)',
    labels={'Service': 'Service', 'Frequency': 'Frequency'},
    template='plotly_dark',
    color='Frequency',
    color_continuous_scale='teal'
)

fig.update_layout(
    xaxis_title='Service',
    yaxis_title='Frequency',
    xaxis_tickangle=60,
    height=700
)

st.plotly_chart(fig, use_container_width=True)
