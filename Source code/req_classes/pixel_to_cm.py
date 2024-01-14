""" This file is part of ProSeedling project.
    The ProSeedling Project, funded by FAPESP, has been developed
    by Luiz Gustavo Schultz Senko as part of his Master's Thesis
    at the University of São Paulo (USP).

    ProSeedling is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ProSeedling is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ProSeedling.  If not, see <https://www.gnu.org/licenses/>
"""
import cv2
import numpy as np

#------------------------------ NEW WORKING CODE -------------------------------------------

def get_pixel_to_cm(img, checkerboard_size = (28,20)):
    
    # Load the image
    # img = cv2.imread(img)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    # If found, compute the size of a square in pixels
    if ret == True:
        square_size_pixels = []
        # Horizontal lines
        for i in range(checkerboard_size[1]-1):
            for j in range(checkerboard_size[0]-1):
                # Calculate the distance between two horizontally adjacent corners
                p1 = corners[j + i*checkerboard_size[0]]
                p2 = corners[j + i*checkerboard_size[0] + 1]
                distance = np.sqrt(((p1-p2)**2).sum())
                square_size_pixels.append(distance)
        # Vertical lines
        for i in range(checkerboard_size[0]):
            for j in range(checkerboard_size[1]-1):
                # Calculate the distance between two vertically adjacent corners
                p1 = corners[i + j*checkerboard_size[0]]
                p2 = corners[i + (j+1)*checkerboard_size[0]]
                distance = np.sqrt(((p1-p2)**2).sum())
                square_size_pixels.append(distance)
        # Average size of a square in pixels
        average_square_size_pixels = np.mean(square_size_pixels)
        # Since the size of a square in the real world is 1cm, our conversion factor from pixels to cm is then:
        pixel_per_cm = 1 / average_square_size_pixels
        pixel_per_cm = np.round( 1/pixel_per_cm)
        print(f"Conversion factor: {pixel_per_cm} cm/pixel") # = 0.021289622730154698
        print(f"1cm is equal to:", (1/pixel_per_cm))         # = 46.97124099731445 
        return pixel_per_cm
    else:
        print("Could not find chessboard corners")
        return None
