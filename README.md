# lms-vocal-isolator
Subtractive vocal isolation using an LMS algorithm

# What is this?
This is a personal project of mine that isolates vocals from a song, given an instrumental file. I decided to leave it up so that fellow remixers could use it. Note that this will not work well if the instrumental signal is not a linear transform of the song signal. In other words, you will only get good results from a studio instrumental.

# How does it work?
There is an old producer’s trick where if you line up a song waveform with an instrumental waveform, invert the instrumental, and add them together, the instrumental will cancel out and leave only the vocals. 

The problem with this method is that you must line the files up by hand, which is tedious and subject to human error. On top of that, the by-hand method will not work if either the song or instrumental file has gone through post-processing such as gain staging, dynamic compression, or limiting. For instance, if the standalone instrumental file is louder than the instrumental in the song, the instrumental will not cancel perfectly.

This program addresses both issues:
1. It uses a correlation matrix between the song and instrumental waveform to automatically line up the files.
2. It uses the least-mean square (LMS) signal processing algorithm to compensate for post-processing effects.

This produces better vocals than the by-hand method for less manual work.

# How do I use it?
The quick and dirty version:

1. Ensure that the song file, instrumental file, and all python files (readWavFile, alignFiles, lmsAdaptiveFilter, and vocalIsolator) are all in the same directory.
2. Ensure that the song and instrumental files are in 16-bit WAV format with the same sample rate and number of channels. (Remember, this program cannot convert file formats; you will need 3rd
party software for this. I recommend Audacity).
3. Run the main Python file (vocalIsolator).
4. Enter the name of the song file.
5. Enter the name of the instrumental file.
6. Allow the program to run (it may take a few minutes).
7. The program will print “Finished!” when it is done. The vocal file will be writen into a 16-bit
WAV file called “vocals.wav” in the same directory as all the other files.
For an in-depth explanation of everything, I recommend reading explanation.pdf.
