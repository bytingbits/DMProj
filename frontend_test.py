import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequency Visualizer", layout="wide")

st.title("📊 Service Frequency Visualizer")
st.markdown("This app shows a **bar chart (log scale)** and a **histogram** with equi-width binning of all services.")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# --- BAR CHART (log y-axis) ---

st.header("📌 Bar Chart of All Services (Log Scale)")

fig_bar = px.bar(
    df,
    x='Service',
    y='Frequency',
    title='All Services - Frequencies (Log Scale)',
    labels={'Service': 'Service', 'Frequency': 'Frequency'},
    template='plotly_dark',
    color='Frequency',
    color_continuous_scale='teal'
)

fig_bar.update_layout(
    xaxis_title='Service',
    yaxis_title='Frequency (Log Scale)',
    xaxis_tickangle=60,
    yaxis_type='log',
    height=700
)

st.plotly_chart(fig_bar, use_container_width=True)

# --- HISTOGRAM ---

st.header("📊 Histogram of Service Frequencies")

# Slider to select number of bins
num_bins = st.slider("🔧 Select Number of Bins", min_value=10, max_value=200, value=50)

# Create histogram using numpy histogram binning
counts, bins = np.histogram(df['Frequency'], bins=num_bins)

# Mid-points of bins for plotting
bin_centers = 0.5 * (bins[:-1] + bins[1:])

# Create a histogram DataFrame
hist_df = pd.DataFrame({
    'BinCenter': bin_centers,
    'Count': counts
})

# Plot histogram
fig_hist = px.bar(
    hist_df,
    x='BinCenter',
    y='Count',
    labels={'BinCenter': 'Frequency Range (bin center)', 'Count': 'Number of Services'},
    title=f'Histogram of Service Frequencies with {num_bins} Bins',
    template='plotly_dark'
)

fig_hist.update_layout(
    xaxis_title='Frequency Range',
    yaxis_title='Number of Services',
    height=600
)

st.plotly_chart(fig_hist, use_container_width=True)
