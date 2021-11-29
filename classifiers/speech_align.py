#author: Yan Cong

# launch libraries
import numpy as np
import pandas as pd
import re
import string
import os
import math
import csv
import shutil, sys 
import glob

# using google colab
# speech alignment with Montreal Forced Aligner (mfa)
# mfa outputs TextGrid, which is used for word-time based audio-text-TextGrid alignment

from google.colab import drive 
drive.mount('/content/gdrive/') 
root_dir = '/content/gdrive/My Drive/your.pipeline/mfa/'
for_align = root_dir + 'your.text/'
input_raw = root_dir + 'your.text.csv' # a big csv, text line by line, with time stamps

df = pd.read_csv(input_raw)
df.head()

with open(input_raw) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        file_name ='id_{0}_audio.txt'.format(row['your ID goes here']) 
        with open(file_name, 'w') as f:
          f.write(row['transcprit_by_phoneme'].strip('"'))            
        shutil.move('/content/' + file_name, for_align) # generate a txt file for each line in csv, prep for alignment

all_input_files = os.listdir(drive_trancript_in_path)

# Organization: move audios that have txt-audio match to another folder
source_folder = os.listdir(root_dir + 'your_audio/')
destination_folder = os.listdir(root_dir + 'your_audio_hastxt/')
for_align = os.listdir(root_dir + 'your_txt/')

files_to_move = []
for txt in for_align:
  for audio in source_folder:
    if txt.split('.')[0] == audio.split('.')[0]:
      files_to_move.append(audio)

# iterate files
for file in files_to_move:
    # construct full file path
    source = root_dir + 'your_audio/' + file
    destination = root_dir + 'your_audio_hastxt/' + file
    # move file
    shutil.move(source, destination)

# !pip install textgrid
# python pkg for textgrid processing
import textgrid
from textgrid import TextGrid

# You can test 1 file locally to see the data structure of a TextGrid
# Read a TextGrid object from a file.
tg = textgrid.TextGrid.fromFile('your_testing_audio.textgrid')
# Read a IntervalTier object.
print("------- IntervalTier Example -------")
with open('test.txt', 'w') as testing:
  for t in tg.tiers[0]:
    testing.writelines(str(t.minTime) + ' ' + str(t.maxTime) + ' ' + str(t.mark) + '\n')

# run through all the files
mfa_aligned = os.listdir(root_dir + 'your_aligned/') #type: list
for f in mfa_aligned:
    tg = textgrid.TextGrid.fromFile(root_dir + 'your_aligned/' + f)
    file_name = f.split('.')[0] + '.word' 
    with open(file_name, 'w') as o:
      for t in tg.tiers[0]:
        o.writelines(str(t.minTime) + ' ' + str(t.maxTime) + ' ' + str(t.mark) + '\n')
    shutil.move('/content/' + file_name, root_dir + 'your_aligned_word/')    # congrats! that's all for word alignment!








