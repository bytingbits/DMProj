import streamlit as st
import pandas as pd

# Load main dataset (df)
file_id = "1LmgJ7wmSq_6sMVFytewc9B1PJ3qwHvHe"
download_url = f"https://drive.google.com/uc?id={file_id}"

st.subheader("Main Dataset (df)")
st.write("Download URL:", download_url)

try:
    df = pd.read_csv(download_url)
    st.write("Columns in df:", df.columns.tolist())
    st.write(df.head())
except Exception as e:
    st.error(f"Error loading df: {e}")

# Load association rules dataset (df1)
fid = "1lrL0OwuLVi5DMF_srFDH8Me_yt4o9cNO"
download_url1 = f"https://drive.google.com/uc?id={fid}"

st.subheader("Association Rules Dataset (df1)")
st.write("Download URL:", download_url1)

try:
    df1 = pd.read_csv(download_url1, converters={
        'antecedents': eval,
        'consequents': eval
    })
    st.write("Columns in df1:", df1.columns.tolist())
    st.write(df1.head())
except Exception as e:
    st.error(f"Error loading df1: {e}")

# Prediction logic
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

# Multiselect input
options = df
current_history = st.multiselect("Choose service in current history:", options)

# Show predictions
if current_history:
    st.subheader("Predicted Next Likely Websites")
    predicted = predict_next_websites(current_history, df1, top_n=5, metric='confidence', show_lift=False)
    st.write(predicted)
