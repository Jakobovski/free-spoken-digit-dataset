import os
from collections import defaultdict

import numpy as np
from scipy.io.wavfile import read, write

from say_numbers_prompt import generate_number_sequence, DELAY_BETWEEN_NUMBERS

"""
Splits up the audio data you collected in Audacity.

Adjust the CONSTANTS below and run this file.

Labeled audio will appear in the "recordings" dir.
"""

YOUR_NAME_HERE = 'theo'

# Where did you save your Audacity-exported wav file?
PATH_TO_AUDIO_FILE = r'C:\Users\theo\Desktop\spoken_numbers_R_8khz.wav'

# Time (seconds) between the beginning of the file and the first number
# If your output files end up silent, change this number!
# It may help to look at the beginning of your recording in Audacity to see the offset.
START_OFFSET = 1.2

# How long it actually took you to say each number, typically 1.5 seconds
SECS_PER_NUMBER = 3

LABELS = generate_number_sequence()


def split_wav(start_offset, secs_between_numbers, secs_per_number):
    fname = PATH_TO_AUDIO_FILE
    rate, sound = read(fname)

    if len(sound.shape) > 1:
        # Audio probably has L and R channels.
        # Use the left channel only (mono).
        sound = sound[:, 0]

    samples_between_numbers = int(rate * secs_between_numbers)
    offset_idx = int(rate*start_offset)

    counts = defaultdict(lambda: 0)

    for i, label in enumerate(LABELS):
        label = str(label)
        start_idx = offset_idx + i * samples_between_numbers
        stop_idx = start_idx + int(rate * secs_per_number)

        if stop_idx > len(sound):
            raise('Error: Sound ends before expected number of samples reached for index:' + str(i))

        # trim silence
        digit_audio = sound[start_idx:stop_idx]
        digit_audio_trimmed = trim_silence(digit_audio)

        # Build filename
        outfile = label + "_" + YOUR_NAME_HERE + "_" + str(counts[label]) + ".wav"
        outfile = 'recordings' + os.sep + outfile

        # Write audio chunk to file
        print "writing", outfile
        write(outfile, rate, digit_audio_trimmed)
        counts[label] += 1



def trim_silence(audio, n_noise_samples=1000, noise_factor=1.0, mean_filter_size=100):
    """ Removes the silence at the beginning and end of the passed audio data
    Fits noise based on the last n_noise_samples samples in the period
    Finds where the mean-filtered magnitude > noise
    :param audio: numpy array of audio
    :return: a trimmed numpy array
    """
    start = 0
    end = len(audio)-1

    mag = abs(audio)

    noise_sample_period = mag[end-n_noise_samples:end]
    noise_threshold = noise_sample_period.max()*noise_factor

    mag_mean = np.convolve(mag, [1/float(mean_filter_size)]*mean_filter_size, 'same')

    # find onset
    for idx, point in enumerate(mag_mean):
        if point > noise_threshold:
            start = idx
            break

    # Reverse the array for trimming the end
    for idx, point in enumerate(mag_mean[::-1]):
        if point > noise_threshold:
            end = len(audio) - idx
            break

    return audio[start:end]


if __name__ == '__main__':
    split_wav(START_OFFSET, DELAY_BETWEEN_NUMBERS, SECS_PER_NUMBER)

