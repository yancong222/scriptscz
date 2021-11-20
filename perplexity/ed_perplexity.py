# -*- coding: utf-8 -*-
""" yan cong ed_perplexity.py
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

#set variables for folder names:
datain = '/content/drive/My Drive/.../'
dataout = '/content/drive/My Drive/.../' #make sure dir starts with /

!pip install git+https://github.com/huggingface/transformers
!pip install sentencepiece

from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration, T5Model

T5_PATH = "t5-small" # "t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b"

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 

t5_tokenizer = T5Tokenizer.from_pretrained(T5_PATH)
t5_config = T5Config.from_pretrained(T5_PATH)
t5_mlm = T5ForConditionalGeneration.from_pretrained(T5_PATH, config=t5_config).to(DEVICE)

type(t5_tokenizer) #it's not working if it's nonetype

df_sent = pd.read_csv(datain + 'test.csv')
df_sent.head(5)

firstrun = []
loss_scz = []
t = 0
l = 0

with open(datain + 'test.csv', newline='') as f:
    reader = csv.DictReader(f)
    for line in reader:
      loss_scz = []
      content = line['content']
      #print(content)
      if line['uid'] not in firstrun:
        for w in content.split(' '):
          target_scz = w
          #print(target_scz)
          if target_scz in content.split(' '):
            sentence = content.replace(target_scz, '<extra_id_0>', 1)
            #print(sentence) #testing
            input_ids = t5_tokenizer(sentence, return_tensors='pt').input_ids.to(DEVICE)
            labels_scz = t5_tokenizer('<extra_id_0> ' + target_scz + ' <extra_id_1> </s>', return_tensors='pt').input_ids.to(DEVICE)                              
            outputs_scz = t5_mlm(input_ids = input_ids, labels = labels_scz)       
            loss_scz.append(outputs_scz.loss)
            #print('loss: ', loss_scz, 'minimum: ', min(loss_scz), 'average: ', sum(loss_scz)/len(loss_scz))
        with open (dataout + 'test.csv', 'a', newline='') as f2:
          l += 1
          t = 0
          writer = csv.writer(f2)

          for j,w in zip(loss_scz, line['content'].split( )):
            t += 1
            writer.writerow([line['grid'], line['speaker'], line['sentence_id'], line['task'],
                            line['n_words'], line['timepoint'],
                            T5_PATH, l, line['content'], t, w, j,
                            min(loss_scz), max(loss_scz),
                            sum(loss_scz)/len(loss_scz)]) # add task col to sentence_agg

df_sent_loss.to_csv(dataout + 'test.csv')
