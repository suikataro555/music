import numpy as np
import scipy.io.wavfile as wav
import random
import simpleaudio as sa

def saveAsWav(output_file,waveform,sample_rate=44100):
  wav.write(output_file,sample_rate,waveform)

def getWave(frequency=400,duration=1,sample_rate=44100):
  t=np.linspace(0,duration,int(sample_rate*duration),endpoint=False)
  wave = np.sin(2*np.pi*frequency*t+2*np.pi*np.random.random(size=1))
  return wave

def comp(waveform,amplitude=1):
  waveform *= amplitude/max(waveform)

def play(waveform,sample_rate=44100):
  wave=np.int16(waveform*32767)
  play_obj = sa.play_buffer(wave,1,2,sample_rate)
  play_obj.wait_done()

def getPink(length):
  tmp = np.random.random(size=length)*2-1
  S=np.fft.rfft(tmp)
  fil = 1/(np.arange(len(S))+1)
  S*=fil
  s = np.fft.irfft(S)
  s /= np.max(np.abs(s))
  #print("(max,min) = (" + str(np.max(s)) + " , "+str(np.min(s)) + ")")
  return s

Freq = 220
num_waves = 20
waveforms = getWave()
for i in range(num_waves-1):
  frequency = random.randint(1,10)/random.randint(1,10)*Freq
  waveforms = np.vstack((waveforms,getWave(frequency)))

waveform = np.zeros(len(waveforms[0]))
for wave in waveforms:
  waveform += wave

waveform_out = waveform 

for i in range(50):
  waveform -= waveforms[i%num_waves]
  waveforms[i%num_waves] = getWave(frequency = random.randint(1,10)/random.randint(1,10)*Freq)
  waveform += waveforms[i%num_waves]
  waveform_out = np.append(waveform_out,waveform)

x=np.linspace(0,len(waveform_out),len(waveform_out),endpoint=False)
x/=len(x)
volume = 1.0+0.5*(np.sin(2*np.pi*x*6))
volume += 0.3*(np.sin(2*np.pi*x*3.5))
waveform_out *= volume

comp(waveform_out)
# noise = np.random.normal(loc=0,scale=0.07,size=len(waveform_out))
noise = getPink(len(waveform_out))
#noise=0
waveform_out += noise
comp(waveform_out,0.5)
play(waveform_out)

# Save wav format
saveAsWav('output.wav',waveform_out)