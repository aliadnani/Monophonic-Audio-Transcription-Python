import scipy
import scipy.io.wavfile
import plotly

import cufflinks as cf
import plotly.express as px
import plotly.offline
import plotly.graph_objects as go
import psutil

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

wavFileSampleRate,wavFileSamples = scipy.io.wavfile.read('majorChord.wav')

wavFileSamplesLR = [((x[0] + x[1]) / 2) for x in wavFileSamples]

print(wavFileSamples)

fig = px.scatter(y=wavFileSamplesLR, x=range(len(wavFileSamplesLR)))
fig.show()