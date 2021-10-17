import os
import numpy as np
import hub
from utils.fsdd import FSDD

from tqdm import tqdm


DATASET_URI = "./mnist_audio"
# DATASET_URI = "hub://activeloop/spoken_mnist"

SPECTROGRAMS_DIR = "./spectrograms"
WAVS_DIR = "./recordings"


with open("README.md", encoding="utf-8") as f:
    readme_description = f.read()


if __name__ == "__main__":
    ds = hub.empty(DATASET_URI, overwrite=True)

    ds.info.update({
        "title": "Spoken Digit Dataset",
        "citation": "https://github.com/Jakobovski/free-spoken-digit-dataset",
        "description": readme_description,
    })

    ds.create_tensor("spectrograms", htype="image", chunk_compression="png")
    ds.create_tensor("labels", htype="class_label")
    ds.create_tensor("audio", htype="audio", sample_compression="wav")
    ds.create_tensor("speakers", htype="text")

    with ds:
        gen = FSDD.get_spectrograms(SPECTROGRAMS_DIR)
        num = len(os.listdir(SPECTROGRAMS_DIR))

        for _, label, spectrogram_path in tqdm(gen, total=num, desc="uploading to hub"):
            filename_no_ext = os.path.basename(spectrogram_path).split(".")[0]
            speaker_name = filename_no_ext.split("_")[1]

            wav_path = os.path.join(WAVS_DIR, filename_no_ext + ".wav")

            if not os.path.exists(wav_path):
                raise Exception("Missing audio file: {}".format(wav_path))

            ds.spectrograms.append(hub.read(spectrogram_path))
            ds.audio.append(hub.read(wav_path))
            ds.labels.append(np.uint32(label))
            ds.speakers.append(str(speaker_name))

    print(f'dataset was successfully uploaded to {DATASET_URI}.')
    print(ds)

    