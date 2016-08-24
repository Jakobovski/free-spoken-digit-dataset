
import scipy.io.wavfile as wavfile
import numpy as np

def stft(samples, framesize = 512,step = 64,windowfxn = np.hanning):
    print framesize, step
    #Window weight
    #Ww = windowfxn(framesize+1)[:-1] #with the +1 [:-1] the reconstruction is supposedly better...
    Ww = 1 #don't fuck around with this for now.'
    return [np.fft.fft(Ww * samples[offset:offset+framesize]) for offset in xrange(0,len(samples)-framesize,step)]

def istft(frequencies, T = None, step=64, windowfxn = np.hanning):
    N = len(frequencies)
    framesize = frequencies[0].shape[0]
    if T is None: T = framesize + N * step

    #Window weight
    #Ww = windowfxn(framesize+1)[:-1] #with the +1 [:-1] the reconstruction is supposedly better...
    Ww = 1 #still do not fuck with the window scaling

    #to be reconstructed        #weighting envelope for scaling as post processing
    samples = np.zeros((T,));    env = np.zeros_like(samples)

    for i,offset in enumerate(range(0,len(samples)-framesize,step)):
        samples[offset:offset+framesize] += np.real(np.fft.ifft(frequencies[i]))
        env[offset:offset+framesize] += Ww

    env[env == 0] = 1 # avpoid zero division
    return samples/env


def wav2png(wavpath,pngpath=None, framesize = 512, step = 64, windowfxn = np.hanning, layer3constant = 0):
    '''
    Computes a complex-valued spectrogram from the wav file specified by wavpath,
    where
        the R-layer of the output png holds the real valued spectrum,
        the G-layer of the output png holds the imaginarily valued spectrum,
        and the B-layer is constantly 0

        framesize is the time frame to consider
        spectrogram_dim is the number of time and frequency steps to output.
        step controls the overlap of time frames to spectrograph.
        windowfxn defines a window of weights applied to the raw singal for a smoother transition and later easier reconstruction

        returns the image and a parameter dictionary
    '''

    samplerate,samples = wavfile.read(wavpath) #dtype of samples is int16
    T = len(samples)
    frequency_data = np.zeros((framesize,framesize,3));
    # some debugging values for myself.
    #overlap = (framesize - step + 0.0) / framesize
    #framesize = double the extractable frequency spectrum?
    #how does that relate to - with the signal - the output dims (how much signal can we get, what needs to be padded?)

    raw_frequency_data = stft(samples, framesize,step,windowfxn)
    resample = istft(raw_frequency_data,T,step)
    resample_tenth = istft([raw_frequency_data[i]/20. for i in xrange(len(raw_frequency_data))],T,step)

    #wavfile.write('original.wav', samplerate, samples)
    #wavfile.write('restored.wav', samplerate, resample.astype(np.int16)) # ROUNDING TO INT IS FUCKING IMPORTANT: DENOISING DELUXE!!!
    #wavfile.write('restored_tenth.wav', samplerate, resample_tenth.astype(np.int16)) # FREQUENCY MUTING ON LOG SCALE WITH HEATMAPS?



    #AS IMAGES BELOW HERE
    #print 'debug'
    #print '...'

    #for i in xrange(len(raw_frequency_data)):
    #    tspectrum = raw_frequency_data[i]

    #    frequency_data[:,i,0] = np.real(tspectrum)
    #    frequency_data[:,i,1] = np.imag(tspectrum)
    #    frequency_data[:,i,2] = layer3constant

        #NOTE HERE:
        # real(tspectrum[x]) == real(tspectrum[-x])
        # BUT
        # imag(tspectrum[x]) == - imag(tspectrum[-x])
        # use this knowledge somehow? compress the data with that, later reconstruct? gotta pee.



wavpath = '/media/lapuschkin/Data/AUDIO-LRP/free-spoken-digit-dataset/recordings/0_jackson_10.wav'
wav2png(wavpath)