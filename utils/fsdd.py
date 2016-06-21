from os import listdir
from os.path import isfile, join
from collections import defaultdict

import numpy as np
import scipy.io.wavfile


class FSDD:

    def __init__(self, data_dir):
        """ Initializes the FSDD data helper which is used for fetching FSDD data.

        :param data_dir: The directory where the audiodata is located.
        :return: None
        """
        self.recording_paths = defaultdict(list) # A cache
        file_paths = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]

        for digit in range(0, 10):
            # fetch all the file paths that start with this digit
            digit_paths = [join(data_dir, f) for f in file_paths if f[0] == str(digit)]
            self.recording_paths[digit] = digit_paths

    def get_random_recording(self, limit=None):
        """ Gets a random recoridng from the dataset as a numpy array.
        :param limit: a list that containes a subset of digits to sample from.
        :returns a tuple containing the label and a numpy array of the audio.
        """
        if limit is None:
            limit = range(10)

        # pick a random label
        label = np.random.choice(limit)
        file_path = np.random.choice(self.recording_paths[label])
        rate, audio = scipy.io.wavfile.read(file_path)
        return digit, audio
