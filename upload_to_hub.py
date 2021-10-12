import numpy as np
import hub
from utils.fsdd import FSDD


DATASET_URI = "./mnist_audio"


def upload_spectrograms(ds):
    ds.create_tensor("spectrograms/images", htype="image", chunk_compression="png")
    ds.create_tensor("spectrograms/labels", htype="class_label")

    with ds:
        for _, label, file_path in FSDD.get_spectrograms("./spectrograms"):
            spectrogram_sample = hub.read(file_path)
            ds.spectrograms.images.append(spectrogram_sample)
            ds.spectrograms.labels.append(np.uint32(label))

            # TODO: unbreak
            break


def upload_audio(ds):
    raise NotImplementedError


if __name__ == "__main__":
    ds = hub.empty(DATASET_URI, overwrite=True)

    upload_spectrograms(ds)
    upload_audio(ds)
    