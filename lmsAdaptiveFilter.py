"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    In many cases, the amplitude or phase of the song and instrumental may not
    match. To compensate, we can use a least mean squares filter to linearly
    transform the instrumental until the error between the two sound waves is
    minimized.

    In simple terms, we can use math to make the instrumental better match the song.

    M is a constant integer and must be odd. It is the number of samples used
    in the filter. A bigger M can correct bigger discrepancies at the cost of
    greater processing power.

    MU is a constant float. It controls how quickly the weights change. In theory,
    it must be smaller than 1/lambda, where lambda is the max eignevalue of the
    autocorrelation matrix of the input signal. But this is really complicated to
    find so I just gradually reduce MU until the algorithm works. Changing MU only
    changes the starting value - MU still gets updated over time.

    As with all constants, they can be changed, but I find that M = 7 and MU = 2**-36
    works decently well without eating too much processing power.

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
import numpy as np
from scipy import io

M = 7
MU = 2**-36

# The input signal is the instrumental waveform, the desired signal is the song waveform
def runLMSAdaptiveFilter(inputSignal, desiredSignal):
    # Convert to floats to allow decimal calculations and prevent integer overflow
    inputSignal = np.float64(inputSignal)
    desiredSignal = np.float64(desiredSignal)
    
    # Initialize x (chunk of input signal)
    x = np.zeros(M)
    for i in range(int((M-1)/2)+1, M):
        x[i] = inputSignal[i]
    # Initialize w (weights)
    w = np.zeros(M)
    w[int((M-1)/2)] = 1
    # Initialize y and e (filtered input signal and error signal, respectively)
    y = np.empty(len(inputSignal))
    e = np.empty(len(desiredSignal))
    # Re-initialize mu as a local variable (since the constant can't be changed)
    mu = MU
    print(f"Starting with m = {M}, mu = {mu}")
    # The weights will stop changing ("converge") if mu is small enough
    # If mu is too large, the weights will grow to infinity
    # We can keep lowering mu until the weights converge
    convergence = False
    while convergence == False:
        convergence = True
        for i in range(len(inputSignal)):
            # Shift x to left
            x[:-1] = x[1:]
            try:
                x[-1] = inputSignal[i + int((M-1)/2)]
            except IndexError:
                x[-1] = 0
            # np.errstate catches RuntimeWarnings (since those errors are already handled below)
            with np.errstate(all="ignore"):
                y[i] = sum(x * w)
                e[i] = desiredSignal[i] - y[i]
                w = w + (mu * e[i]) * x
            # Check if any weight is NaN (caused by mu being too large)
            if np.any(np.isnan(w)) == True:
                # Lower mu
                mu /= 2
                print(f"Lowering mu to {mu}")
                # Reset x, w, y, and e
                x = np.zeros(M)
                for i in range(int((M-1)/2)+1, M):
                    x[i] = inputSignal[i]
                w = np.zeros(M)
                w[int((M-1)/2)] = 1
                y = np.zeros(len(y))
                e = np.zeros(len(e))
                # Stop the current loop and start from the beginning again
                convergence = False
                break

    return e