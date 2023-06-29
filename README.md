# TFM

This repository contains the code used in the computational part of my Master's thesis.

In the file Tracking.py, the recorded videos are tracked for each colloid. Firstly, they are located using the 'locate' function and assigned an ID for each one. Finally, the tracking is performed using the 'tracking' function. The output is a file that contains the position of the colloids for each frame, along with their corresponding IDs.

In the file Analysis.py, the trajectories are analyzed (using the data file). Filters are applied since the tracking may capture points that do not correspond to a colloid. From there, the potential figure is generated, as well as the length of the trap based on the distance the colloids move. All results include their respective errors.

In the file PotentialBarrier.py, there is the code used to generate the figure of the potential with respect to the width (w), including the regression line and the corresponding errors.
