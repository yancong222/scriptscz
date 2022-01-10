#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:27:48 2021

@author: yancong
"""

import os
import os.path
import csv
import shutil

audio_path='/your/audio/path'
output_path='dir_opensmile_output'
audio_list=os.listdir(audio_path)
for audio in audio_list:
    if audio[-4:]=='.wav':
        this_path_input=os.path.join(audio_path,audio)
        this_path_output=os.path.join(output_path, audio[:-4]+'.csv')
        
        
        cmd='/Users/xyz/opensmile-master/build/progsrc/smilextract/SMILExtract -C ./Desktop/opensmile-master/config/myIS13_ComParE_8K.conf -I '+this_path_input
        
        os.system(cmd)
        
        file1 = open(audio[:-4]+'.csv', "w")
        
        with open('output.lld.csv', mode='r', newline = '') as f:
            for l in csv.reader(f): 
                toFile = 'unknown'.join(l)
                #print(type(toFile), toFile)
                file1.write(toFile + '\n')
                
                
            
            file1.close()
            
            shutil.move("/Users/xyz/" + audio[:-4]+'.csv', output_path)
            
            os.remove("/Users/xyz/" + 'output.lld.csv')
            
