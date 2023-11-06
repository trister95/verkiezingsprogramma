import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache
def load_data(filename):
    return pd.read_csv(filename)

df = load_data('outputs/csvs/parties_sentences_topics.csv')
metrics_df = load_data('outputs/csvs/metrics.csv')

party_list = df['party'].unique()
party = st.sidebar.selectbox('Select a party:', party_list)

party_data = df[df['party'] == party]
metrics_party_data = metrics_df[metrics_df['party'] == party]

st.write(f"Attention plot for {party}")

party_data_sorted = metrics_party_data.sort_values('relative_difference', ascending=True)

fig, ax = plt.subplots(figsize=(10, 8))

bar_colors = ['#ffb6c1' if x < 0 else '#add8e6' for x in party_data_sorted['relative_difference']]

bars = ax.barh(party_data_sorted['primary_topic'], party_data_sorted['relative_difference'], color=bar_colors)

for bar in bars:
    width = bar.get_width()
    label_x_pos = width if width > 0 else width - 5
    ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.0f}%', va='center')

ax.set_xlabel('Relative Difference (%)')
ax.set_title(f'Relative Difference in Topic Attention for {party}')

st.pyplot(fig)

topic_list = party_data['primary_topic'].unique()
topic = st.sidebar.selectbox('Select a topic:', topic_list)
sentences = party_data[party_data['primary_topic'] == topic]['sentence']
st.write('Sentences:')
st.write(sentences)
