import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

st.set_page_config(page_title="Service Frequencies", layout="wide")

st.title("📊 Service Frequencies Bar Chart")
st.markdown("Each bar shows the frequency of a specific service.")

# Load data
@st.cache_data
df = pd.read_csv(CSV_URL)
    

df = load_data()
options = df['Service'] #pred
options = df

# Optional top-k filter
top_k = st.slider("🔝 Show Top K Services", min_value=10, max_value=200, value=50)

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
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Title
st.title("Binned Frequency Distribution of Named Entries")
# Check columns
if 'Service' not in df.columns or 'Frequency' not in df.columns:
    st.error("CSV must contain 'Service' and 'Frequency' columns.")
else:
    # Bin size input
    bin_size = st.number_input("Choose your bin size:", min_value=1, value=10, step=1)

    # Create bins using numpy
    max_freq = df['Frequency'].max()
    bins = np.arange(0, max_freq + bin_size, bin_size)
    df['Frequency Bin'] = pd.cut(df['Frequency'], bins=bins, include_lowest=True)

    # Count how many services fall into each bin
    bin_counts = df['Frequency Bin'].value_counts().sort_index().reset_index()
    bin_counts.columns = ['Frequency Range', 'Number of Services']

    # Plot histogram using Plotly
    fig = px.bar(
        bin_counts,
        x='Frequency Range',
        y='Number of Services',
        labels={'Frequency Range': 'Frequency Interval', 'Number of Services': 'Count of Named Entries'},
        title=f'Binned Histogram of Named Entry Frequencies (Bin Size = {bin_size})'
    )

    st.plotly_chart(fig, use_container_width=True)

