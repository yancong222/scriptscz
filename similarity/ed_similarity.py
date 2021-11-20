# -*- coding: utf-8 -*-
"""yan cong ed_similarity.py

# Mount google dirve
"""

#Mounting G-Drive and reading in libraries
from google.colab import drive
drive.mount('/content/drive')

#import libraries
import numpy as np
import pandas as pd
import re
import string
import os
import math
import torch
import csv
import torch

#set variables for folder names:
datain = '/content/drive/My Drive/.../'
dataout = '/content/drive/My Drive/.../' #make sure dir starts with /

"""# Explore data"""

df_datain = pd.read_csv(datain + 'test.csv')
df_datain.head(5)

"""# Trasnformers similarity scores"""

!pip install transformers

!pip install sentencepiece

from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration, T5Model
T5_PATH = "t5-small" # "t5-small", "t5-base", "t5-large" [the best a GPU-computer can do, very slow], "t5-3b", "t5-11b"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 

t5_tokenizer = T5Tokenizer.from_pretrained(T5_PATH)
#what is t5 tokenizer doing todo
t5_config = T5Config.from_pretrained(T5_PATH)
t5_mlm = T5ForConditionalGeneration.from_pretrained(T5_PATH, config=t5_config).to(DEVICE)

type(t5_tokenizer) #it's not working if it's nonetype; try restart runtime

"""## clean dataset"""

df_sent = pd.read_csv(datain + 'test.csv')
taskin = ['test']
timepointin = ['BL']
speakerin = ['Subject']
df_sent = df_sent[df_sent['task'].isin(taskin)]
df_sent = df_sent[df_sent['timepoint'].isin(timepointin)]
df_sent = df_sent[df_sent['speaker'].isin(speakerin)]

df_sent = df_sent[df_sent['n_words'] > 3]

df_sent['t5small_similarity'] = ""

df_sent.head(5)

def clean_verbatim(content):
  for s in content.split(' '):
    #print(s)
    if s.endswith('-') or s.lower() in interjections:
      content = content.replace(s, '')
      content = " ".join(content.split())
  return content

df_sent['content'].replace(r'=','', inplace=True)
df_sent['content'].replace(r'\'=', '', inplace=True)
df_sent['content'].replace(r'\^', '', inplace=True)
df_sent['content'].replace(r'\+', '', inplace=True)
df_sent['content'].replace(r'\#', value='', inplace=True, regex = True)

df_sent['content'].replace(r'\{[A-Za-z]+\}', value='', inplace=True, regex = True)
df_sent['content'].replace(r'\(\([A-Za-z\s]+\)\)', value='', inplace=True)

df_sent['content'] = df_sent['content'].apply(lambda x: clean_verbatim(x))

df_sent.to_csv(datain + 'testcsv')

"""# Run encoder-decoder for adjacent sent
## similarity: sent
"""

df_sent = pd.read_csv(datain + 'test.csv')
for i in df_sent.index:
  text = df_sent['content'][i]
  text = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', text) #replace ' .' with '.'
  df_sent['content'][i] = text

df_sent.tail()

buglst = {}
for i,r in df_sent.iterrows():
  if r['speaker'] != 'Interviewer':
    try:
      seq1 = r['content']
      #print('seq1: ', seq1)

      seq2 = df_sent['content'][i+1]
      #print('seq2: ', seq2)

      similarity_prob = "stsb sentence1: " + seq1 + " sentence2: " + seq2
      print('sentence pair: ', similarity_prob) 
                            
      encoded = t5_tokenizer.encode(similarity_prob, return_tensors="pt").to(DEVICE)
      outputs2 = t5_mlm.generate(encoded)
      similarity_rating = t5_tokenizer.decode(outputs2[0], skip_special_tokens=True)
      print("similarity: ", similarity_rating)

      df_sent['t5small_similarity'][i+1] = similarity_rating
    except KeyError:
      buglst[df_sent['Unnamed: 0'][i]] = df_sent['content'][i]
      continue

buglst 

df_sent.to_csv(dataout + 'test.csv')

"""## cumulative centroid"""
