# Imports
import scipy.io.wavfile
import scipy.fftpack
import scipy.signal
import numpy as np



# Graph Imports
import cufflinks as cf
import plotly.express as px
import plotly.offline
import plotly.graph_objects as go
import psutil

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)



# Read Wav
def readMonoWAV(filename):
  wavFileSampleRate, wavFileSamplesLR = scipy.io.wavfile.read('lick.wav')
  wavFileSamplesLR = [((x[0] + x[1]) / 2) for x in wavFileSamplesLR]
  return (wavFileSampleRate, wavFileSamplesLR)

wavFileSampleRate, wavFileSamplesLR = readMonoWAV('lick.wav')

# # Show WAV
# waveformFig = px.scatter(y=wavFileSamplesLR, x=range(len(wavFileSamplesLR)))
# waveformFig.show()



print(len(wavFileSamplesLR))



timeStep = (1 / wavFileSampleRate)
chunkSize = int(wavFileSampleRate / 20 )
startChunk = 0
endChunk = startChunk + chunkSize
domFreqs = []
numSamp = len(wavFileSamplesLR)

activationLevel = max(wavFileSamplesLR) / 12

while (endChunk < numSamp):
    chkVol = np.array(wavFileSamplesLR[startChunk:endChunk])
    chkVol = np.absolute(chkVol)
    
    if (np.mean(chkVol) < activationLevel):
        startChunk = endChunk
        endChunk += chunkSize
        domFreqs.append(0.0)
        continue
    chunk = wavFileSamplesLR[startChunk:endChunk]
    chunkFFT = np.abs(scipy.fftpack.fft(chunk))
    chunkFFTFreqs = scipy.fftpack.fftfreq(int(len(chunkFFT)),d=timeStep)
    chunkFFTPos = chunkFFT[:int(abs(len(chunkFFT)))]

    FFTPeaksIdx, _ = scipy.signal.find_peaks(chunkFFTPos)
    FFTPeaks = [chunkFFTFreqs[x] for x in FFTPeaksIdx]
    domFreq = chunkFFTFreqs[np.argmax(chunkFFT)]
    domFreqs.append(domFreq)
    startChunk = endChunk
    endChunk += chunkSize

print(domFreqs)
# FFTFig = px.line(y=chunkFFTPos, x=chunkFFTFreqs)
# FFTFig.show()


# for 

# FFTPeaksFig = px.scatter(y=FFTPeaksY )




length = (chunkSize / wavFileSampleRate )

finalSin = []
sinArr = []
for frequency in domFreqs:
    t = np.linspace(0,length, wavFileSampleRate * length)  #  Produces a 5 second Audio-File
    y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz
    sinArr.append(y)

finalSin = np.concatenate(sinArr)
scipy.io.wavfile.write('lick_Sin.wav', wavFileSampleRate, finalSin)





