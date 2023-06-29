import glob 
import os
import matplotlib.pyplot as plt
import pims as pm
from pims import pipeline # To analyze one frame at each time
import trackpy as tp # To do the tracking
import numpy as np
import pandas as pd

# To convert to gray scale one by one each image of the video
@pipeline
def as_gray(frame):
    red = frame[:, :, 0]
    green = frame[:, :, 1]
    blue = frame[:, :, 2]
    return 0.2125 * red + 0.7154 * green + 0.0721 * blue

directory = "/Users/montserrattrullsjuanola/Desktop/TFM/Videosanalitzats/1,0"

filenames = [file for file in glob.glob(
    os.path.join(directory,('*.avi')))]
filenames


############## Functions and parameters used in the tracking loop

min_travelled_distance = -200
diameter = 15
radius = diameter/2

def mean(video):

    frames = video[0]
    for i in range(1, len(video), 1):

        frames = frames + video[i]
        
    mean = frames/len(video)
    return mean

def analyze_whole_vid(video,filename):
        loc_df = []
        # The following loop perform the tracking
#         mean_v = mean(video)
        for i in range(0,len(video), 1): # Analyze 1 frame each 5 frame
            #print(i)
#             sub = substraction(i, mean_v, video) # change the frame where the channel is empty
            loc = tp.locate(video[i],2*round(radius)+1,threshold = 50,minmass = 200)
            loc['frame'] = i
            loc_df.append(loc.copy(deep = True))
            
        location = pd.concat(loc_df)
        location.to_csv(filename[:filename.find(".avi")]+"_location.dat", sep = "\t")

        return location
    
########### Loop to analyze all the videos
    
@pipeline 
def locate_and_track(filename):
    
    print(filename)
    video = pm.open(filename)
    video = as_gray(video)
    print(len(video))

    location = analyze_whole_vid(video,filename)
    # Here we filter the particles that passed through the channel 

    tracking = tp.link(location,7, memory = 50, neighbor_strategy= 'KDTree') # Generate the trajectories
    tracking = tracking.set_index(["frame","particle"])
#     track = filtering_particles_passed_channel(tracking, min_travelled_distance = -200)

    # Saving the data
    tracking.to_csv(filename[:filename.find(".avi")]+"_tracking.dat", sep="\t")
    
[locate_and_track(f) for f in filenames[:]]

########### Show trajectories of all the analyzed experiments

n_rows = len(filenames)
n_rows

fig, ax = plt.subplots(int(n_rows),1,figsize=(15,16*n_rows))

i = -1
for file_no, filename in enumerate(filenames[0:]):

    trj = pd.read_csv(filename[:filename.find(".avi")]+"_tracking.dat", index_col = [0,1], sep ="\t")
        
    #video = pm.open(filename)

    #ax.flatten()[file_no].imshow(video[file_no])
    #ax.flatten()[file_no].set_axis_off()
    for p,trj_p in trj.groupby("particle"):
        ax.flatten()[file_no].plot(trj_p.x, trj_p.y, '.', alpha = 0.1, markersize = 20)
        ax.flatten()[file_no].set_title(str(filename))
#           ax.plot(trj_p.x, trj_p.y*0.2*i, 'o', alpha = 0.1, markersize = 5)
#           ax.set_title(str(filename))
plt.tight_layout()
