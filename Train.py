from scipy.io import wavfile
from hmmlearn import hmm

from MFCC import mfcc
import numpy as np
import pickle
import sys
import os
import scipy.io.wavfile as wav

dictionary = {}

if (len(sys.argv) == 1):
    path = "dictionary/"
    for foldername in os.listdir(path):
        if not os.path.isdir(path+foldername):
            continue
        trainingData = []
        for filename in os.listdir(path+foldername):
            (rate,sig) = wav.read(path+foldername+'/'+filename)
            mfcc_feat = mfcc(sig,rate)
            trainingData.append(mfcc_feat)
        model = hmm.GMMHMM(n_components = len(foldername)*2, n_mix = len(foldername)*2, \
                           covariance_type='diag', n_iter = 10)
        model.fit(trainingData) 
        dictionary[foldername] = model
        print (foldername)
else:
    with open('database/dictionary.pkl', 'rb') as input:
        dictionary = pickle.load(input)
    foldername = str(sys.argv[1])
    path = "dictionary/" + foldername
    trainingData = []
    for filename in os.listdir(path):
        (rate,sig) = wav.read(path+'/'+filename)
        mfcc_feat = mfcc(sig,rate)
        trainingData.append(mfcc_feat)
    model = hmm.GMMHMM(n_components = len(foldername)*2, n_mix = len(foldername)*2, \
                       covariance_type='diag', n_iter = 10)
    model.fit(trainingData) 
    dictionary[foldername] = model

with open('database/dictionary.pkl', 'wb') as output:
    pickle.dump(dictionary, output, pickle.HIGHEST_PROTOCOL)