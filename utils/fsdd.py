from __future__ import print_function
import os
from collections import defaultdict
import scipy.io.wavfile
import scipy.ndimage


class FSDD:
    """Summary

    Attributes:
        file_paths (TYPE): Description
        recording_paths (TYPE): Description
    """

    def __init__(self, data_dir):
        """Initializes the FSDD data helper which is used for fetching FSDD data.

        :param data_dir: The directory where the audiodata is located.
        :return: None

        Args:
            data_dir (TYPE): Description
        """

        # A dict containing lists of file paths, where keys are the label and vals.
        self.recording_paths = defaultdict(list)
        file_paths = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        self.file_paths = file_paths

        for digit in range(0, 10):
            # fetch all the file paths that start with this digit
            digit_paths = [os.path.join(data_dir, f) for f in file_paths if f[0] == str(digit)]
            self.recording_paths[digit] = digit_paths

    @staticmethod
    def get_spectrograms(data_dir=None):
        """

        Args:
            data_dir (string): Path to the directory containing the spectrograms.

        Returns:
            (spectrograms, labels): a tuple of containing lists of spectrograms images(as numpy arrays) and their corresponding labels as strings
        """
        spectrograms = []
        labels = []

        if data_dir is None:
            data_dir = os.path.dirname(__file__) + '/../spectrograms'
            print(data_dir)

        file_paths = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and '.png' in f]

        if len(file_paths) == 0:
            raise Exception('There are no files in the spectrogram directory. Make sure to run the spectrogram.py before calling this function.')

        for file_name in file_paths:
            label = file_name[0]
            spectrogram = scipy.ndimage.imread(data_dir + '/' + file_name, flatten=True).flatten()
            spectrograms.append(spectrogram)
            labels.append(label)

        return spectrograms, labels
