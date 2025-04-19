import streamlit as st
import pandas as pd
import plotly.express as px

# Load main data (df)
file_id = "1LmgJ7wmSq_6sMVFytewc9B1PJ3qwHvHe"
download_url = f"https://drive.google.com/uc?id={file_id}"

try:
    df = pd.read_csv(download_url)
    st.write("Main DataFrame (df):")
    st.write(df)
except Exception as e:
    st.error(f"Error loading df: {e}")

# Set options for multiselect
options = df

# Load association rules (df1)
file_id1 = "1lrL0OwuLVi5DMF_srFDH8Me_yt4o9cNO"
download_url1 = f"https://drive.google.com/uc?id={file_id1}"

try:
    df1 = pd.read_csv(download_url1, converters={
        'antecedents': eval,
        'consequents': eval
    })
    st.write("Association Rules DataFrame (df1):")
    st.write(df1.head())
except Exception as e:
    st.error(f"Error loading df1: {e}")

# Prediction function
def predict_next_websites(current_sites, rules_df, top_n=5, metric='confidence', show_lift=True):
    current_set = frozenset(current_sites)

    matched_rules = rules_df[rules_df['antecedents'].apply(lambda x: x.issubset(current_set))]
    
    if matched_rules.empty:
        return pd.DataFrame(columns=['Website', metric] + (['lift'] if show_lift else []))

    predictions = []
    seen = set()

    for _, row in matched_rules.sort_values(by=metric, ascending=False).iterrows():
        for site in row['consequents']:
            if site not in seen:
                entry = {'Website': site, metric: row[metric]}
                if show_lift:
                    entry['lift'] = row['lift']
                predictions.append(entry)
                seen.add(site)
            if len(predictions) == top_n:
                break
        if len(predictions) == top_n:
            break

    return pd.DataFrame(predictions)

# User input for prediction
current_history = st.multiselect("Choose service in current history:", options)

# Generate and show predictions
if current_history:
    predicted = predict_next_websites(current_history, df1, top_n=5, metric='confidence', show_lift=False)
    st.write("Predicted Next Likely Websites:")
    st.write(predicted)
