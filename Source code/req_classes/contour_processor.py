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
from skimage.morphology import skeletonize
from skimage.util import img_as_float, img_as_ubyte
from utils import *
from shapely import ops, geometry
# import matplotlib.pyplot as plt
from .skeletonGeneratorAnalyzer import SkeltonizerContour
from proj_settings import MainSettings, SeedHealth
import json


def plot_line(ax, ob, color):
    x, y = ob.xy
    ax.plot(x, y, color=color, alpha=0.7, linewidth=3, 
            solid_capstyle='round', zorder=2)

class ContourProcessor:
    def __init__(self, imgBinary, colorImg):
        self.binaryImgRaw = imgBinary
        self.colorImg = colorImg
        ############
        self.shortlisted_contours = []
        ############
        self.binaryImgShortlistedCnt =None
        self.__get_img_prop()
        self.preprocess_thresholded_img()
        self.__findContours()
        self.__draw_shortlisted_contours_binary()

    def __get_img_prop(self):
        self.imgH, self.imgW = self.binaryImgRaw.shape[:2]

    def __draw_shortlisted_contours_binary(self):
        self.binaryImgShortlistedCnt = np.zeros_like(self.binaryImgRaw)
        for cnt in self.shortlisted_contours:
            cv2.drawContours(self.binaryImgShortlistedCnt, [cnt], -1, 255, -1)
        
    def __findContours(self):
        contours, heirarchy = cv2.findContours(self.binaryImgRaw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contoursSorted = sorted(contours, key=cv2.contourArea)
        for cnt in contoursSorted:
            x,y,w,h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if w > 0.75 * self.imgW or h >0.75 * self.imgH:
                continue
            # elif area <500:
            elif area<100:
                continue
            else:
                # print("area",area)
                self.shortlisted_contours.append(cnt)

        # print("Shortlisted contours :",len(self.shortlisted_contours))

    def preprocess_thresholded_img(self):
        kernel_ =cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        self.binaryImgRaw = cv2.dilate(self.binaryImgRaw, kernel_, 3)

    def display_shortlisted_contours(self, imgColor):
        for cnt in self.shortlisted_contours:
            cv2.drawContours(imgColor, cnt, -1, (255,0,0), 2)

        return imgColor

    def get_skeleton_img(self):
        self.__draw_shortlisted_contours_binary()
        skImg = img_as_float(self.binaryImgShortlistedCnt)
        skeltonized = skeletonize(skImg)
        skeltonized = img_as_ubyte(skeltonized)
        # display_img('binaryImg',self.binaryImgShortlistedCnt)
        # display_img('skeleton',skeltonized)




class Seed():
    
    def __init__(self, xywh, imgBinarySeed, imgBinaryHeadOnly, imgColor, n_segments_each_skeleton=15,
                        thres_avg_max_radicle_thickness=12, mainUI=None):
        self.imgBinarySeed = imgBinarySeed
        self.imgBinaryHead = imgBinaryHeadOnly
        self.colorImg = imgColor
        self.colorImgCopy = imgColor.copy()
        self.xywh = xywh  ## Location of seed in image
        self.n_segments_each_skeleton = n_segments_each_skeleton    # divisions to make in each length
        self.thres_avg_max_radicle_thickness = thres_avg_max_radicle_thickness # avg thickness to distinguish radicle and hypercotyl

        ####################################
        self.cropped_head_binary = None
        self.cropped_seed_binary = None
        self.imgBinarySeedWoHead = None
        self.skeltonized = None
        self.singlBranchBinaryImg = None

        self.hyperCotyl_length_pixels = 0
        self.radicle_length_pixels = 0
        self.total_length_pixels = 0

        self.factor_pixel_to_cm = 0
        self.hyperCotyl_length_cm = 0
        self.radicle_length_cm = 0
        self.total_length_cm = 0
        self.ratio_h_root = 0
        
        self.sorted_point_list = []
        self.list_points_hypercotyl = [] ## [y,x] format
        self.list_points_root = []

        self.seed_health = SeedHealth.NORMAL_SEED
        self.settings_file_path = MainSettings.settings_json_file_path
        self.dict_settings = {}
        self.load_settings()
        self.remove_head()

    def remove_head(self):
        self.cropped_head_binary = cropImg(self.imgBinaryHead, self.xywh)
        self.cropped_seed_binary = cropImg(self.imgBinarySeed, self.xywh)
        self.cropped_seed_color = cropImg(self.colorImg, self.xywh)
        #NOTE: this is risky... pl check
        # self.cropped_seed_color = cropImg_with_margin(self.colorImg, self.xywh, percent_margin=5)
        self.imgBinarySeedWoHead = cv2.subtract(self.cropped_seed_binary, self.cropped_head_binary)

        
    
    def load_settings(self):
        with open(self.settings_file_path, 'r') as f:
            data = f.read()
            self.dict_settings = json.loads(data)
            self.factor_pixel_to_cm = self.dict_settings['factor_pixel_to_cm']

    def show_comparison(self):
        result_img = np.hstack((self.cropped_seed_binary, self.cropped_head_binary, self.imgBinarySeedWoHead))
        # display_img("Removed Head", result_img)
        # cv2.waitKey(-1)

    def morph_head_img(self):
        for i in range(1,5):
            kernel_ = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(7,7))
            morphed_ = cv2.dilate(self.cropped_head_binary, kernel=kernel_, iterations=i)
            self.cropped_head_binary = morphed_
            self.imgBinarySeedWoHead = cv2.subtract(self.cropped_seed_binary, self.cropped_head_binary)
            
            contours, heirarchy = cv2.findContours(self.cropped_head_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            maxAreaCnt = max(contours, key=cv2.contourArea)
            maxArea = cv2.contourArea(maxAreaCnt)
            # print(f"kernel 7x7 maxArea {maxArea} iteration {i}")
            # self.show_comparison()
            if maxArea >4000:
                break
        self.getMaxLengthContour()

    def getMaxLengthContour(self):
        contours, heirarchy = cv2.findContours(self.imgBinarySeedWoHead, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours)>0:
            maxArcLengthCnt = None
            maxArcLength = 0
            for cnt in contours:
                arcLengthCnt = cv2.arcLength(cnt, closed=True)
                if arcLengthCnt > maxArcLength:
                    maxArcLengthCnt = cnt
                    maxArcLength = arcLengthCnt


            imgBinaryNew = np.zeros_like(self.imgBinarySeedWoHead)
            cv2.drawContours(imgBinaryNew, [maxArcLengthCnt],-1, 255, -1)
            self.imgBinarySeedWoHead = imgBinaryNew

        # display_img("Final root img", self.imgBinarySeedWoHead)
        # cv2.waitKey(-1)

    def skeletonize_root(self):

        skImg = img_as_float(self.imgBinarySeedWoHead)
        skeltonized = skeletonize(skImg)
        self.skeltonized = img_as_ubyte(skeltonized)
        skelton_result = np.hstack((self.imgBinarySeedWoHead, self.skeltonized))
        # display_img('Skeletonized root',skelton_result)

    def calculate_values_in_cm(self):
        # print("self.factor_pixel_to_cm", self.factor_pixel_to_cm)
        self.total_length_cm = round(self.total_length_pixels / self.factor_pixel_to_cm, 2)
        self.hyperCotyl_length_cm = round(self.hyperCotyl_length_pixels / self.factor_pixel_to_cm ,2)
        self.radicle_length_cm = round(self.radicle_length_pixels / self.factor_pixel_to_cm, 2)
        self.ratio_h_root = round(self.hyperCotyl_length_cm/self.radicle_length_cm, 2) if self.radicle_length_cm>0 else 'NA'
        # print(f"hyperCotyl_length_cm , radicle_length_cm : {self.hyperCotyl_length_cm}, {self.radicle_length_cm}")
        self.analyze_health()


    def analyze_health(self):
        if 'dead_seed_max_length' in self.dict_settings.keys():
            if self.total_length_cm <= self.dict_settings['dead_seed_max_length']:
                self.seed_health = SeedHealth.DEAD_SEED
            elif self.total_length_cm <= self.dict_settings['abnormal_seed_max_length']:
                self.seed_health = SeedHealth.ABNORMAL_SEED
            else:
                self.seed_health = SeedHealth.NORMAL_SEED

    def analyzeSkeleton(self):
        skeletonAnayzer = SkeltonizerContour(self.imgBinarySeedWoHead, colorImg = self.cropped_seed_color, 
                n_segments_each_skeleton=self.n_segments_each_skeleton, 
                thres_avg_max_radicle_thickness=self.thres_avg_max_radicle_thickness)
        skeletonAnayzer.get_line_endpoints_intersections()
        skeletonAnayzer.seperate_each_branch_of_skeleton()
        self.singlBranchBinaryImg  = skeletonAnayzer.singlBranchImg
        
        self.hyperCotyl_length_pixels = skeletonAnayzer.hyperCotyl_length_pixels
        self.radicle_length_pixels = skeletonAnayzer.radicle_length_pixels
        self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
        self.ratio_h_root = round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'

        self.analyze_health()

        self.sorted_point_list = skeletonAnayzer.sorted_points_list
        self.list_points_hypercotyl = skeletonAnayzer.list_hypercotyl_points
        self.list_points_root = skeletonAnayzer.list_root_points
        
        self.calculate_values_in_cm()

    def make_offset(self):
        skeleton_copy = self.skeltonized.copy()
        skeleton_copy2 = self.skeltonized.copy()

        intersection_points, line_end_points = get_line_endpoints_intersections(skeletonized_img_np_array=self.skeltonized)
        
        pixels = np.argwhere(self.skeltonized==255)
        pixels = pixels[...,[1,0]]
        
        h_sk, w_sk = self.skeltonized.shape[:2]
        pixels[:,1] = h_sk - pixels[:,1]

        pixels = pixels.tolist()
        # print(pixels)
        if len(pixels)>0:
            line  = geometry.LineString(pixels)
            offset_left = line.parallel_offset(1, 'left', join_style=1)
            offset_right = line.parallel_offset(1, 'right', join_style=1)

            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # # plot_line(ax, line, "blue")
            # plot_line(ax, offset_left, "green")
            # plot_line(ax, offset_right, "purple")
            # plt.show()

        for endpoint in line_end_points:
            y,x = endpoint
            cv2.circle(skeleton_copy, (x,y),3,255,1)
        
        get_seperate_lines_from_intersections(skeleton_copy2, intersection_points)

        for intersection_point in intersection_points:
            y,x = intersection_point
            cv2.circle(skeleton_copy, (x,y),3,255,1)
            cv2.circle(skeleton_copy, (x,y),5,255,1)
        
        # cv2.imshow("ENdpoints Intersections", skeleton_copy)
        # cv2.waitKey(-1)

    def reassign_points(self, new_break_point):
        """Function recalculates the hypercotyl and root length when input a user added breakpoint. 
        """
        # print("new_break_point",new_break_point)
        # print(new_break_point in self.sorted_point_list)
        # print(self.sorted_point_list)
        
        print('reassign_points')
        self.hyperCotyl_length_pixels , self.radicle_length_pixels=0,0
        gotBreakPointFromBottom = False
        if len(self.sorted_point_list)>0:
            for i,j in self.sorted_point_list:
                if [i,j] != new_break_point:
                    pass
                else:
                    gotBreakPointFromBottom = True
                
                if not gotBreakPointFromBottom:
                    ## root
                        
                    self.cropped_seed_color[i,j] = (255,0,0)
                    
                    self.radicle_length_pixels+=1

                    ## edit2 check
                    if [i,j] not in self.list_points_root:
                        self.list_points_root.append([i,j])
                    if [i,j] in self.list_points_hypercotyl:
                        self.list_points_hypercotyl.remove([i,j])


                else:
                    self.cropped_seed_color[i,j] = (0,255,0)
                    self.hyperCotyl_length_pixels+=1
                    if [i,j] not in self.list_points_hypercotyl:
                        self.list_points_hypercotyl.append([i,j])
                    if [i,j] in self.list_points_root:
                        self.list_points_root.remove([i,j])
            
            
            self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
            self.ratio_h_root = round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'
            # print(f"hyperCotyl_length_pixels , radicle_length_pixels : {self.hyperCotyl_length_pixels}, {self.radicle_length_pixels}")
            
            ## CM calculations
            self.calculate_values_in_cm()
            # cv2.imshow('colorImg', self.colorImg)
            # cv2.waitKey(1)
        else:
            print("No sorted point list...")

    def update_everything(self):
        imgCopy = cropImg(self.colorImgCopy, self.xywh).copy()
        # cv2.imshow('before corrected', imgCopy)
        for i, j in self.list_points_hypercotyl:
            imgCopy[i,j] = (0,255,0)
        for i, j in self.list_points_root:
            imgCopy[i,j] = (255,0,0)
        
        # cv2.imshow('corrected', imgCopy)
        # cv2.waitKey(1)
        self.cropped_seed_color = imgCopy

        self.hyperCotyl_length_pixels = len(self.list_points_hypercotyl)
        self.radicle_length_pixels = len(self.list_points_root)
        self.total_length_pixels = self.hyperCotyl_length_pixels + self.radicle_length_pixels
        self.ratio_h_root =  round(self.hyperCotyl_length_pixels/self.radicle_length_pixels, 2) if self.radicle_length_pixels>0 else 'NA'

        self.calculate_values_in_cm()

    def erase_points(self, point):
       
        if point in self.list_points_hypercotyl:            
            self.list_points_hypercotyl.remove(point)

        if point in self.list_points_root:            
            self.list_points_root.remove(point)

        if point in self.sorted_point_list:
            self.sorted_point_list.remove(point)

           
        self.update_everything()
        
        
    def add_hypercotyl_points(self, point_list):
        # print('add_hypercotyl_points function', point)
        for point in point_list:
            if point not in self.list_points_hypercotyl:
                self.list_points_hypercotyl.append(point)
        
        ### add point to the start of sorted point list
        list_sorted = []
        list_sorted.extend(self.sorted_point_list)
        list_sorted.extend(point_list)
        self.sorted_point_list = list_sorted

        self.update_everything()
      
        
    def add_root_points(self, point_list):
        # print('add_hypercotyl_points function', point)
        for point in point_list:
            if point not in self.list_points_root:
                self.list_points_root.append(point)
        

        ### add point to the end of sorted point list
        list_sorted = []
        list_sorted.extend(point_list)
        list_sorted.extend(self.sorted_point_list)
        self.sorted_point_list = list_sorted



        self.update_everything()