'''
@author: Sebastian Lapuschkin
@maintainer: Sebastian Lapuschkin
@contact: sebastian.lapuschkin@hhi.fraunhofer.de
@date: 24.08.2015
@version: 0.0
@copyright: Copyright (c) 20165, Sebastian Lapuschkin
@license : BSD-2-Clause
'''

import scipy.io.wavfile as wavfile
import numpy as np
import audioprocessing

framesize = 512
step = 16

wavpath = '/media/lapuschkin/Data/AUDIO-LRP/free-spoken-digit-dataset/recordings_8000/0_jackson_10.wav'
samplerate,samples = wavfile.read(wavpath) #dtype of samples is int16
T = len(samples)
raw_frequency_data =    audioprocessing.stft(samples,framesize,step)
resample =              audioprocessing.istft(raw_frequency_data,step,dtype=np.int16)
resample_tenth =        audioprocessing.istft([raw_frequency_data[i]/10. for i in xrange(len(raw_frequency_data))],step,dtype=np.int16)
resample_three =        audioprocessing.istft([raw_frequency_data[i]*3 for i in xrange(len(raw_frequency_data))],step,dtype=np.int16)
wavfile.write('original.wav', samplerate, samples)
wavfile.write('restored.wav', samplerate, resample)
wavfile.write('restored_tenth.wav', samplerate, resample_tenth)
wavfile.write('restored_three.wav', samplerate, resample_three)


freqmat = audioprocessing.samples2freqmat(samples, framesize, step )
restoration =  audioprocessing.freqmat2samples(freqmat,step,dtype=np.int16)
wavfile.write('matrix_restored.wav',samplerate,restoration)
print 'done' # RESTORATION DIFFERS FROM RESAMPLE: FIND OUT WHY . HAS TO DO WITH FREQ -> WAV


#NOTE HERE:
        # real(tspectrum[x]) == real(tspectrum[-x])
        # BUT
        # imag(tspectrum[x]) == - imag(tspectrum[-x])
        # use this knowledge somehow? compress the data with that, later reconstruct? gotta pee.
print 'DURING POST PROCESSING FEATURE EXTRACTION:'
print '- crop negative frequencies?, restore later? what do the heatmaps say?' #maybe
print '- pad signal before spectrum analysis?' #no
print '- only compute spectrogram, save phase information for later recovery?' #maybe, kinda not
print '- linearly scaling the frequency == linearly scaling the samples by the same factor'
