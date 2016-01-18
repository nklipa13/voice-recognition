import sys
import os
import pickle

from MFCC import mfcc
import scipy.io.wavfile as wav

from Recording import record_to_file

with open('database/dictionary.pkl', 'rb') as input:
        dictionary = pickle.load(input)

record_to_file('current', 1)

(rate,sig) = wav.read("current.wav")
mfcc_feat = mfcc(sig,rate)

#finished recording
scores = {}
print (len(dictionary))
for name, hmmModel in dictionary.items():
	score = hmmModel.score(mfcc_feat)
	scores[name] = score

predictedlabel, prob = max(scores.items(), key=lambda x:x[1])

print (predictedlabel)
print (prob)
#list all files from dictionary





