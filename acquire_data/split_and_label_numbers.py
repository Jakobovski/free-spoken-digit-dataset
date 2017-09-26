import os
from collections import defaultdict

from scipy.io.wavfile import read, write

from say_numbers_prompt import generate_number_sequence, DELAY_BETWEEN_NUMBERS

"""
Splits up the audio data you collected in Audacity.

Adjust the CONSTANTS below and run this file.

Labeled audio will appear in the "recordings" dir.
"""

YOUR_NAME_HERE = 'theo'

# Where did you save your Audacity-exported wav file?
PATH_TO_AUDIO_FILE = r'C:\Users\theo\Desktop\big.wav'

# Time (seconds) between the beginning of the file and the first number
# If your output files end up silent, change this number!
# It may help to look at the beginning of your recording in Audacity to see the offset.
START_OFFSET = 3

# How long it actually took you to say each number, typically 1.5 seconds
SECS_PER_NUMBER = 1.5

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
        start_idx = offset_idx + i * samples_between_numbers
        stop_idx = start_idx + int(rate * secs_per_number)

        if stop_idx > len(sound):
            raise('Error: Sound ends before expected number of samples reached for index:' + str(i))

        # Build filename
        outfile = label + "_" + YOUR_NAME_HERE + "_" + str(counts[label]) + ".wav"
        outfile = 'recordings' + os.sep + outfile
        # Write audio chunk to file
        print "writing", outfile
        write(outfile, rate, sound[start_idx:stop_idx])
        counts[label] += 1


if __name__ == '__main__':
    split_wav(START_OFFSET, DELAY_BETWEEN_NUMBERS, SECS_PER_NUMBER)
