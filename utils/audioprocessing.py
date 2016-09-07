'''
@author: Sebastian Lapuschkin
@maintainer: Sebastian Lapuschkin
@contact: sebastian.lapuschkin@hhi.fraunhofer.de
@date: 23.08.2015
@version: 0.0
@copyright: Copyright (c) 20165, Sebastian Lapuschkin
@license : BSD-2-Clause
'''

import numpy as np
import audioop

def stft(samples, framesize = 512,step = 16, windowfxn = np.hanning):
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
            default = 16
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

def istft(frequencies, step=16, windowfxn = np.hanning, dtype = None):
    '''
    Computes the inverse short time fourier transform from a given sequence of frequencies and restores the described wav signal

    Parameters:
    -----------
    frequencies: [numpy.ndarray]
        a list of N complex valued numpy arrays containing the frequency spectrums of consecutive time windows.

    step : int
        default = 16
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

def samples2freqmat(samples, framesize = 512, step = 16, windowfxn = np.hanning ):
    '''
    Computes a complex-valued spectrogram using short time fourier transform (stft) based on a
    wav file and produces a png file and stores the real and imaginary parts of the data as
    separate layers in matrix form.

    Parameters:
    -----------
        samples: numpy.ndarray
            the input sequence wav samples

        framesize: int
            default = 512
            the size of the sequency time frame to consider for stft.

        step: int
            default = 16
            the offset in number of samples between two consecutive frame windows used in stft

        windowfxn: function
            default = numpy.hanning
            CAUTION! NOT USED BY NEITHER STFT AND ISTFT CURRENTLY
            function for computing weights for the samples of each time window used in stft

    Returns:
    --------
        freqmat : numpy.ndarry
            Numpy array of shape (framesize,T,2)
            where framesize is the number of extracted frequencies, T is the number of transformed
            time steps and the third dimension indexing the real (index 0) and imaginary (index 1)
            components of the data.
            The order of the frequency components conforms to the implementation of numpy.fft.fft,
            e.g. for each t:
            freqmat[t,0,:] contains the signal mean (zero frequency term)
            freqmat[t,1:n/2,:] contains the positive fequency terms
            freqmat[t,n/2+1:,:] contains the negative frequency terms
            freqmat[t,n,:] contains the Nyquist frequency for n%2 == 1
            freqmat[t,(n-1)/2,:] contains the largest positive frequency for n%2 == 0
            freqmat[t,(n+1)/2,:] contains the largest negative frequency for n%2 == 0

    '''

    # some debugging values for myself.
    #overlap = (framesize - step + 0.0) / framesize
    #framesize = double the extractable frequency spectrum?
    #how does that relate to - with the signal - the output dims (how much signal can we get, what needs to be padded?)
    T = len(samples)
    raw_frequency_data = np.array(stft(samples, framesize,step,windowfxn)).T # framesize x N numpy.ndarray of complex128
    freqmat = np.empty((framesize, raw_frequency_data.shape[1],2)) # float64
    freqmat[...,0] = np.real(raw_frequency_data)
    freqmat[...,1] = np.imag(raw_frequency_data)
    return freqmat


def freqmat2samples(freqmat, step=16, windowfxn= np.hanning, dtype = None):
    '''
    Inverse function to samples2freqmat. See function description for details

    Parameters:
    -----------
    freqmat : numpy.ndarray
        A shaped numpy matrix describing the frequency spectrum shaped (F,T,2+)
        F is the frequency frame size (or 2*frequencies or the length of the time frame of the signal sequences described)
        T is the number of consecutive time windows encoded in the matrix
        the last dimension encodes the real (index 0) and imaginary (index 1) parts of the spectra.
        additional layers of this index are ignored

    step : int
        default = 16
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

    REAL = freqmat[...,0].T # T x F shaped real frequency components
    IMAG = freqmat[...,0].T # T x F shaped imaginary frequency components

    frequencies = [REAL[t,:] + 1j*IMAG[t,:] for t in xrange(REAL.shape[0])]
    samples = istft(frequencies, step, windowfxn, dtype)
    return samples






'''
RECORDING FUNCTIONS BELOW
'''



def trim_silence(samples, noise_threshold=150):
    '''
    Removes leading and trailing periods of silence from a given audio signal.
    This impmentation has been adapted from: https://github.com/Jakobovski/free-spoken-digit-dataset/blob/master/utils/trimmer.py

    Parameters:
    -----------
        samples : numpy.ndarray
            a one-dimensional numpy array

        noise_threshold : int
            thresholding value. every sample at the beginning and end of samples smaller
            than this value will be considered as noise/silence.

    Returns:
    --------
        trimmed_samples: numpy.ndarray
            the trimmed audio samples without leading and trailing noise segments.
    '''

    start,end = None,None
    for t,value in enumerate(samples):
        if abs(value) > noise_threshold:
            start = t;
            break
    for t,value in enumerate(samples[::-1]):
        if abs(value) > noise_threshold:
            end = t;
            break

    return samples[start:end+1]

def resample_data(samples,samplerate,newrate,width=2):
    '''
    Resamples the given single channel audio samples with a new data rate.

    Parameters:
    -----------

    samples : numpy.ndarray
        the input audio samples to sample at another data rate

    samplerate : int
        the sample rate in hz of the input signal

    newrate : int
        the sample rate of the output signal in hz

    width : int
        default = 2
        the sample width in byte.
        1 = 8-bit samples
        2 = 16-bit samples
        ...

    Returns:
    --------

    newsamples: numpy.ndarray
        the input signal sampled at another data rate.
    '''
    #width is the sample width, number of bytes.
    return np.fromstring(audioop.ratecv(samples,width,1, samplerate, newrate, None)[0],dtype='int16')


def record_audio(TODO = 'TODO'): pass