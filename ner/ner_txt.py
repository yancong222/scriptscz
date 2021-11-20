#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09 2021
@author: yancong
"""
#%%
import re
import csv
import glob
import pandas as pd

#%% extract alld the instances of squared brackets strings per line
df = pd.read_csv('test.txt', sep = "\t")
df.columns = ['l', 'num', 'grid', 'num1', 'task', 'speaker', 'content', 'unnamed']
df['ne'] = df['content'].str.findall(r"\[([A-Za-z~'.\- \s]+)\]") 
ne = []
for i in range(len(df['ne'])):
    try:
        ne += df['ne'][i]
    except TypeError:
        continue
ne_set = set(ne)

#%% ner 1 big txt file first run
import re
import csv
import glob

for filepath in glob.iglob('./**/*.txt', recursive=True):
    # entity set need to delete header
    # entity set need to insert ';' columns in between the existing columns
    if filepath != './test.csv': 
        print(filepath)
        with open(filepath) as file:
            s = file.read()
        with open('entity_set.csv') as f:
            for l in f.readlines():
                print(l.split(';')[1])
                if '[' not in l and ']' not in l:
                    s = s.replace(l.split(';')[0][0:-1], l.split(';')[1][1:-1])
                else:
                    s = s.replace(l.split(';')[0][1:-2], l.split(';')[1][2:-2])
                print(s)
        with open(filepath, "w") as file:
            file.write(s)     

#%% extract the first instance of named entities per line
df = pd.read_csv('test.txt', sep = "\t")

ne1 = []
start = 0
end = 0
for i in range(len(df['content'])):
    try:
        if '[' in df['content'][i] or ']' in df['content'][i]:
            start = df['content'][i].index('[') + 1
            end = df['content'][i].index(']')
            ne1.append(df['content'][i][start:end])
    except:
        print('flag: ', df['content'][i-1]) #nan
        continue

#%% second run
import re
import csv
import glob

with open('test.txt') as file:
    s = file.read()
    with open('entity_set.csv') as f:
        for l in f.readlines():
            print(l.split(';')[1])
            if '[' not in l and ']' not in l:
                s = s.replace(l.split(';')[0][0:-1], l.split(';')[1][1:-1])
            else:
                s = s.replace(l.split(';')[0][1:-2], l.split(';')[1][2:-2])
    with open('test.txt', "w") as file:
        file.write(s)          
        
#%% exclude unintelligibles but all int become floats
to_exclude = ['...']

dfr = pd.read_csv('test.txt', sep = "\t")
dfr.columns = ['l', 'num', 'grid', 'num1', 'task', 'speaker', 'content', 'unnamed']
for i in to_exclude:
    dfr = dfr.drop(dfr[dfr.grid == i].index)
dfr.to_csv('test.txt', sep='\t', 
           index=False, header=False, mode = 'a')

#%% #remove unintelligens
with open('test.txt') as file:
    s = file.read()
    for line in s.split('\n'):
        try:
            if line.split('\t')[2] in to_exclude:
                s = s.replace(line,'')
        except:
            print('flag: ', line) #empty line
            continue
            
with open('test.txt', "w") as file:
    file.write(s)        
#%%
