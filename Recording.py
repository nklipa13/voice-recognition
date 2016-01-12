from sys import byteorder
from array import array
from struct import pack

import wave
import pyaudio
import sys

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
RECORD_SECONDS = 3
THRESHOLD = 30

def normalize(snd_data):
    #pojacaj zvuk
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    #trazenje reci
    def _trim(snd_data):
        started = False
        r = array('h')
        for i in snd_data:
            if not started and abs(i)>THRESHOLD:
                started = True
                r.append(i)
            elif started:
                r.append(i)
        return r

    # levo
    snd_data = _trim(snd_data)

    # desno
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def record():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = array('h', stream.read(CHUNK))
        if byteorder == 'big':
            data.byteswap()
        frames.extend(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    frames = trim(frames)
    frames = normalize(frames)

    return p.get_sample_size(FORMAT), frames

def record_to_file(path):
    #"Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()