# -*- coding: utf-8 -*-
"""yan cong mlm_similarity.py

# Mount google drive
"""

from google.colab import drive
drive.mount('/content/drive/')

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
import tensorflow as tf

from torch import tensor

#set variables for folder names:
datain = '/content/drive/My Drive/.../'
dataout = '/content/drive/My Drive/.../' #make sure dir starts with /

"""# Check GPU availability"""

#%% check if GPU is active
torch.cuda.is_available() #True
print(torch.cuda.device_count()) #1
# setting device on GPU if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()

#Additional Info when using cuda
if device.type == 'cuda':
    print(torch.cuda.get_device_name(0)) #NVIDIA GeForce RTX 2080
    print('Memory Usage:')
    print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
    print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')

"""# Launch transformers"""

!pip install transformers

!pip install sentence-transformers

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('stsb-roberta-large')
type(model) #sentence_transformers.SentenceTransformer.SentenceTransformer

"""# Adjacent sent"""

df_sent = pd.read_csv(datain + 'test.csv')
df_sent = df_sent.rename(columns={'t5small_similarity': 'roberta_similarity'})
df_sent.head(5)

df_sent.head(5)

buglst = {}
for i,r in df_sent.iterrows():
  if r['speaker'] != 'Interviewer':
    try:
      sentence1 = r['content']
      sentence2 = df_sent['content'][i+1]

      # encode sentences to get their embeddings
      embedding1 = model.encode(sentence1, convert_to_tensor=True)
      embedding2 = model.encode(sentence2, convert_to_tensor=True)
      # compute similarity scores of two embeddings
      cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
      print("Sentence 1:", sentence1)
      print("Sentence 2:", sentence2)
      print("Similarity score:", cosine_scores.item())

      df_sent['roberta_similarity'][i+1] = cosine_scores.item()

    except KeyError:
      buglst[df_sent['Unnamed: 0'][i]] = df_sent['content'][i]
      continue


df_sent.to_csv(dataout + 'test.csv')

df_sent = pd.read_csv(dataout + 'test.csv')

"""# Centroid: cos_sim
# Get Centroid (average weighted vector, by file)
# Takes in embeddings for each file
"""

df_sent = pd.read_csv(dataout + 'test.csv')

df_sent['centroid'] = ''
df_sent['cos_centroid'] = ''
flag = 0

def mean_sentence(embedding):
  avg_emb = torch.mean(torch.stack(embedding), dim=0)
  return avg_emb

def cos_sent_centroid(sent_emb, centroid):
  cos = util.pytorch_cos_sim(sent_emb, centroid)
  return cos.item()

buglst = {}

lst = []
for i,r in df_sent.iterrows():
  try:
    if i < 5473:
      if df_sent['task'][i] == df_sent['task'][i+1]:
        text = r['content']
        print('text: ', text)

        # encode sentences to get their embeddings
        embedding_i = model.encode(text, convert_to_tensor=True)
        print('current sent: ', embedding_i)
        lst.append(embedding_i)

        flag += 1

      else:
        end_text = r['content']
        print('end text: ', end_text)
        end_embedding_i = model.encode(end_text, convert_to_tensor=True)
        print('current end sent: ', end_embedding_i)
        lst.append(end_embedding_i)
        flag += 1

        text_emb_mean = mean_sentence(lst)
        df_sent['centroid'][i] = text_emb_mean
        print('text_emb_mean: ', text_emb_mean, type(text_emb_mean), text_emb_mean.shape)

        for line in range(flag):
          print('match: ', lst[line])
          df_sent['cos_centroid'][(i+1)-flag+line] = cos_sent_centroid(lst[line], df_sent['centroid'][i])
          print('flag: ', flag, 'i: ', i, 'line: ', line, 'current: ', i+1-flag+line)
        
        lst = []
        flag = 0

    elif i == 5474:
      text_emb_mean = mean_sentence(lst)
      df_sent['centroid'][i] = text_emb_mean

  except:
    buglst[df_sent['Unnamed: 0'][i]] = df_sent['content'][i]
    continue

df_sent.head()

buglst

df_sent.to_csv(dataout + 'test.csv')
