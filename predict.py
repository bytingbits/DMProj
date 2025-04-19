import streamlit as st
import pandas as pd
import plotly.express as px


CSV_URL = "https://raw.githubusercontent.com/bytingbits/DMProj/main/sorted_service_frequencies.csv"

#st.set_page_config(page_title="Service Frequencies", layout="wide")

#st.title("📊 Service Frequencies Bar Chart")
#st.markdown("Each bar shows the frequency of a specific service.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()
options = df #pred
st.write(df)

CSV_URL1 = "https://raw.githubusercontent.com/bytingbits/DMProj/main/cleaned_final_association_rules.csv"
df1 = pd.read_csv(CSV_URL1, converters={
    'antecedents': eval,
    'consequents': eval
})

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
