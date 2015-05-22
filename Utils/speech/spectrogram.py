from pylab import *
import wave
import sys
import struct

# open the wave file
fp = wave.open(sys.argv[1],"rb")

binData = fp.readframes(fp.getnframes())

binData = array(struct.unpack("%dB"%(len(binData)), binData),Float)-128

(Pxx, freqs, bins, im) = specgram(binData,NFFT=4096)
show()
