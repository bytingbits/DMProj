import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequencies", layout="wide")

st.title("📊 Service Frequencies Bar Chart")
st.markdown("Each bar shows the frequency of a specific service.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

# Optional top-k filter
top_k = st.slider("🔝 Show Top K Services", min_value=10, max_value=len(df), value=50)

# Plot bar chart
fig = px.bar(
    df.head(top_k),
    x='Service',
    y='Frequency',
    title=f'Top {top_k} Services by Frequency',
    labels={'Service': 'Service Name', 'Frequency': 'Frequency'},
    template='plotly_dark',
    color='Frequency',
    color_continuous_scale='teal'
)

fig.update_layout(
    xaxis_tickangle=45,
    xaxis_title='Service',
    yaxis_title='Frequency',
    height=600
)

st.plotly_chart(fig, use_container_width=True)
