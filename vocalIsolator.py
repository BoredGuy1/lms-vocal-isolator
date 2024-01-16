"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    There is an old producer's trick where if you line up a song waveform with an
    instrumental waveform and invert the instrumental, the instrumental will cancel
    out and leave only the vocals. The problem with this method is that you must
    line the waves up by hand, which is tedious and subject to human error. On top
    of that, the by-hand method will not work if either the song or instrumental
    has gone through post-processing such as gain staging, dynamic compression, or
    limiting. This program addresses both issues by automatically lining up the waves
    and using a signal processing algorithm to compensate for post-processing effects,
    which produces better vocals than the by-hand method for less manual work.

    This is the main file and holds everything together. It depends on user-defined
    functions in readWavFile.py, alignFiles.py, and lmsAdaptiveFilter.py.

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
from alignFiles import alignFiles
from lmsAdaptiveFilter import runLMSAdaptiveFilter
import numpy as np
from scipy import io

def main():
    # Validate files
    while True:
        songSampleRate, songChannels, songWave = readWavFile("Enter the name of the song file: ")
        instrumentalSampleRate, instrumentalChannels, instrumentalWave = readWavFile("Enter the name of the instrumental file: ")
        # Check if sample rates are equal
        if songSampleRate != instrumentalSampleRate:
            print("Error: Files must be the same sample rate. Please try again.")
        # Check if number of channels are equal
        elif songChannels != instrumentalChannels:
            print("Error: Files must have the same number of channels. Please try again.")
        # Agree on a universal sample rate and number of channels for both files
        else:
            sampleRate = songSampleRate
            channels = songChannels
            break
    
    print("Aligning files...")
    songWave, instrumentalWave = alignFiles(sampleRate, channels, songWave, instrumentalWave)
    totalSamples = len(songWave)

    print("Running LMS filter...")
    if channels == 1: # Mono files
        vocalWave = runLMSAdaptiveFilter(instrumentalWave, songWave)
    else: # Non-mono files
        # Initialize vocal array
        vocalWave = np.empty((totalSamples, channels))
        # Run LMS filter on each channel
        for i in range(channels):
            print(f"Filtering channel {i+1}/{channels}...")
            vocalWave[:,i] = runLMSAdaptiveFilter(instrumentalWave[:,i], songWave[:,i])
            print(f"Channel {i+1} complete!")
    
    print("Writing vocal file...")
    io.wavfile.write("vocals.wav", sampleRate, vocalWave.astype(np.int16))
    print("Finished!")

if __name__ == "__main__":
    main()