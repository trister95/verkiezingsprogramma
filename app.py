import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data (this would be replaced by the actual path to your data)
@st.cache  # This decorator caches the data and only reloads it when the file changes
def load_data(filename):
    return pd.read_csv(filename)

# Load your data
df = load_data('test/test_csvs/parties_sentences_topics.csv')
metrics_df = load_data('test/test_csvs/metrics.csv')

# Sidebar for party selection
party_list = df['party'].unique()
party = st.sidebar.selectbox('Select a party:', party_list)

# Filter data for the selected party
party_data = df[df['party'] == party]
metrics_party_data = metrics_df[metrics_df['party'] == party]

# Main plot area
st.write(f"Attention plot for {party}")

# Sort the topics by the relative difference to have a meaningful order in the plot
party_data_sorted = metrics_party_data.sort_values('relative_difference', ascending=True)

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(10, 8))

# Determine the colors for the bars based on the relative difference values
bar_colors = ['#ffb6c1' if x < 0 else '#add8e6' for x in party_data_sorted['relative_difference']]

# Create the bar plot with different colors for positive and negative values
bars = ax.barh(party_data_sorted['primary_topic'], party_data_sorted['relative_difference'], color=bar_colors)

# Annotate the bars with the percentage values
for bar in bars:
    width = bar.get_width()
    label_x_pos = width if width > 0 else width - 5
    ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.0f}%', va='center')

# Set labels and title
ax.set_xlabel('Relative Difference (%)')
ax.set_title(f'Relative Difference in Topic Attention for {party}')

# Display the plot in the Streamlit app
st.pyplot(fig)

# Display sentences for selected topic
topic_list = party_data['primary_topic'].unique()
topic = st.sidebar.selectbox('Select a topic:', topic_list)
sentences = party_data[party_data['primary_topic'] == topic]['sentence']
st.write('Sentences:')
st.write(sentences)

# To run this Streamlit app, save the code in a file named, for example, `app.py`
# Then in your terminal, navigate to the directory where `app.py` is located and run:
# streamlit run app.py
