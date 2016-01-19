from sys import byteorder
from array import array
from struct import pack

import wave
import pyaudio
import sys
import os
import math

import scipy.io.wavfile as wav
from pydub import AudioSegment
import numpy as np

import matplotlib.pyplot as plt

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 3

def normalize(snd_data):
    #pojacaj zvuk
    MAXIMUM = 20384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = []
    for i in snd_data:
        r.append(int(i*times))
    return r

def detect_leading_silence(sound, chunk_size=10):
    
    # zvuk = [sound[i].dBFS for i in range(0, len(sound))]

    # plt.bar(range(0, len(zvuk)), zvuk)
    # plt.show()

    silence = [sound[i : i+chunk_size].dBFS for i in range(0, 140, chunk_size)]
    thresh = [np.mean([silence[i], silence[i+1], silence[i+2]]) for i in range(0, len(silence)-2)]

    maks = np.max(thresh)
    silence_threshold = maks / 2
        
    trim_ms = chunk_size # ms
    duration = len(sound)
    while True:
        t1 = trim_ms
        t2 = t1+chunk_size
        t3 = t2+chunk_size
        t4 = t3+chunk_size
                
        minimum = np.min([
            sound[t1:t2].dBFS,
            sound[t2:t3].dBFS,
            sound[t3:t4].dBFS
            ])
        if(minimum > silence_threshold):
            break
        trim_ms += chunk_size/2

        # infinite loop prevention
        if(t4 > duration):
            silence_threshold *= 1.5
            trim_ms = chunk_size

    return trim_ms

def trim(path, where):
    sound = AudioSegment.from_file(path, format="wav")

    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)    
    trimmed_sound = sound[start_trim:duration-end_trim]
    trimmed_sound= trimmed_sound.apply_gain(-trimmed_sound.max_dBFS)
    trimmed_sound.export(where, format="wav")

def record():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    for i in range(0, int(RATE / CHUNK * 0.5)):
            data = stream.read(CHUNK)

    print("* recording")

    frames = []
    # thresHelp = 0
    # for i in range(0, int(RATE / CHUNK * 0.1)):
    #     data = array('h', stream.read(CHUNK))
    #     if byteorder == 'big':
    #         data.byteswap()
    #     frames.extend(data)
    #     thresHelp+=data

    # THRESHOLD = thresHelp / (RATE / CHUNK * 0.1) * 2
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return p.get_sample_size(FORMAT), frames

def record_to_file(path, num):
    filename = path + ".wav"
    if (num==2):
        if not os.path.exists('dictionary/'+path):
            os.makedirs('dictionary/'+path)
        i = 0
        while os.path.exists("dictionary/" + path + '/' + ("%s_%s.wav" % (path, i))):
            i += 1
        filename = "%s_%s.wav" % (path, i)

    #"Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    if (num == 2):
        if not os.path.exists('original/'+path):
            os.makedirs('original/'+path)
        save_to_file("original/"+path+'/'+filename, data, sample_width)
        trim("original/"+path+'/'+filename, "dictionary/"+path+'/'+filename)
        #data = normalize(data)
        #save_to_file("dictionary/"+path+'/'+filename, data, sample_width)
    else:
        save_to_file("currentOriginal.wav", data, sample_width)
        trim("currentOriginal.wav", "current.wav")
        #data = normalize(data)
        #save_to_file("current.wav", data, sample_width)



def save_to_file(path, data, sample_width):
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data))
    wf.close()
