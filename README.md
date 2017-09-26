# Free Spoken Digit Dataset (FSDD)

A simple audio/speech dataset consisting of recordings of spoken digits in `wav` files at 8kHz. The recordings are trimmed so that they have near minimal silence at the beginnings and ends.

FSDD is an open dataset, which means it will grow over time as data is contributed. Thus in order to enable reproducibility and accurate citation in scientific journals the dataset is versioned using `git tags`.

### Current status
- 3 speakers
- 1,500 recordings (50 of each digit)
- English pronunciations

### Organization
Files are named in the following format:
`{digitLabel}_{speakerName}_{index}.wav`
Example: `7_jackson_32.wav`

### Metadata
`metadata.py` contains meta-data regarding the speakers gender and accents. 

### Contributions
Please contribute your homemade recordings. All recordings should be 8kHz `wav ` files and be trimmed to have minimal silence. Don't forget to update `metadata.py` with the speaker meta-data.
Use the scripts in `acquire_data` to make the recording process easier.

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


### License
[Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
