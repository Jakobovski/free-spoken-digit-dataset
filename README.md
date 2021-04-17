# Free Spoken Digit Dataset (FSDD)
[![DOI](https://zenodo.org/badge/61622039.svg)](https://zenodo.org/badge/latestdoi/61622039)

A simple audio/speech dataset consisting of recordings of spoken digits in `wav` files at 8kHz. The recordings are trimmed so that they have near minimal silence at the beginnings and ends.

FSDD is an open dataset, which means it will grow over time as data is contributed.  In order to enable reproducibility and accurate citation the dataset is versioned using Zenodo DOI as well as `git tags`.

### Current status
- 6 speakers
- 3,000 recordings (50 of each digit per speaker)
- English pronunciations

### Organization
Files are named in the following format:
`{digitLabel}_{speakerName}_{index}.wav`
Example: `7_jackson_32.wav`

### Contributions
Please contribute your homemade recordings. All recordings should be mono 8kHz `wav ` files and be trimmed to have minimal silence. Don't forget to update `metadata.py` with the speaker meta-data.

To add your data, follow the recording instructions in `acquire_data/say_numbers_prompt.py`
and then run `split_and_label_numbers.py` to make your files.

### Metadata
`metadata.py` contains meta-data regarding the speakers gender and accents.

### Included utilities
`trimmer.py`
Trims silences at beginning and end of an audio file. Splits an audio file into multiple audio files by periods of silence.

`fsdd.py`
A simple class that provides an easy to use API to access the data.

`spectogramer.py`
Used for creating spectrograms of the audio data. Spectrograms are often a useful pre-processing step.

### Usage
The test set officially consists of the first 10% of the recordings. Recordings numbered `0-4` (inclusive) are in the test and `5-49` are in the training set.

### Made with FSDD
Did you use FSDD in a paper, project or app? Add it here!
* [https://github.com/Jakobovski/decoupled-multimodal-learning](https://github.com/Jakobovski/decoupled-multimodal-learning)
* [https://adhishthite.github.io/sound-mnist/](sound-mnist) by Adhish Thite (https://adhishthite.github.io/)
* [https://github.com/eonu/torch-fsdd](https://github.com/eonu/torch-fsdd) - A simple PyTorch data loader for the dataset (by [Edwin Onuonga](https://github.com/eonu)).

### External tools
- **C#/.NET.** The FSDD dataset can be used in .NET applications using the [FreeSpokenDigitsDataset class](http://accord-framework.net/docs/html/T_Accord_DataSets_FreeSpokenDigitsDataset.htm) included withing the Accord.NET Framework. A basic example on [how to perform spoken digits classification using audio MFCC features can be found here](http://accord-framework.net/docs/html/T_Accord_Audition_BagOfAudioWords.htm).

### License
[Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
