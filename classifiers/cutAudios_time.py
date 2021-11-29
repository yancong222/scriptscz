# launch libraries
import numpy as np
import pandas as pd
import re
import string
import os
import math
import shutil, sys

# mount google drive
# speech aligned with Montreal Forced Aligner
from google.colab import drive 
drive.mount('/content/gdrive/') 
drive_data_path = '/content/gdrive/My Drive/your.pipeline/'
mfa_dir = '/content/gdrive/My Drive/your.pipeline/mfa/'
drive_trancript_in_path = drive_data_path + "transcripts/"
cut_audio_dir = mfa_dir + "audio_cut/"

# prep text and audio
all_txt_files = os.listdir(drive_trancript_in_path)
all_audio_files = os.listdir(mfa_dir + '00_0_audio_raw/')

# !pip install ffmpeg-python
import ffmpeg
from sys import argv

# cut 1 participant-audio into multiple audios based on time stamp (~36s / audio)
def make_time(elem):
    t = elem.split(':')
    try:
        return int(float(t[0])) * 60 + float(t[1])
    except IndexError:
        return float(t[0])

def collect_from_file():
    time_pairs = []
    with open(drive_trancript_in_path + _in_txt) as in_times:
        for l, line in enumerate(in_times):
            tp = line.strip('\n').split('\t')
            print('here: ', tp)
            tp[0] = make_time(tp[2])
            print('flag: ', tp[0])
            tp[1] = make_time(tp[3]) - tp[0]
            print('flag2: ', tp[1])
            # if no name given, append line count
            if len(tp) < 3:
                tp.append(str(l) + '.wav')
            time_pairs.append(tp)
    return time_pairs

def main():
    for i, tp in enumerate(collect_from_file()):
        try:
            stream = ffmpeg.input(mfa_dir + '00_0_audio_raw/' + _in_file, ss=tp[0], t=tp[1])
            stream = ffmpeg.output(stream, _in_file.split('.')[0] + '_' + str(i) + '.wav')

            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

        except ffmpeg.Error as e:
              print('stdout:', e.stdout.decode('utf8'))
              print('stderr:', e.stderr.decode('utf8'))
              raise e
        
        shutil.move('/content/' + _in_file.split('.')[0] + '_' + str(i) + '.wav', cut_audio_dir) 


# go through all transcript files
for audio in all_audio_files:
  _in_file = audio 

  for txt in all_txt_files:
    if txt.split('.')[0] == _in_file.split('.')[0]:
      _in_txt = txt

      if __name__ == '__main__':
          main()

# cut 1 participant-transcript into multiple txt based on time stamp (~3s / txt)
l = -1
for audio in all_audio_files:
  _in_file = audio 
  for txt in all_txt_files:
    if txt.split('.')[0] == _in_file.split('.')[0]:
      _in_txt = txt
      with open(drive_trancript_in_path + _in_txt) as tfile:
          row = tfile.readlines()
          for r in row:
            l += 1 
            file_name = txt.split('.')[0] + '_' + str(l) + '.txt'
            with open(file_name, 'w') as f:
                f.write(r.split('\t')[-1])
                  
            shutil.move('/content/' + file_name, mfa_dir + '00_2_txt_cut/')                                               
