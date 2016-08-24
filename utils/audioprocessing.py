'''
@author: Sebastian Lapuschkin
@maintainer: Sebastian Lapuschkin
@contact: sebastian.lapuschkin@hhi.fraunhofer.de
@date: 23.08.2015
@version: 0.0
@copyright: Copyright (c) 20165, Sebastian Lapuschkin
@license : BSD-2-Clause
'''


import scipy.io.wavfile as wavfile
import numpy as np

def stft(samples, framesize = 512,step = 64, windowfxn = np.hanning):
    '''
    Computes the short time fourier transform of a given single channel wav signal.

    Parameters:
    -----------
        samples : numpy.ndarray
            samples.shape should be (N,) with N being the number of discrete values

        framesize : int
            default = 512
            the window size of a time frame to process via fft

        step : int
            default = 64
            the offset between two consecutive time windows

        windowfxn : function
            default = numpy.hanning. CURRENTLY INACTIVE. IDENTITY FUNCTION IS USED!!!
            A wave function for weighting the samples of a time window for a smoother frequency spectrum

        Returns:
        --------
            frequencies : [numpy.ndarray]
            A list of length floor((N-framesize)/step), containing the complex valued frequency spectrum
            of each transformed time window as a numpy.ndarray of shape (framesize,)
    '''

    #weighted window function
    #Ww = windowfxn(framesize+1)[:-1] #with the +1 [:-1] the reconstruction is supposedly better...
    Ww = 1 #don't fuck around with this for now.
    return [np.fft.fft(Ww * samples[offset:offset+framesize]) for offset in xrange(0,len(samples)-framesize,step)]

def istft(frequencies, step=64, windowfxn = np.hanning, dtype = None):
    '''
    Computes the inverse short time fourier transform from a given sequence of frequencies and restores the described wav signal

    Parameters:
    -----------
    frequencies: [numpy.ndarray]
        a list of N complex valued numpy arrays containing the frequency spectrums of consecutive time windows.

    step : int
        default = 64
        the offset in amount of samples between the fourier-transformed input frequency spectra

    windowfxn : function
        default = numpy.hanning. CURRENTLY INACTIVE. IDENTITY FUNCTION IS USED!!!
        A wave function for weighting the samples of a time window for a smoother recovery frequency spectrum
        This should be the same wave function as used during the stft

    dtype : a numpy data type constant
        default = None
        defines the target data type of the output wave signal. The default value None returns the wav samples
        as directly restored by the ISTFT algorithm, i.e samples.dtype = numpy.float64.
        However, due to residual reconstruction errors very small deviations from the original signal might be
        the result, resulting in strong auditory noise due to noisy high frequency content being embedded.
        A Recommended value for dtype would be numpy.int16

    Returns:
    --------
        samples : np.ndarray
            the restored wav signal as a numpy array of shape (N,)

    '''

    N = len(frequencies)
    framesize = frequencies[0].shape[0]
    T = framesize + N * step

    #Window weight
    #Ww = windowfxn(framesize+1)[:-1] #with the +1 [:-1] the reconstruction is supposedly better...
    Ww = 1 #still do not fuck with the window scaling

    #to be reconstructed        #weighting envelope for scaling as post processing
    samples = np.zeros((T,));    env = np.zeros_like(samples)

    for i,offset in enumerate(range(0,len(samples)-framesize,step)):
        samples[offset:offset+framesize] += np.real(np.fft.ifft(frequencies[i]))
        env[offset:offset+framesize] += Ww

    env[env == 0] = 1 # avpoid zero division
    samples = samples / env #normalize

    #data type conversion
    if not dtype == None: # None = 'leave it as is, e.g. float64 most probably'
        samples = samples.astype(dtype)

    return samples




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
    resample = istft(raw_frequency_data,step)
    resample_tenth = istft([raw_frequency_data[i]/10. for i in xrange(len(raw_frequency_data))],step)

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



