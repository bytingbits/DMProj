import streamlit as st
import pandas as pd
import plotly.express as px








file_id = "1LmgJ7wmSq_6sMVFytewc9B1PJ3qwHvHe"
download_url = f"https://drive.google.com/uc?id={file_id}"

# Load into pandas DataFrame
df = pd.read_csv(download_url)
st.write(df)
options = df
#CSV_URL1 = "https://drive.google.com/file/d/1lrL0OwuLVi5DMF_srFDH8Me_yt4o9cNO"
#https://drive.google.com/file/d/
file_id1 = "1lrL0OwuLVi5DMF_srFDH8Me_yt4o9cNO"
download_url1 = f"https://drive.google.com/uc?id={file_id1}"

df1 = pd.read_csv(download_url1, converters={
    'antecedents': eval,
    'consequents': eval
})
st.write(" df1 'dump" )
st.write(df1)
def predict_next_websites(current_sites, rules_df, top_n=5, metric='confidence', show_lift=True):
    """
    Predicts the next likely website(s) based on fuzzy association rules.

    Args:
        current_sites (list or set): The websites visited so far.
        rules_df (DataFrame): The mined fuzzy association rules.
        top_n (int): Number of top predictions to return.
        metric (str): Metric to sort predictions by.
        show_lift (bool): Whether to include lift in the output DataFrame.

    Returns:
        DataFrame: Top predicted websites with selected metrics.
    """
    current_set = frozenset(current_sites)

    # Filter rules where antecedents are a subset of current sites
    matched_rules = rules_df[rules_df['antecedents'].apply(lambda x: x.issubset(current_set))]
    
    if matched_rules.empty:
        return pd.DataFrame(columns=['Website', metric] + (['lift'] if show_lift else []))

    # Flatten consequents and collect metrics
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

current_history = selected = st.multiselect("Choose service in current history: ", options)
predicted = predict_next_websites(current_history, df1, top_n=5, metric='confidence', show_lift=False)
st.write(predicted)
