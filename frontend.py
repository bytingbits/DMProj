import streamlit as st
import gdown
import os
import pandas as pd
import ast

#Loading required files
if not os.path.exists("association_rules.csv"):
    file_id = "1D-A3WpSw8OtuVVM9BD1j8dLw3PORsQna" 
    gdown.download(f"https://drive.google.com/uc?id={file_id}", "association_rules.csv", quiet=False)

rules_df = pd.read_csv("association_rules.csv")

# Set page configuration
st.set_page_config(page_title="Fuzzy Association Rule Mining Dashboard", layout="wide")

# Sidebar for global filters and settings
st.sidebar.header("Settings")
st.sidebar.title("Fuzzy Association Rule Mining Dashboard")
st.sidebar.markdown("An interactive dashboard for analyzing frequent itemsets, association rules, clustering, and predictions.")

# ---- ROW 1: Dataset Analysis, Itemsets, Clustering ----
st.markdown("## Data Overview, Itemsets, and Clustering")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Dataset Analysis & Stats")
    # TODO: Add dataset statistics and visualizations
    # Example: st.write(df.describe())

with col2:
    st.subheader("Frequent Itemsets")
    # TODO: Display itemsets of different lengths
    # Example: st.dataframe(itemsets_df)

with col3:
    st.subheader("Clustering Visualization")
    # TODO: Add clustering plots (e.g., DBSCAN results)
    # Example: st.plotly_chart(cluster_fig)

# ---- ROW 2: Evaluation Metrics, Association Rules, Prediction Engine ----
st.markdown("## Evaluation Metrics, Association Rules, and Prediction")
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Evaluation Metrics")
    # TODO: Display evaluation metrics like support, confidence, lift
    # Example: st.metric("Support", "0.75")

with col5:
    st.subheader("Association Rules")
    conf_range = st.slider("Confidence Range", 0.5, 1.0, (0.5, 1.0), step=0.01)
    lift_range = st.slider("Lift Range", 1.0, 10.0, (1.0, 3.0), step=0.1)

    filtered_rules = rules_df[
        (rules_df['confidence'] >= conf_range[0]) & (rules_df['confidence'] <= conf_range[1]) &
        (rules_df['lift'] >= lift_range[0]) & (rules_df['lift'] <= lift_range[1])
    ]

    if 'filter_applied' not in st.session_state:
        st.session_state['filter_applied'] = False

    if conf_range != (0.5, 1.0) or lift_range != (1.0, 3.0):
        st.session_state['filter_applied'] = True

    if not st.session_state['filter_applied']:
        st.markdown("Top 50 Rules")
        st.dataframe(
            rules_df.sort_values(by='confidence', ascending=False).head(50)[
                ['antecedents', 'consequents', 'support', 'confidence', 'lift']
            ],
            use_container_width=True
        )
    elif filtered_rules.empty:
        st.info("No rules found for the selected filter values.")
    else:
        st.dataframe(
            filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values(by='confidence', ascending=False),
            use_container_width=True
        )


with col6:
    st.subheader("Prediction Engine")
    # TODO: Implement prediction based on input
    # Example: st.text_input("Enter items:")
    #          st.write("Predicted next item: ...")
