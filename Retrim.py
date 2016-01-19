from Recording import trim, normalize, save_to_file
import scipy.io.wavfile as wav
import os

path = "original/"
for foldername in os.listdir(path):
	if not os.path.isdir(path+foldername):
		continue
	if not os.path.exists('dictionary/'+foldername):
		os.makedirs('dictionary/'+foldername)

	for filename in os.listdir(path+foldername):
		if not filename.endswith('.wav'):
			continue
		trim(path+foldername+'/'+filename, "dictionary/"+foldername+'/'+filename)

	print(foldername)