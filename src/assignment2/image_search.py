
#________________### Instructions ###________________#

"""
Choose one image in your data that you want to be the 'target image'. 
Write a Python script or Notebook which does the following:

Use the cv2.compareHist() function to compare the 3D color histogram for your 
target image to each of the other images in the corpus one-by-one.

In particular, use chi-square distance method, like we used in class. 
Round this number to 2 decimal places.

Save the results from this comparison as a single .csv file, 
showing the distance between your target image and each of the other images. 
The .csv file should show the filename for every image in your data 
except the target and the distance metric between that image and your target. 
Call your columns: filename, distance.

Print the filename of the image which is 'closest' to your target image

"""

#________________### Import packages ###________________#

import os
#import sys
import pandas as pd
import cv2
#import matplotlib.pyplot as plt
#import pathlib as Path
import glob

#sys.path.append(os.path.join("..",".."))
#from utils.imutils import jimshow


#________________### The script ###________________#

# Create function to construct histograms including all three color channels
def myHist(path):

    # Read image
    image = cv2.imread(path)

    # We only want 8 bins for each color channels 0, 1, and 2 (chunk it down so it is easier to measure anything)
    hist = cv2.calcHist([image], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256]) 

    # MinMax normalization: (value - min) / (max - min)
    hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX) 

    return(hist)

def main():

    # Import a list of all file paths to images 
    file_path = glob.glob("data/jpg/*.jpg")

    # Extract an image as target image while removing it from 'images'
    target_path = file_path.pop(1)

    # Create empty dataframe
    Columns = ['filename','distance']           
    DATA = pd.DataFrame(columns = Columns)
    
    # Create a 0 distance variable to be overwritten in the loop
    min_distance = 0

    for file in file_path:

        # Target histogram
        hist1 = myHist(target_path)

        # Constructing a histogram for each image in the list.
        hist2 = myHist(file)

        # Calculate distance with compreHist()
        distance = round(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR),2)

        # Save the given filename wihout the path
        filename = os.path.basename(file)

        # Find the image with the lowest distance (and save filename and distance)
        if (min_distance == 0):           # I made a variable outside the loop being 0
            min_distance = distance     # the first distance will be the first current min_distance
        elif (min_distance > distance): # every time there is a lower distance, the min_distance will be overwritten
            min_distance = distance
            min_filename = filename     # save the filename of the lowest distance image

        # Append info to dataframe
        DATA = DATA.append({
            'filename': filename,
            'distance': distance,
            }, ignore_index=True)
    
    # Print the chi^2 of the image most similar to the target image
    print(f"The image {min_filename} has the lowest distance measured in chi^2, {min_distance}, to the target image which is {os.path.basename(target_path)}.")

    # Save the dataframe as a csv file.
    DATA.to_csv('image_search_results.csv')


if __name__=="__main__":
    main()