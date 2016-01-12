import sys
import os

from MFCC import mfcc
from MFCC import logfbank
import scipy.io.wavfile as wav

from Recording import record_to_file

record_to_file('current.wav')

#finished recording

path = '/dictionary'

for filename in os.listdir(os.getcwd()+path):
  print(filename)

#list all files from dictionary

(rate,sig) = wav.read("current.wav")
mfcc_feat = mfcc(sig,rate)
fbank_feat = logfbank(sig,rate)

print (fbank_feat[1:3,:])


