import os
import pandas as pd
import tqdm
from transformers import pipeline
from folia.main import folia

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
  """ 
  List all .folia.xml files in a  directory.
  """
  folia_files = []
  for filename in os.listdir(directory):
    if filename.endswith('folia.xml'):
      folia_files.append(filename)
  return folia_files