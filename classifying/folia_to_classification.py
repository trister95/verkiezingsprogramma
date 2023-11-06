import os
import pandas as pd
import tqdm
from transformers import pipeline
import folia.main as folia

# Define tokenizer arguments
tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 512}

# Load the model and tokenizer
partypress = pipeline(
    "text-classification",
    model="partypress/partypress-monolingual-netherlands",
    tokenizer="partypress/partypress-monolingual-netherlands",
    **tokenizer_kwargs
)


def process_folia_file(file_path, party_name):
    doc = folia.Document(file=file_path)
    lst = []
    for paragraph in doc.paragraphs():
        for sentence in paragraph:
            lst.append(sentence.text())
            
    df_rows = []
    for sentence in tqdm.tqdm(lst):
        result = partypress(sentence)
        primary_topic = result[0]['label']
        if primary_topic != "98 - Non-thematic":  # Skip nonthematic sentences
            row = {'party': party_name, 'sentence': sentence, 'primary_topic': primary_topic}
            df_rows.append(row)
        
    return pd.DataFrame(df_rows)

def list_folia_files(directory):
    return [filename for filename in os.listdir(directory) if filename.endswith('folia.xml')]

def process_and_concat_files(folder):
    dfs = [process_folia_file(f"{folder}/{f}", f.replace('.folia.xml', '')) for f in list_folia_files(folder)]
    return pd.concat(dfs, ignore_index=True)

# Function to clean topic labels
def clean_topics(df):
    df['primary_topic'] = df['primary_topic'].str.replace('[\d.\-]', '', regex=True).str.strip()
    return df

# Function to calculate metrics
def calculate_metrics(df):
    # Grouping and calculating counts in one step
    grouped = df.groupby(['party', 'primary_topic']).size().reset_index(name='topic_count')
    total_sentences_per_party = grouped.groupby('party')['topic_count'].sum().reset_index(name='total_sentences')
    
    # Merging and calculating percentages
    merged = grouped.merge(total_sentences_per_party, on='party')
    merged['topic_percentage'] = ((merged['topic_count'] / merged['total_sentences']) * 100).round(1)
    
    # Calculating average percentage and relative difference
    average_topic_percentage = merged.groupby('primary_topic')['topic_percentage'].mean().reset_index(name='average_percentage').round(1)
    final = merged.merge(average_topic_percentage, on='primary_topic')
    final['relative_difference'] = ((final['topic_percentage'] - final['average_percentage']) / final['average_percentage'] * 100).round(0)
    
    return final