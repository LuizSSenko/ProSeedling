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
from skimage.morphology import skeletonize
from skimage.util import img_as_float, img_as_ubyte
from utils import display_img
import numpy as np
import cv2
from .branchClass import Branch, BranchList

class SkeltonizerContour:

    def __init__(self, inputImgBinary, colorImg, n_segments_each_skeleton = 15, thres_avg_max_radicle_thickness=12) -> None:
        self.inputImgBinary = inputImgBinary
        self.skeltonized = self.getSkeltonImg()   ## Skeletonized image
        self.binaryImgBrokenBranches = None
        self.colorImg = colorImg
        self.n_breakPoints = n_segments_each_skeleton ### Default 15 segments to cut each root centerline for size checking
        self.thres_avg_max_radicle_thickness = thres_avg_max_radicle_thickness
        ##
        self.list_isolated_points = []  ## having only one white count in 3x3 pixel block around a pixel (itself)
        self.list_line_end_points = [] ## having two white count in 3x3 pixel block around a pixel
        self.list_continuous_line_points = [] ## having three white count in 3x3 pixel block around a pixel
        self.list_intersetion_points = [] ## having > three white count in 3x3 pixel block around a pixel

        self.each_branch_image = []
        self.list_each_branch_points = []
        self.singlBranchImg = None

        self.branch_list = []

        self.hyperCotyl_length_pixels = 0
        self.radicle_length_pixels = 0

        ##
        self.sorted_points_list = []
        self.list_hypercotyl_points = []
        self.list_root_points = []

    def getSkeltonImg(self):
        """Function returns skeltonize image of the input image"""
        skImg = img_as_float(self.inputImgBinary)
        skeltonized = skeletonize(skImg)
        self.skeltonized = img_as_ubyte(skeltonized)
        skelton_result = np.hstack((self.inputImgBinary, self.skeltonized))
        # display_img('Skeletonized root',skelton_result)

        return self.skeltonized

    def get_line_endpoints_intersections(self, skeletonized_img_np_array=None):
        """Function analyzes the skeletone line and detects if it has multiple branches,
        returns intersection points of different branches, and return end points and single isolated point lists
        """
        ### Default skeletonized_img_np_array is the class object
        if skeletonized_img_np_array is None:
            skeletonized_img_np_array = self.skeltonized

        
        whitepixels = np.argwhere(skeletonized_img_np_array==255)
        
        for i_row,j_col in whitepixels:
            cropped_window = skeletonized_img_np_array[i_row-1:i_row+2,j_col-1:j_col+2]        
            count_whites = np.sum(cropped_window==255)
            if count_whites ==1:
                self.list_isolated_points.append([i_row,j_col])
            elif count_whites==2:
                self.list_line_end_points.append([i_row,j_col])
            elif count_whites==3:
                self.list_continuous_line_points.append([i_row,j_col])
            elif count_whites>3:
                self.list_intersetion_points.append([i_row,j_col])

        
        return [self.list_intersetion_points, self.list_line_end_points]

    def seperate_each_branch_of_skeleton(self):
        """  get_line_endpoints_intersection must be executed before this function
        """

        if len(self.list_isolated_points)==0 and len(self.list_intersetion_points) and len(self.list_continuous_line_points)==0 \
            and len(self.list_line_end_points)==0:
            ### Means get_line_endpoints_intersection function is not executed, execute the function
            self.get_line_endpoints_intersections()

        ############ 1. Loop through intersection points and get adjascent intersection points of branches

        newSkeleton = self.skeltonized.copy()

        for i_row, j_col in self.list_intersetion_points:
            newSkeleton[i_row, j_col] = 0
        


        contours, heirarchy = cv2.findContours(newSkeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for cnt in contours:
            if len(cnt)>10:
                self.branch_list.append(cnt)
                
                blank_array = np.zeros_like(self.skeltonized)
                blank_array = cv2.drawContours(blank_array, cnt, -1 , 255 , 1)
                self.each_branch_image.append(blank_array)

        for image_branch in self.each_branch_image:
            whites = np.argwhere(image_branch==255)
            whites = whites.tolist()
            self.list_each_branch_points.append(whites)




        self.binaryImgBrokenBranches = newSkeleton
        # print(f'len contours or braches found',len(contours))

        self.__analyze_each_brach()

    def __sort_branch_bottom_up(self, branchPointList_yx):
        """ function takes in branch point list, bottomEndpoint 
        and sorts points it from bottom to up in linked sequence
        """
        singlBranchImg = np.zeros_like(self.skeltonized, dtype=np.uint8)
        branch = np.array(branchPointList_yx)
        # print(branch.shape)
        # branch = np.roll(branch, 1)
        # singlBranchImg = cv2.drawContours(singlBranchImg, [branch], -1, 255 , 1)
        # branch = np.roll(branch, 1)
        # print("singlBranchImg shape",singlBranchImg.shape)
        # print("np.max",np.max(branch,axis=0))
        # print("np.min",np.min(branch,axis=0))
        for i_row, j_col in branch:            
            singlBranchImg[i_row,j_col] = 255
            
        # cv2.imshow('singlBranchImg',singlBranchImg)
        # cv2.waitKey(-1)
        branchEndpoints = []

        count_whitesMaxFound = -1
        count_whiteMinFound = 9999
        for i_row, j_col in branch:
            cropped_window = singlBranchImg[i_row-1:i_row+2,j_col-1:j_col+2]        
            count_whites = np.sum(cropped_window==255)
            
            if count_whites==2:
                branchEndpoints.append([i_row,j_col])
            if count_whites<count_whiteMinFound:
                count_whiteMinFound = count_whites
            if count_whites>count_whitesMaxFound:
                count_whitesMaxFound = count_whites

        # print(f"count_white found minimum count {count_whiteMinFound} max found {count_whitesMaxFound}")
        
        endpoints = np.array(branchEndpoints)

        btmMostEndpnt = endpoints[np.argmax(endpoints[:,0], axis=0)]
        # print(btmMostEndpnt, endpoints)


        sortedPointList = []
        startPoint = btmMostEndpnt.tolist()
        for i in range(branch.shape[0]):
            ### start point
            # for i_row, j_col in branch:
            i_row, j_col = startPoint
            cropped_window = singlBranchImg[i_row-1:i_row+2,j_col-1:j_col+2]        
            whites = np.argwhere(cropped_window==255)
            for i, j in whites:
                i_row_cr =  startPoint[0] -1 + i
                j_col_cr = startPoint[1] -1 + j
                if [i_row_cr, j_col_cr] not in sortedPointList:
                    sortedPointList.append([i_row_cr, j_col_cr])
                    startPoint = [i_row_cr, j_col_cr]
                    break
        

        ### sort endpoint so that btm most endpoint is first and then others
        ### this is done for checking bottom up approach
        enpointsBtmUp = sorted(endpoints, key=lambda x :x[0])
        # enpointsBtmUp = []
        # enpointsBtmUp.append(btmMostEndpnt)
        # for point in endpoints:
        #     if point not in enpointsBtmUp:
        #         enpointsBtmUp.append(point)  

        return singlBranchImg, sortedPointList, enpointsBtmUp, btmMostEndpnt

    def __divide_final_branch_and_analyse_lengths(self, sortedBranchPointList, singlBranchImgBinary):
        
        total_pixels_branch = len(sortedBranchPointList)
        
        if total_pixels_branch > self.n_breakPoints:
            
            div_length = total_pixels_branch // self.n_breakPoints
            # print(f"total_pixels_branch {total_pixels_branch} div_length {div_length}")
            breakPointList = []

            segmentList = []

            for i in range(self.n_breakPoints):
                breakPnt = sortedBranchPointList[i*div_length] 
                breakPointList.append(breakPnt)
                y,x =breakPnt

                segment = sortedBranchPointList[i*div_length:i*div_length+div_length]
                segmentList.append(segment)

                # cv2.circle(singlBranchImgBinary, (x,y), 3,255,1)
                # print("breakPointList",breakPointList)
            
            # display_img("breakPoints",singlBranchImg)
            list_segment_avg_thickness = []

            isSegmentRadicle = True
            
            for segment in segmentList:
                newImg = np.zeros_like(self.skeltonized, np.uint8)
                # newImg = cv2.drawContours(newImg, [segment], -1,255,1)
                
                segment_btm_y = segment[0][0]
                segment_top_y = segment[-1][0]
                partSegment = self.inputImgBinary.copy()
                partSegment[0:segment_top_y,:] = 0
                partSegment[segment_btm_y:,:] = 0

                count_whites = np.sum(partSegment==255)
                avgThickness = count_whites / len(segment)
                list_segment_avg_thickness.append(int(avgThickness))

                for i, j in segment:
                    newImg[i,j] = 255
                    if avgThickness >self.thres_avg_max_radicle_thickness:
                        isSegmentRadicle = False
                        
                    if isSegmentRadicle:
                        self.colorImg[i,j] = (255,0,0)
                        self.radicle_length_pixels+=1
                        self.list_root_points.append([i,j])
                    else:
                        self.colorImg[i,j] = (0,255,0)
                        self.hyperCotyl_length_pixels+=1
                        self.list_hypercotyl_points.append([i,j])
                

                # print("Average segment thickenss", list_segment_avg_thickness)
                hconcat = np.hstack((partSegment,newImg))
                # cv2.imshow("ResultSEED",self.colorImg)
                # cv2.imshow("newImg",hconcat)
                # cv2.waitKey(-1)
        else:
            self.radicle_length_pixels = 0
            self.hyperCotyl_length_pixels = total_pixels_branch

    def __remove_small_branches_to_keep_single_branch_only(self):
        """Function removes small branches and keep single branch only"""
        """ 1. Get max length branch. sort its points bottom up
            2. Check its both endpoints for adjascent branches select maxLength branch for each endpoint
            3. Again join the selected two branches and repeat above steps """

        # 1. Get max length branch. sort its points bottom up
        # print("self.branch_list.shape",len(self.branch_list))

        branch_point_lists = self.list_each_branch_points.copy()
        shortlisted_indices = []

        branch_lengths = [len(branchPoints) for branchPoints in branch_point_lists]
        # print("Branch lengths",branch_lengths)
        
        maxBranchLengthIndex = branch_lengths.index(max(branch_lengths))
        shortlisted_indices.append(maxBranchLengthIndex)

        whites = branch_point_lists[maxBranchLengthIndex]
        
        self.singlBranchImg, sortedPointList, enpointsBtmUp, btmMostEndpnt = self.__sort_branch_bottom_up(branchPointList_yx=whites)
        self.sorted_points_list = sortedPointList
        

        # 2. Check its both endpoints for adjascent branches select maxLength branch for each endpoint
        ## 2.1 Draw 4x4 rect around endpoint and check which branch it has adjascent
        for endpoint in enpointsBtmUp:
            y,x = endpoint
            ySt, xSt = y-4, x-4
            cropped = self.binaryImgBrokenBranches[y-4:y+4,x-4:x+4]
            whitePoints = np.argwhere(cropped==255)

            adjascent_branch_list = []

            for point in whitePoints:
                y_cr, x_cr = point
                y_white, x_white = ySt+y_cr, xSt+x_cr

                ### Check in what contours it lies
                if y_white != endpoint[0] and x_white != endpoint[1]:
                    for index in range(len(branch_point_lists)):
                        if index not in shortlisted_indices:
                            branch_to_check = branch_point_lists[index]
                            if [y_white,x_white] in branch_to_check:
                                adjascent_branch_list.append(branch_to_check)
                                shortlisted_indices.append(index)
    

            if len(adjascent_branch_list)>2:
                list_length_adjascent_branch = [len(branch) for branch in adjascent_branch_list]
                # print(f"adjascent branch list_length for endpoint {endpoint} is {list_length_adjascent_branch}")

                adjsacent_max_length_brach = max(adjascent_branch_list, key=len)
                # print()

    def __analyze_each_brach(self):
        """get endpoint of each branch and process further"""

        if len(self.branch_list)==1:
            ### only single branch found --- process further.
            #   1. get endpoints (already it has), sort contour from top btm to top in line
            #   2. divide branch in number of segments   
                # 3.
            ###
            #### Get bottom most endpoint (start from bottom)
            self.singlBranchImg, sortedPointList, enpointsBtmUp, btmMostEndpnt = self.__sort_branch_bottom_up(self.list_continuous_line_points)

            self.sorted_points_list = sortedPointList
            self.__divide_final_branch_and_analyse_lengths(sortedPointList, self.singlBranchImg)

        elif len(self.branch_list)==2:
            branchPointList1, branchPointList2  = self.list_each_branch_points
            # print("self.list_each_branch_points",self.list_each_branch_points)
            singlBranchImg1, sortedPointList1, enpointsBtmUp1, btmMostEndpnt1 = self.__sort_branch_bottom_up(branchPointList_yx=branchPointList1)
            singlBranchImg2, sortedPointList2, enpointsBtmUp2, btmMostEndpnt2 = self.__sort_branch_bottom_up(branchPointList_yx=branchPointList2)

            totalSortedPoints = []
            if enpointsBtmUp1[0][0] < enpointsBtmUp2[0][0]:
                ## then join
                topEndPnt1_btm_cnt = enpointsBtmUp1[1]
                btmEndPnt2_top_cnt = enpointsBtmUp2[0]
                totalSortedPoints.extend(sortedPointList1)
                totalSortedPoints.extend(sortedPointList2)
            else:
                topEndPnt1_btm_cnt = enpointsBtmUp2[1]
                btmEndPnt2_top_cnt = enpointsBtmUp1[0]
                totalSortedPoints.extend(sortedPointList2)
                totalSortedPoints.extend(sortedPointList1)

            y1,x1 = topEndPnt1_btm_cnt
            y2,x2 = btmEndPnt2_top_cnt

            # blankImg = np.zeros_like(self.skeltonized)
            combined = singlBranchImg1 + singlBranchImg2
            self.singlBranchImg = combined

            cv2.line(combined,(x1,y1), (x2,y2), 255, 1)
            # cv2.imshow("combined",combined)
            # cv2.waitKey(-1)
            self.sorted_points_list = totalSortedPoints
            self.__divide_final_branch_and_analyse_lengths(totalSortedPoints, self.singlBranchImg)

        elif len(self.branch_list)!=0:
            ##### remove small branches to keep single branch only
            branchListObj = BranchList(self.skeltonized) 
            
            for i, branchPoints in enumerate(self.list_each_branch_points):
                branchObj = Branch(branchRandomPointList_yx=branchPoints, 
                    allBranchSkeletonBinaryImg=self.skeltonized , branchNo=i)
                branchListObj.append(branchObj)

            


            # list_branch_results = [self.__sort_branch_bottom_up(branchPoints) for branchPoints in self.list_each_branch_points ]           
            # print("Details of each branch as follows ")
            

            
            # for branchObj in branchListObj:
             
            #     branchObj.print_branch_details()
            
            branchListObj.getClosestBranchListEndpointWise()
            # branchListObj.print_adj_branch_dict()
            branchListObj.shortList_Branches_for_single()
            finalImgWithShortlistedBranchesOnly = branchListObj.get_final_single_path_binary_image()

            ### CREATE BRANCH OBJECT FINAL SINGLE LENGTH WITH binaryImgSinglelineBranch
            
            
            branchFinalSingleLine = Branch.from_singlBranchImg(singleBranchBinaryImg=finalImgWithShortlistedBranchesOnly,
                        allBranchSkeletonBinaryImg=self.skeltonized, branchNo=-1)
            
            self.sorted_points_list = branchFinalSingleLine.sortedPointList
            self.singlBranchImg = branchFinalSingleLine.singlBranchImg
            
            self.__divide_final_branch_and_analyse_lengths(branchFinalSingleLine.sortedPointList, 
                                    branchFinalSingleLine.singlBranchImg)
