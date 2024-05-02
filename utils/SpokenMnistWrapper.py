import hub
import numpy as np

class SpokenMnistWrapper:
    """
    A wrapper class for the Spoken MNIST dataset.

    Attributes:
    - dataset: The Spoken MNIST dataset loaded from the ActiveLoop hub.

    Methods:
    - get_audio_from_index(index): Returns the audio data for a given index.
    - get_spectrogram_from_index(index): Returns the spectrogram data for a given index.
    - get_label_from_index(index): Returns the label for a given index.
    - get_speaker_from_index(index): Returns the speaker name for a given index.
    - get_item(index): Returns a dictionary containing audio, spectrogram, label, and speaker data for a given index.
    - get_speakers(): Returns an array of unique speaker names in the dataset.
    - get_labels(): Returns an array of unique labels in the dataset.
    - get_sample(sample_size, digits=None, speakers=None): Returns a sample of items from the dataset that match the specified criteria.
    """

    def __init__(self):
        self.dataset = hub.load("hub://activeloop/spoken_mnist")
        self.sampling_rate = 8000 # All recordings should be mono 8kHz

    def get_audio_from_index(self, index):
        """
        Returns the audio data for a given index.

        Parameters:
        - index (int): The index of the item in the dataset.

        Returns:
        - audio (ndarray): The audio data.
        """
        return self.dataset['audio'][int(index)]

    def get_spectrogram_from_index(self, index):
        """
        Returns the spectrogram data for a given index.

        Parameters:
        - index (int): The index of the item in the dataset.

        Returns:
        - spectrogram (ndarray): The spectrogram data.
        """
        return self.dataset['spectrograms'][int(index)]

    def get_label_from_index(self, index):
        """
        Returns the label for a given index.

        Parameters:
        - index (int): The index of the item in the dataset.

        Returns:
        - label (int): The label.
        """
        return self.dataset['labels'][int(index)]

    def get_speaker_from_index(self, index):
        """
        Returns the speaker name for a given index.

        Parameters:
        - index (int): The index of the item in the dataset.

        Returns:
        - speaker (str): The speaker name.
        """
        return self.dataset['speakers'][int(index)]

    def get_item_from_index(self, index):
        """
        Returns a dictionary containing audio, spectrogram, label, and speaker data for a given index.

        Parameters:
        - index (int): The index of the item in the dataset.

        Returns:
        - item (dict): A dictionary containing audio, spectrogram, label, and speaker data.
        """
        return {
            'audio': self.get_audio_from_index(index),
            'spectrogram': self.get_spectrogram_from_index(index),
            'label': self.get_label_from_index(index),
            'speaker': self.get_speaker_from_index(index),
        }
    
    def get_speakers(self):
        """
        Returns an array of unique speaker names in the dataset.

        Returns:
        - speakers (ndarray): An array of unique speaker names.
        """
        return np.unique(self.dataset['speakers'].numpy())
    
    def get_labels(self):
        """
        Returns an array of unique labels in the dataset.

        Returns:
        - labels (ndarray): An array of unique labels.
        """
        return np.unique(self.dataset['labels'].numpy())

    def get_sample(self, sample_size, digits=None, speakers=None):
        """
        Returns a sample of items from the dataset that match the specified criteria.

        Parameters:
        - sample_size (int): The number of items to include in the sample.
        - digits (list, optional): A list of digits that should be included in the sample. If not specified, any digit can be included.
        - speakers (list, optional): A list of speaker names that should be included in the sample. If not specified, any speaker can be included.

        Returns:
        - sample (list): A list of items from the dataset that match the specified criteria.
        """
        sample = []
        indices = []

        if digits is None:
            indices = range(len(self.dataset))
        else:
            for i in range(len(self.dataset)):
                label = self.get_label_from_index(i).numpy()
                if label in digits:
                    indices.append(i)

        if speakers is not None:
            indices = [i for i in indices if self.get_speaker_from_index(i) in speakers]

        if len(indices) < sample_size:
            raise ValueError("Not enough items in the dataset that match the specified criteria.")

        sample_indices = np.array(indices)[np.random.randint(low=0,high=len(indices)-1, size= sample_size)]
        for index in sample_indices:
            sample.append(self.get_item_from_index(index))

        return sample
    
    


if __name__ == "__main__":
    # Example usage
    # Load the Spoken MNIST dataset
    spoken_mnist = SpokenMnistWrapper()

    # Get the names of the speakers in the dataset
    speakers = spoken_mnist.get_speakers()

    # Get 5 samples of digits 0 and 1 spoken by speakers 0 and 1
    print(spoken_mnist.get_sample(5, digits=[0, 1], speakers=speakers[:2]))
