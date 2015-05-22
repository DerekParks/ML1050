"""
waveToCSV posDir negDir outputFile nFFT imageWidth imageHeight

posDir - dir full of + class wav files
negDir - dir full of - class wav files
nFFT - the length of the FFT per col in the spectragram
imageWidth - the spectragram will be averaged to have this many pixels in the width
imageHeight - the spectragram will be averaged to have this many pixels in the height

"""

from Numeric import *
from MLab import *
from FFT import *
from pylab import *
import wave
import sys
import struct
import csv
import os
from random import shuffle


def waveToImage(filename, fft_length =256, imageWidth = 10, imageHeight = 10):
    """
    Takes a wav file and returns an averaged spectragram
    """

    # open the wave file
    fp = wave.open(filename,"rb")
    sample_rate = fp.getframerate()
    total_num_samps = fp.getnframes()
    num_fft = (total_num_samps / fft_length ) - 2

    # create temporary working array
    temp = zeros((num_fft,fft_length),Float)

    # read in the data from the file
    for i in range(num_fft):
        tempb = array(struct.unpack("%dB"%(2*fft_length), fp.readframes(fft_length)),Float)

        #samples alternate between left and right tracks
        tempbL = zeros(fft_length)
        tempbR = zeros(fft_length)
        for j in range(fft_length):
            tempbL[j] = tempb[2*j] -128
            tempbR[j] = tempb[2*j+1] -128

        temp[i,:] = tempbL
    fp.close()


    # Window the data
    temp = temp * hamming(fft_length)

    # Transform with the FFT, Return Power
    freq_pwr  = 10*log10(1e-20+abs(real_fft(temp,fft_length)))

    subSampleDims = (imageWidth, imageHeight)
    subSamples = zeros(subSampleDims,Float)

    steps= (freq_pwr.shape[0]/(subSampleDims[0]) , freq_pwr.shape[1]/(subSampleDims[1]) ) 

    print freq_pwr.shape, steps, subSampleDims

    #average the data into subSamples
    for i in range(subSampleDims[0]):
        for j in range(subSampleDims[1]):

            iStart = i*steps[0] 
            if i!=subSampleDims[0]-1:
                iStop = (i+1)*steps[0]
            else:
                iStop = -1

            jStart = j*steps[1]
            if j!=subSampleDims[1]-1:
                jStop = (j+1)*steps[1]
            else:
                jStop = -1
            #get a subsqaure of the image
            subSqaure = freq_pwr[iStart:iStop , jStart:jStop]
            #avg all values in the subsquare
            subSamples[i,j] = average(reshape(subSqaure , (1, subSqaure.shape[0] * subSqaure.shape[1] )) [0] )
    return subSamples


def dirToLists(theDir, label, fft_length =256, imageWidth = 10, imageHeight = 10):
    """
    Do an entire dir of wav files
    """
    result = []
    for root, dirs, files in os.walk(theDir):
        for name in files:
            imagePixels = waveToImage(os.path.join(root,name), fft_length, imageWidth, imageHeight)
            result.append(reshape(imagePixels, (1, imageWidth * imageHeight) )[0].tolist()) #turn image Pixles into vector, then to list
            result[-1].insert(0,label) #add the class label
    return result

def showImage(pixels):
    """
    Look at an array of pixels
    """
    imshow(pixels, extent=[-1,1,-1,1],cmap=cm.jet)
    show()

def main ():
    print sys.argv
    if len(sys.argv) != 7:
        print __doc__
        sys.exit(2)

    posDir = sys.argv[1]
    negDir = sys.argv[2]
    outFile = sys.argv[3]
    nFFT = int(sys.argv[4])
    imageW = int(sys.argv[5])
    imageH = int(sys.argv[6])
    csvRows = []
   
    csvRows.extend(dirToLists(posDir, 1, nFFT, imageW, imageH))
    csvRows.extend(dirToLists(negDir, 0, nFFT, imageW, imageH))
    shuffle(csvRows)
    
    writer = csv.writer(open(outFile, "wb"))
    writer.writerows(csvRows)


if __name__ == "__main__":
    try:
        __IP                           # Are we running IPython?
    except NameError:
        main()                         # If not, run the tests

