#main_processor.py

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
import os
import numpy as np
from req_classes.contour_processor import ContourProcessor, Seed
from utils import *
import csv
from req_classes.dataAnalysis import BatchAnalysisNew
import json
from proj_settings import MainSettings

def trace_func(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

class Main_Processor:
    def __init__(self, mainUi) -> None:
        self.mainUi = mainUi
        # self.n_segments_each_skeleton = 15           # divisions to make in each length (Increase this for finer results)
        # self.thres_avg_max_radicle_thickness = 13    # avg thickness to distinguish radicle (tune this if camera position changes)
        # self.dead_seed_max_length_r_h = 80
        # self.abnormal_seed_max_length_r_h =  130
        # self.normal_seed_max_length_r_h = 150

        # self.weights_factor_growth_Pc = 0.7
        # self.weights_factor_uniformity_Pu = 0.3
        """ self.hsv_values_seed_heads = 0,127,0,255,0,34     
        self.hsv_values_seed = 0,179,0,255,0,162 """
        self.batchNumber = 1
        self.SeedObjList = []
        self.batchAnalser = None
        self.settings_file_path = MainSettings.settings_json_file_path
        self.dict_settings = {}
        self.load_settings()

    @trace_func
    def load_settings(self):
        with open(self.settings_file_path, 'r') as f:
            data = f.read()
            self.dict_settings = json.loads(data)
            self.factor_pixel_to_cm = self.dict_settings['factor_pixel_to_cm']

    @trace_func       
    def process_main(self, img_path):
        imageName = os.path.basename(img_path)
        img = cv2.imread(img_path)
        result = img.copy()
        self.load_settings()


        ############### INPUT parameters for tuning ##################

        ####################################################################


        ############### 1. get seed head masks
        self.hsv_values_seed_heads = [self.dict_settings['hmin_head'], self.dict_settings['hmax_head'],
                                      self.dict_settings['smin_head'], self.dict_settings['smax_head'],
                                      self.dict_settings['vmin_head'], self.dict_settings['vmax_head'],
                                      ]
    
        self.hsv_values_seed = [self.dict_settings['hmin_body'], self.dict_settings['hmax_body'],
                                self.dict_settings['smin_body'], self.dict_settings['smax_body'],
                                self.dict_settings['vmin_body'], self.dict_settings['vmax_body'],
                                ]

        hsvMask_seed_heads = get_HSV_mask(img, hsv_values=self.hsv_values_seed_heads)    
        maskConcat = get_Concat_img_with_hsv_mask(img, hsvMask_seed_heads)
        # display_img('Result_heads', maskConcat)
        contourProcessor_heads = ContourProcessor(imgBinary=hsvMask_seed_heads, colorImg = result)

        shortListed_headsContours = contourProcessor_heads.shortlisted_contours
        list_Head_centers = list(map(get_contour_center, shortListed_headsContours))
        # print(list_Head_centers)



        ############### 1. get complete seed masks

        
        hsvMask_seed = get_HSV_mask(img, hsv_values=self.hsv_values_seed)    
        maskConcatSeed = get_Concat_img_with_hsv_mask(img, hsvMask_seed)
        # display_img('Result_seed', maskConcatSeed)

        contourProcessor = ContourProcessor(imgBinary=hsvMask_seed, colorImg = result)
    


        ####################### Check if contours contain heads ###############
        xywh_list = [cv2.boundingRect(cnt) for cnt in contourProcessor.shortlisted_contours]
        cropped_cnts_seeds = [cropImg(contourProcessor.binaryImgShortlistedCnt, tuple_xywh=xywh_tuple) for xywh_tuple in xywh_list]
        cropped_cnt_heads = [cropImg(contourProcessor_heads.binaryImgShortlistedCnt, tuple_xywh=xywh_tuple) for xywh_tuple in xywh_list]

        final_shortListedCnts = []


        xywh_list_final = []
        for i in range(len(xywh_list)):
            croppedCntSeed = cropped_cnts_seeds[i]
            # display_img("croppedCntSeed",croppedCntSeed)
            
            croppedCntHead = cropped_cnt_heads[i]
            resultIntersection = cv2.bitwise_and(croppedCntSeed, croppedCntHead)

            whiteCntsIntersection = np.sum(resultIntersection==255)
            if whiteCntsIntersection >10:
                final_shortListedCnts.append(contourProcessor.shortlisted_contours[i])
                xywh_list_final.append(xywh_list[i])


            comparison = np.hstack((croppedCntSeed, croppedCntHead, resultIntersection))
    
        contourProcessor.shortlisted_contours = final_shortListedCnts    
        result_cnt_drawn =contourProcessor.display_shortlisted_contours(imgColor=img)
        # display_img('drawnContours', result_cnt_drawn)
        contourProcessor.get_skeleton_img()

        ### Sory xywh_list_final 

        xywh_list_final = sort_xywh_l_to_r(xywh_list_final)

        ################## Creating SEED object list ##################
        self.SeedObjList = []
        list_hypercotyl_radicle_lengths = []
        for i in range(len(xywh_list_final)):
            SeedObject = Seed(xywh=xywh_list_final[i], imgBinarySeed=hsvMask_seed, 
                imgBinaryHeadOnly=contourProcessor_heads.binaryImgShortlistedCnt,
                imgColor = contourProcessor.colorImg,
                n_segments_each_skeleton = self.mainUi.n_segments_each_skeleton,
                thres_avg_max_radicle_thickness = self.mainUi.thres_avg_max_radicle_thickness
                )

            self.SeedObjList.append(SeedObject)
            SeedObject.morph_head_img()
            SeedObject.skeletonize_root()
            # SeedObject.make_offset()
            SeedObject.analyzeSkeleton()
            list_hypercotyl_radicle_lengths.append([SeedObject.hyperCotyl_length_pixels,SeedObject.radicle_length_pixels])



        ######################### Batch analysis

        self.batchAnalyser = BatchAnalysisNew(img_path=img_path, batchNumber=self.batchNumber, seedObjList=self.SeedObjList)

        """ batch_seed_vigor_index = self.batchAnalyser.seed_vigor_index """


        """ print()   
        print("#"*50)
        print("FINAL RESULT FOR IMAGE", imageName)
        print("HYPERCOTYL AND RADICLE LENGTHS  ")
        print("RESULT",list_hypercotyl_radicle_lengths)
        print("#"*50)
        print("*"*50)
        print("Seed_vigor_index", self.batchAnalyser.seed_vigor_index)
        print("Growth", self.batchAnalyser.growth)
        print("Uniformity", self.batchAnalyser.uniformity)
        print("Germinated_seed_count", self.batchAnalyser.germinated_seed_count)
        print("Dead_seed_count", self.batchAnalyser.dead_seed_count)
        print("Abnormal_seed_count", self.batchAnalyser.abnormal_seed_count)
        print("*"*50)
        print() """

        # display_img("Result",contourProcessor.colorImg)
        # cv2.waitKey(-1)
        return list_hypercotyl_radicle_lengths, contourProcessor.colorImg, self.batchAnalyser
        
    """ @trace_func
    def getInputs():
        cultivator_name = input("Please enter cultivator name : ")
        batchNumber = input("Please input batch number :")
        analysts_name = input("Please input analysts name :")
        n_plants = input("Please input number of plants :")
        folder_path = input("Please input folder path of images (default trial_images folder):")


        return cultivator_name, batchNumber, analysts_name, n_plants, folder_path """


