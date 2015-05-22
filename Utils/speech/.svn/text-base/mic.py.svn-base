""" Record a few seconds of audio and save to a WAVE file. """
import pyaudio
import wave
import sys
import struct

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output_%d.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

all = []
recording = 0
thisWord = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
	
    data = stream.read(chunk)
    avg = sum(struct.unpack("%dB"%(25), data[:25]))/25
    print avg
    if avg > 60:
    	recording = 10
        thisWord.append(data)
    	print "Recording"
    	
    elif recording > 0 :
    	thisWord.append(data)
    	
    	if recording == 1:
    		print "Stop Recording"
    		all.append(thisWord)
    		thisWord = []
    		recording -= 1
    	else:
    	   recording -= 1


stream.close()
p.terminate()

# write data to WAVE file
for i,word in enumerate(all):
	data = ''.join(word)
	wf = wave.open(WAVE_OUTPUT_FILENAME % (i), 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(data)
	wf.close()
