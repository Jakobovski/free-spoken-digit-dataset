from __future__ import division
from os import listdir
from os.path import isfile, join
from wand.image import Image

from matplotlib import pyplot as plt
import scipy.io.wavfile as wav


def wav_to_spectrogram(audio_path, save_path, spectrogram_dimensions=(64, 64), noverlap=16, cmap='grey_r'):
    """ Creates a spectrogram of a wav file.

    :param audio_path: path of wav file
    :param save_path:  path of spectrogram to save
    :param spectrogram_dimensions: number of pixels the spectrogram should be. Defaults (64,64)
    :param noverlap: See http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    :param cmap: the color scheme to use for the spectrogram. Defaults to 'gray_r'
    :return:
    """

    sample_rate, samples = wav.read(audio_path)

    plt.specgram(samples, cmap=cmap, noverlap=noverlap)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
    plt.tight_layout()

    # TODO: Because I cant figure out how to create a plot without padding
    # I am using `.trim()`, It would be better to do this in the plot itself.
    # Also probably better to do the sizing in the plot too.
    with Image(filename=save_path) as i:
        i.trim()
        i.resize(spectrogram_dimensions[0], spectrogram_dimensions[1])
        i.save(filename=save_path)


def dir_to_spectrogram(audio_dir, spectrogram_dir, spectrogram_dimensions=(64, 64), noverlap=16, cmap='gray_r'):
    """ Creates spectrograms of all the audio files in a dir

    :param audio_dir: path of directory with audio files
    :param spectrogram_dir: path to save spectrograms
    :param spectrogram_dimensions: tuple specifying the dimensions in pixes of the created spectrogram. default:(64,64)
    :param noverlap: See http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
    :param cmap: the color scheme to use for the spectrogram. Defaults to 'gray_r'
    :return:
    """
    file_names = [f for f in listdir(audio_dir) if isfile(join(audio_dir, f)) and '.wav' in f]

    for file_name in file_names:
        print file_name
        audio_path = audio_dir + file_name
        spectogram_path = spectrogram_dir + file_name.replace('.wav', '.png')
        wav_to_spectrogram(audio_path, spectogram_path, spectrogram_dimensions=spectrogram_dimensions, noverlap=noverlap, cmap=cmap)


if __name__ == '__main__':
    audio_dir = "/Users/Jackson/development/free-spoken-digit-dataset/recordings/"
    spectrogram_dir = "/Users/Jackson/development/free-spoken-digit-dataset/spectrograms/"
    dir_to_spectrogram(audio_dir, spectrogram_dir)
