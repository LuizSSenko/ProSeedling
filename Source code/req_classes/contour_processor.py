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
# Import required libraries and modules.
import cv2
import numpy as np
from skimage.morphology import skeletonize         # For skeletonization of binary images.
from skimage.util import img_as_float, img_as_ubyte  # Converting images between formats.
from utils import *                                  # Import all helper functions from utils.
from shapely import ops, geometry                    # For geometric operations (offsets, lines).
# import matplotlib.pyplot as plt                    # (Commented out) For plotting if needed.
from .skeletonGeneratorAnalyzer import SkeletonizerContour  # Custom skeleton analyzer.
from proj_settings import MainSettings, SeedHealth   # Settings and seed health definitions.
import json


def plot_line(ax, ob, color):
    """
    Plot a shapely geometry (line) on the provided matplotlib axis.

    Parameters:
        ax: Matplotlib axis object to plot on.
        ob: A shapely geometry object with x and y coordinates.
        color: Color to use for the line.
    """
    x, y = ob.xy
    ax.plot(x, y, color=color, alpha=0.7, linewidth=3, 
            solid_capstyle='round', zorder=2)

class ContourProcessor:
    def __init__(self, imgBinary, colorImg):
        """
        Initialize the ContourProcessor instance.

        Parameters:
            imgBinary: Binary image (thresholded image) to process.
            colorImg: The corresponding color image.
        """
        # Store the raw binary and color images.
        self.binaryImgRaw = imgBinary
        self.colorImg = colorImg
        self.shortlisted_contours = []  # List to store contours that meet criteria.

        self.binaryImgShortlistedCnt = None  # Image to hold drawn shortlisted contours.
        self.__get_img_prop()                # Get image dimensions.
        self.preprocess_thresholded_img()    # Preprocess the binary image.
        self.__findContours()                # Find and shortlist valid contours.
        self.__draw_shortlisted_contours_binary()  # Draw the shortlisted contours into an image.

    def __get_img_prop(self):
        """
        Retrieve the height and width of the binary image.
        """
        self.imgH, self.imgW = self.binaryImgRaw.shape[:2]

    def __draw_shortlisted_contours_binary(self):
        """
        Draw all shortlisted contours onto a blank image.
        This image is used later for skeletonization.
        """
        self.binaryImgShortlistedCnt = np.zeros_like(self.binaryImgRaw)
        for cnt in self.shortlisted_contours:
            cv2.drawContours(self.binaryImgShortlistedCnt, [cnt], -1, 255, -1)
        
    def __findContours(self):
        """
        Find contours in the binary image and shortlist those that satisfy
        specific area and size criteria.
        """
        contours, heirarchy = cv2.findContours(self.binaryImgRaw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # Sort contours by area (smallest first).
        contoursSorted = sorted(contours, key=cv2.contourArea)
        for cnt in contoursSorted:
            # Get bounding rectangle parameters (x, y, width, height).
            #Aqui, (x, y) é o ponto de início (canto superior esquerdo) e w e h são a largura e a altura do retângulo.
            x,y,w,h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            # Exclude contours that are too large relative to the image dimensions.
            if w > 0.75 * self.imgW or h >0.75 * self.imgH:
                continue
            # Exclude very small contours.
            elif area<100:
                continue
            else:
                # print("area",area)
                self.shortlisted_contours.append(cnt)
        # Debug: print("Shortlisted contours :", len(self.shortlisted_contours))

    def preprocess_thresholded_img(self):
        """
        Preprocess the binary image by performing morphological operations.
        This includes closing small holes and dilating to connect nearby regions.
        """
        # Create an elliptical kernel.
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # Apply morphological closing to fill small holes.
        self.binaryImgRaw = cv2.morphologyEx(self.binaryImgRaw, cv2.MORPH_CLOSE, kernel)
        # Optionally, dilate the image to connect regions that are very close.
        self.binaryImgRaw = cv2.dilate(self.binaryImgRaw, kernel, iterations=1)

    def display_shortlisted_contours(self, imgColor):
        """
        Draw the shortlisted contours on a given color image.

        Parameters:
            imgColor: The color image on which contours will be drawn.

        Returns:
            The color image with drawn contours.
        """
        for cnt in self.shortlisted_contours:
            cv2.drawContours(imgColor, cnt, -1, (255,0,0), 2)
        return imgColor

    def get_skeleton_img(self):
        """
        Generate a skeletonized image from the shortlisted contours.
        This function converts the drawn contours image to float, applies skeletonization,
        then converts the result back to an 8-bit image.
        """
        self.__draw_shortlisted_contours_binary()
        skImg = img_as_float(self.binaryImgShortlistedCnt)
        skeltonized = skeletonize(skImg)
        skeltonized = img_as_ubyte(skeltonized)
        # Uncomment the following lines to display the images during debugging.
        # display_img('binaryImg', self.binaryImgShortlistedCnt)
        # display_img('skeleton', skeltonized)




class Seed():
    def __init__(self, xywh, imgBinarySeed, imgBinaryHeadOnly, imgColor, n_segments_each_skeleton=15,
                        thres_avg_max_radicle_thickness=12, mainUI=None):
        """
        Initialize a Seed instance.

        Parameters:
            xywh: A tuple or list representing the seed location and dimensions in the image.
            imgBinarySeed: The binary image of the entire seed.
            imgBinaryHeadOnly: The binary image containing only the head of the seed.
            imgColor: The color image of the seed.
            n_segments_each_skeleton: Number of segments for skeleton analysis.
            thres_avg_max_radicle_thickness: Threshold value to differentiate radicle from hypocotyl.
            mainUI: Reference to the main UI, if needed.
        """
        # Store images and location information.
        self.imgBinarySeed = imgBinarySeed
        self.imgBinaryHead = imgBinaryHeadOnly
        self.colorImg = imgColor
        self.colorImgCopy = imgColor.copy()
        self.xywh = xywh  # Location and size of the seed in the image.
        self.n_segments_each_skeleton = n_segments_each_skeleton    # divisions to make in each length
        self.thres_avg_max_radicle_thickness = thres_avg_max_radicle_thickness # avg thickness to distinguish radicle and hypercotyl

        # Variables for cropped images and skeleton results
        self.cropped_head_binary = None
        self.cropped_seed_binary = None
        self.imgBinarySeedWoHead = None
        self.skeltonized = None
        self.singlBranchBinaryImg = None

        # Length measurements in pixels.
        self.hyperCotyl_length_pixels = 0
        self.radicle_length_pixels = 0
        self.total_length_pixels = 0

        # Conversion factor and lengths in centimeters.
        self.factor_pixel_to_cm = 0
        self.hyperCotyl_length_cm = 0
        self.radicle_length_cm = 0
        self.total_length_cm = 0
        self.ratio_h_root = 0
        
        # Lists for storing points along the seed structure.
        self.sorted_point_list = []
        self.list_points_hypercotyl = [] # Stored in [y, x] format.
        self.list_points_root = []

        # Set initial seed health.
        self.seed_health = SeedHealth.NORMAL_SEED
        # Load settings from JSON file.
        self.settings_file_path = MainSettings.settings_json_file_path
        self.dict_settings = {}
        self.load_settings()

        # Remove the seed head/seed from the binary image.
        self.remove_head()

    def remove_head(self):
        """
        Remove the head/seed part from the seedling image by cropping.
        This function creates cropped images for the head and the seed without the head.
        """
        self.cropped_head_binary = cropImg(self.imgBinaryHead, self.xywh)
        self.cropped_seed_binary = cropImg(self.imgBinarySeed, self.xywh)
        self.cropped_seed_color = cropImg(self.colorImg, self.xywh)
        # NOTE: Optionally, crop with a margin if needed.
        # self.cropped_seed_color = cropImg_with_margin(self.colorImg, self.xywh, percent_margin=5)
        # Subtract the head image from the full seed image to obtain the seed body.
        self.imgBinarySeedWoHead = cv2.subtract(self.cropped_seed_binary, self.cropped_head_binary)


    def load_settings(self):
        """
        Load settings from the JSON settings file.
        Sets the conversion factor from pixels to centimeters.
        """
        with open(self.settings_file_path, 'r') as f:
            data = f.read()
            self.dict_settings = json.loads(data)
            self.factor_pixel_to_cm = self.dict_settings['factor_pixel_to_cm']

    def show_comparison(self):
        """
        Display a horizontal concatenation of the cropped seed binary,
        head binary, and seed without head for visual comparison.
        """
        result_img = np.hstack((self.cropped_seed_binary, self.cropped_head_binary, self.imgBinarySeedWoHead))
        # Uncomment below to display the image for debugging.
        # display_img("Removed Head", result_img)
        # cv2.waitKey(-1)

    def morph_head_img(self):
        """
        Apply morphological dilation to the head binary image to smooth or enlarge it.
        Iteratively dilates until the maximum contour area exceeds a threshold,
        then updates the seed image without the head.
        """
        for i in range(1,5):
            # Create a kernel of size 7x7 for dilation.
            kernel_ = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(7,7))
            morphed_ = cv2.dilate(self.cropped_head_binary, kernel=kernel_, iterations=i)
            self.cropped_head_binary = morphed_
            # Update the seed binary image without the head.
            self.imgBinarySeedWoHead = cv2.subtract(self.cropped_seed_binary, self.cropped_head_binary)
            
            # Find contours in the head image.
            contours, heirarchy = cv2.findContours(self.cropped_head_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            maxAreaCnt = max(contours, key=cv2.contourArea)
            maxArea = cv2.contourArea(maxAreaCnt)
            # Debug: print(f"kernel 7x7 maxArea {maxArea} iteration {i}")
            # self.show_comparison()
            if maxArea >4000:
                break
        # After dilation, obtain the contour with maximum arc length.
        self.getMaxLengthContour()

    def getMaxLengthContour(self):
        """
        Identify and retain the contour with the maximum arc length in the seed without the head.
        This helps in isolating the main structure of the seed.
        """
        contours, heirarchy = cv2.findContours(self.imgBinarySeedWoHead, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            maxArcLengthCnt = None
            maxArcLength = 0
            for cnt in contours:
                arcLengthCnt = cv2.arcLength(cnt, closed=True)
                if arcLengthCnt > maxArcLength:
                    maxArcLengthCnt = cnt
                    maxArcLength = arcLengthCnt
            if maxArcLengthCnt is not None:
                # Create a new blank image and draw the maximum arc length contour.
                imgBinaryNew = np.zeros_like(self.imgBinarySeedWoHead)
                cv2.drawContours(imgBinaryNew, [maxArcLengthCnt], -1, 255, -1)
                self.imgBinarySeedWoHead = imgBinaryNew
            else:
                print("Warning: No valid head contour found, check HSV values.")
        else:
            print("Warning: No head contours detected, check HSV values.")



    def skeletonize_root(self):
        """
        Skeletonize the seed body (seed without head) to obtain a thin version of its structure.
        The resulting skeleton is stored in self.skeltonized.
        """
        skImg = img_as_float(self.imgBinarySeedWoHead)
        skeltonized = skeletonize(skImg)
        self.skeltonized = img_as_ubyte(skeltonized)
        # For debugging, one might horizontally stack the original and skeletonized images.
        skelton_result = np.hstack((self.imgBinarySeedWoHead, self.skeltonized))
        # Uncomment below to display the skeletonized image.
        # display_img('Skeletonized root', skelton_result)

    def calculate_values_in_cm(self):
        """
        Convert measured lengths from pixels to centimeters using the conversion factor.
        Also calculate the ratio of hypocotyl to radicle length and analyze seed health.
        """
        self.total_length_cm = round(self.total_length_pixels / self.factor_pixel_to_cm, 2)
        self.hyperCotyl_length_cm = round(self.hyperCotyl_length_pixels / self.factor_pixel_to_cm ,2)
        self.radicle_length_cm = round(self.radicle_length_pixels / self.factor_pixel_to_cm, 2)
        self.ratio_h_root = round(self.hyperCotyl_length_cm/self.radicle_length_cm, 2) if self.radicle_length_cm>0 else 'NA'
        # Debug print: print(f"hyperCotyl_length_cm, radicle_length_cm: {self.hyperCotyl_length_cm}, {self.radicle_length_cm}")
        self.analyze_health()


    def analyze_health(self):
        """
        Determine the health of the seed based on its total length.
        Uses thresholds from the settings to classify the seed as DEAD, ABNORMAL, or NORMAL.
        """
        if 'dead_seed_max_length' in self.dict_settings.keys():
            if self.total_length_cm <= self.dict_settings['dead_seed_max_length']:
                self.seed_health = SeedHealth.DEAD_SEED
            elif self.total_length_cm <= self.dict_settings['abnormal_seed_max_length']:
                self.seed_health = SeedHealth.ABNORMAL_SEED
            else:
                self.seed_health = SeedHealth.NORMAL_SEED

    def analyzeSkeleton(self):
        """
        Analyze the skeleton of the seed (without head) using the SkeletonizerContour class.
        This method extracts endpoints, separates branches, and calculates lengths.
        It then updates the seed's measurements and health based on the skeleton.
        """
        skeletonAnayzer = SkeletonizerContour(self.imgBinarySeedWoHead, colorImg = self.cropped_seed_color, 
                n_segments_each_skeleton=self.n_segments_each_skeleton, 
                thres_avg_max_radicle_thickness=self.thres_avg_max_radicle_thickness)
        # Obtain intersections of line endpoints.
        skeletonAnayzer.get_line_endpoints_intersections()
        # Separate the skeleton into individual branches.
        skeletonAnayzer.seperate_each_branch_of_skeleton()
        self.singlBranchBinaryImg  = skeletonAnayzer.singlBranchImg
        
        # Update length measurements in pixels.
        self.hyperCotyl_length_pixels = skeletonAnayzer.hyperCotyl_length_pixels
        self.radicle_length_pixels = skeletonAnayzer.radicle_length_pixels
        self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
        self.ratio_h_root = round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'

        # Re-evaluate seed health based on the new measurements.
        self.analyze_health()

        # Store the sorted list of points and points for each segment.
        self.sorted_point_list = skeletonAnayzer.sorted_points_list
        self.list_points_hypercotyl = skeletonAnayzer.list_hypercotyl_points
        self.list_points_root = skeletonAnayzer.list_root_points

        # Convert pixel measurements to centimeters.
        self.calculate_values_in_cm()

    def make_offset(self):
        """
        Calculate parallel offset lines for the skeleton to visualize its left and right boundaries.
        Uses the shapely library to compute offsets based on the set of white pixels in the skeleton.
        Also marks the intersection and endpoint locations.
        """
        # Create copies of the skeleton for drawing.
        skeleton_copy = self.skeltonized.copy()
        skeleton_copy2 = self.skeltonized.copy()

        # Get intersections and endpoints from the skeleton.
        intersection_points, line_end_points = get_line_endpoints_intersections(skeletonized_img_np_array=self.skeltonized)
        
        # Extract all white pixel coordinates from the skeleton.
        pixels = np.argwhere(self.skeltonized==255)
        # Switch coordinate order to [x, y].
        pixels = pixels[...,[1,0]]
        
        h_sk, w_sk = self.skeltonized.shape[:2]
        # Adjust the y-coordinates.
        pixels[:,1] = h_sk - pixels[:,1]

        pixels = pixels.tolist()
        # print(pixels)
        if len(pixels)>0:
            # Create a LineString from the white pixel coordinates.
            line  = geometry.LineString(pixels)
            # Calculate offsets to the left and right of the line.
            offset_left = line.parallel_offset(1, 'left', join_style=1)
            offset_right = line.parallel_offset(1, 'right', join_style=1)

            # Uncomment below to visualize using matplotlib.
            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # plot_line(ax, line, "blue")
            # plot_line(ax, offset_left, "green")
            # plot_line(ax, offset_right, "purple")
            # plt.show()

        # Mark endpoints on the skeleton copy.
        for endpoint in line_end_points:
            y,x = endpoint
            cv2.circle(skeleton_copy, (x,y),3,255,1)
        
        # Separate lines based on intersection points.
        get_seperate_lines_from_intersections(skeleton_copy2, intersection_points)

        # Mark intersections on the skeleton copy.
        for intersection_point in intersection_points:
            y,x = intersection_point
            cv2.circle(skeleton_copy, (x,y),3,255,1)
            cv2.circle(skeleton_copy, (x,y),5,255,1)
        
        # Uncomment below to display the result.
        # cv2.imshow("Endpoints & Intersections", skeleton_copy)
        # cv2.waitKey(-1)

    def reassign_points(self, new_break_point):
        """
        Recalculate the hypocotyl and radicle lengths after a user adds a breakpoint.
        
        The function iterates through the sorted list of points along the seed skeleton.
        Points before the breakpoint are considered part of the radicle, while points after
        (including the breakpoint) belong to the hypocotyl.
        
        Parameters:
            new_break_point: The [y, x] coordinate of the newly added breakpoint.
        """
        print('reassign_points')
        # Reset lengths.
        self.hyperCotyl_length_pixels , self.radicle_length_pixels=0,0
        gotBreakPointFromBottom = False
        if len(self.sorted_point_list)>0:
            for i,j in self.sorted_point_list:
                # Check if the current point is the new breakpoint.
                if [i,j] != new_break_point:
                    pass
                else:
                    gotBreakPointFromBottom = True
                
                if not gotBreakPointFromBottom:
                    # Before reaching the breakpoint: treat as radicle.
                    self.cropped_seed_color[i,j] = (255,0,0)
                    self.radicle_length_pixels+=1
                    # If the point is not already in the radicle list, add it.
                    if [i,j] not in self.list_points_root:
                        self.list_points_root.append([i,j])
                    # Remove the point from the hypocotyl list if present.
                    if [i,j] in self.list_points_hypercotyl:
                        self.list_points_hypercotyl.remove([i,j])
                # After (and including) the breakpoint: treat as hypocotyl.
                else:
                    self.cropped_seed_color[i,j] = (0,255,0)
                    self.hyperCotyl_length_pixels+=1
                    if [i,j] not in self.list_points_hypercotyl:
                        self.list_points_hypercotyl.append([i,j])
                    if [i,j] in self.list_points_root:
                        self.list_points_root.remove([i,j])
            
            # Update total length and ratio.
            self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
            self.ratio_h_root = round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'            
            # Convert measurements to centimeters.
            self.calculate_values_in_cm()
            # Uncomment below to display the updated color image.
            # cv2.imshow('colorImg', self.colorImg)
            # cv2.waitKey(1)
        else:
            print("No sorted point list...")

    def update_everything(self):
        """
        Update the seed's cropped color image with colored markings for hypocotyl and radicle points.
        Recalculate the lengths based on the current lists of points.
        """
        imgCopy = cropImg(self.colorImgCopy, self.xywh).copy()
        # Mark hypocotyl points in green.
        for i, j in self.list_points_hypercotyl:
            imgCopy[i,j] = (0,255,0)
        # Mark radicle points in blue.
        for i, j in self.list_points_root:
            imgCopy[i,j] = (255,0,0)
        
        # Uncomment below to view the updated image.
        # cv2.imshow('corrected', imgCopy)
        # cv2.waitKey(1)
        self.cropped_seed_color = imgCopy

        # Update length measurements based on the current points.
        self.hyperCotyl_length_pixels = len(self.list_points_hypercotyl)
        self.radicle_length_pixels = len(self.list_points_root)
        self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
        self.ratio_h_root =  round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'

        # Convert updated pixel values to centimeters.
        self.calculate_values_in_cm()

    def erase_points(self, point):
        """
        Remove a point from the hypocotyl, radicle, and sorted point lists.
        Then update all measurements and images.
        
        Parameters:
            point: The point to remove (in [y, x] format).
        """
        if point in self.list_points_hypercotyl:            
            self.list_points_hypercotyl.remove(point)

        if point in self.list_points_root:            
            self.list_points_root.remove(point)

        if point in self.sorted_point_list:
            self.sorted_point_list.remove(point)

        self.update_everything()


    def add_hypercotyl_points(self, point_list):
        """
        Add new points to the hypocotyl list and update the sorted point list.
        
        Parameters:
            point_list: List of new points to add (each in [y, x] format).
        """
        for point in point_list:
            if point not in self.list_points_hypercotyl:
                self.list_points_hypercotyl.append(point)
        
        # Append the new points to the end of the sorted point list.
        list_sorted = []
        list_sorted.extend(self.sorted_point_list)
        list_sorted.extend(point_list)
        self.sorted_point_list = list_sorted

        self.update_everything()


    def add_root_points(self, point_list):
        """
        Add new points to the radicle list and update the sorted point list.
        
        Parameters:
            point_list: List of new points to add (each in [y, x] format).
        """
        for point in point_list:
            if point not in self.list_points_root:
                self.list_points_root.append(point)
        
        # Prepend the new points to the sorted point list.
        list_sorted = []
        list_sorted.extend(point_list)
        list_sorted.extend(self.sorted_point_list)
        self.sorted_point_list = list_sorted

        self.update_everything()