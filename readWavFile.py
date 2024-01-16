"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    This function reads a WAV file and returns it along with the sample rate
    and number of channels. It will throw an error if the file does not exist,
    is not in .WAV format, or does not use 16-bit depth.

    In the future, this could be expanded to work with other data types or even
    non-WAV files by converting them with ffmpeg, but currently I am limited by
    time and computing power.

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

from scipy import io

DATA_TYPE = "int16"

def readWavFile(message):
    while True:
        try:
            file = input(message)
            sampleRate, waveform = io.wavfile.read(file)
            # Check data type
            if waveform.dtype != DATA_TYPE:
                print(f"Error: Only {DATA_TYPE} bit depth is supported. Please try again.")
            else:
                break
        
        # Throw an error if the file does not exist
        except FileNotFoundError:
            print("Error: File not found. Please try again.")
        # Throw an error if the file is not a WAV file
        # A ValueError is usually raised if the file is not supported (i.e. not a WAV file)
        except ValueError:
            print("Error: Only .wav files are supported. Please try again.")
    
    # Find the number of channels
    # Handling mono files
    if waveform.ndim == 1:
        channels = 1
    # Handling other files (stereo, 5.1 channel, 7.1 channel, etc)
    else:
        channels = waveform.shape[1]

    return sampleRate, channels, waveform