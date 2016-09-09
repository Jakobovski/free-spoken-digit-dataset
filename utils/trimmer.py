import scipy.io.wavfile


def split_multiple_recordings(audio, min_silence_duration=0.25, noise_threshold=150, sample_rate_hz=8e3):
    """ Accepts a numpy array of audio data and splits it at the points of silence into multiple arrays of data.

    :param audio: numpy array of audio data
    :param min_silence_duration: the required period of silence to split the recording
    :param sample_rate_hz: the sample rate of the audio
    :return: a list of split numpy arrays
    """
    # A list of tuples (start, stop)
    min_silence_frame = sample_rate_hz * min_silence_duration
    silence_zones = []

    zone_start = None
    zone_end = None

    for idx, point in enumerate(audio):
        if abs(point) < noise_threshold and zone_start is None:
            zone_start = idx

        if abs(point) > noise_threshold and zone_start is not None:
            zone_end = idx

        # If we are in a silent zone and we come to the end point
        if zone_start is not None and zone_end and abs(point) > noise_threshold:
            if (zone_end - zone_start) > min_silence_frame:
                silence_zones.append((zone_start, zone_end))

            zone_start = None
            zone_end = None

    # Split the recording by the zones
    split_recordings = []
    for idx, zone in enumerate(silence_zones):
        if idx == 0:
            start = 0
        else:
            start = silence_zones[idx - 1][1]

        end = zone[0]
        split_recordings.append(audio[start:end])

    return split_recordings


def trim_silence(audio, noise_threshold=150):
    """ Removes the silence at the beginning and end of the passed audio data

    :param audio: numpy array of audio
    :param noise_threshold: the maximum amount of noise that is considered silence
    :return: a trimmed numpy array
    """
    start = None
    end = None

    for idx, point in enumerate(audio):
        if abs(point) > noise_threshold:
            start = idx
            break

    # Reverse the array for trimming the end
    for idx, point in enumerate(audio[::-1]):
        if abs(point) > noise_threshold:
            end = len(audio) - idx
            break

    return audio[start:end]


def trim_silence_file(file_path, noise_threshold=150):
    """Accepts a file path, trims the audio and overwrites the original file with the trimmed version.

    :param file_path: file to trim
    :param noise_threshold: the maximum amount of noise that is considered silence
    :return: None
    """
    rate, audio = scipy.io.wavfile.read(file_path)
    trimmed_audio = trim_silence(audio, noise_threshold=noise_threshold)
    scipy.io.wavfile.write(file_path, rate, trimmed_audio)


def split_multiple_recordings_file(file_path, min_silence_duration=0.25, noise_threshold=150):
    """Accepts a file_path of a `wav` file, splits it by it's silent periods and creates new files for each split.
    This is useful when contributing recordings, as it allwos one to record multiple pronunciations in one file and then
    split them programmaticly.

    :param file_path: wav file path to  split
    :param min_silence_duration: the required period of silence to split the recording
    :param noise_threshold: the maximum amount of noise that is considered silence
    :return:
    """
    rate, audio = scipy.io.wavfile.read(file_path)
    split_recordings = split_multiple_recordings(audio, min_silence_duration=min_silence_duration,
                                                 noise_threshold=noise_threshold, sample_rate_hz=rate)

    if file_path.count('.') != 1:
        raise Exception('File_path must contain exactly one period, usually in extension. IE: /home/test.wav')

    for idx, recording in enumerate(split_recordings):
        new_file_path = file_path.split('.')[0] + '_' + str(idx) + ".wav"
        scipy.io.wavfile.write(new_file_path, rate, recording)
