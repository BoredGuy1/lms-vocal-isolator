"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Sometimes, songs and instrumental versions aren't synchronized or the same
    length. This function aligns the song and instrumental tracks and pads them
    with silence so that they're the same length. The end result may not be
    perfect, but it should be no more than a few samples off, and the LMS filter
    will take care of the rest.

    Currently, only the first minute is used to line up the files because cross
    correlating everything is computationally expensive, especially for songs
    that are long or have multiple channels. This can be configured by changing
    the constants.

Assignment Information
    Assignment:     Final Python Project (Individual)
    Author:         Alec Peng, peng340@purdue.edu
    Team ID:        LC2 - 25

Contributor:    None
    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

from readWavFile import readWavFile
from scipy import signal, io
import numpy as np

SONG_ANALYSIS_LENGTH = 60 # In seconds
INSTRUMENTAL_ANALYSIS_LENGTH = 60 # In seconds

def alignFiles(sampleRate, channels, song, instrumental):
    # Trim to the first minute of the song/instrumental (unless it's shorter than 1 minute, then don't trim at all)
    # Finally, convert to int64 to avoid integer overflow
    try:
        trimmedSong = song[0:(sampleRate * SONG_ANALYSIS_LENGTH)]
    except IndexError:
        trimmedSong = song
    finally:
        trimmedSong = trimmedSong.astype(np.int64)
    try:
        trimmedInstrumental = instrumental[0:(sampleRate * INSTRUMENTAL_ANALYSIS_LENGTH)]
    except IndexError:
        trimmedInstrumental = instrumental[0:]
    finally:
        trimmedInstrumental = trimmedInstrumental.astype(np.int64)

    # Calculate correlation of each channel
    # Initialize
    correlation = np.zeros(len(trimmedSong) + len(trimmedInstrumental) - 1, dtype="int64")
    # Mono files
    if channels == 1:
        correlation = signal.correlate(trimmedSong, trimmedInstrumental)
    # Everything else
    else:
        for i in range(channels):
            correlation += signal.correlate(trimmedSong[:,i], trimmedInstrumental[:,i])
    # Normalize correlation
    correlation = correlation.astype(np.float32)
    correlation = (correlation / np.max(correlation)) * np.iinfo(np.int16).max
    # Determine lag
    lags = signal.correlation_lags(len(trimmedSong), len(trimmedInstrumental))
    lag = lags[np.argmax(correlation)]
    # Pad the beginnings so that the files are aligned
    if lag > 0:
        instrumental = np.pad(instrumental, ((lag, 0), (0, 0)), "constant")
    else:
        song = np.pad(song, ((-lag, 0), (0, 0)), "constant")
    # Pad the ends so that the files are the same length
    if len(instrumental) < len(song):
        instrumental = np.pad(instrumental, ((0, len(song) - len(instrumental)), (0, 0)), "constant")
    else:
        song = np.pad(song, ((0, len(instrumental) - len(song)), (0, 0)), "constant")

    return song, instrumental