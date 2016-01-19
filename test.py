import sys
import os
import pickle

from MFCC import mfcc
import scipy.io.wavfile as wav
from Recording import trim

from Recording import record_to_file

with open('database/dictionary.pkl', 'rb') as input:
        dictionary = pickle.load(input)

path = "testing/"
pogodjeni = 0
ukupno = 0
for filename in os.listdir(path):
	ukupno+=1
	if not filename.endswith('.wav'):
		continue
	trim(path+filename, path+"help/"+filename)
	(rate,sig) = wav.read(path+"help/"+filename)
	mfcc_feat = mfcc(sig,rate)

	#finished recording
	scores = {}
	for name, hmmModel in dictionary.items():
		score = hmmModel.score(mfcc_feat)
		scores[name] = score

	predictedlabel, prob = max(scores.items(), key=lambda x:x[1])
	if (predictedlabel==os.path.splitext(filename)[0]):
		pogodjeni += 1

	print (os.path.splitext(filename)[0] + "  on kaze:" + predictedlabel)
	#list all files from dictionary

print(pogodjeni/ukupno)





