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
import numpy as np
import cv2
from utils import find_dist

class BranchList(list):
    def __init__(self, allBranchParentImg) -> None:
        
        self.closestBranchListEndpnt1 = []
        self.closestBranchListEndpnt2 = []

        self.maxDistBetweenEndptToAdjBranch = 30 # in pixels

        self.listadjascentBranchPairs = []
        self.dict_branch_adjascent_branches = {}
        self.dict_close_endpoints = {} ## keys tuplesbranch number e.g. (2,5) value pair of endpoints close to be filled
        self.shortlistedBranches = []
        self.allBranchParentImg = allBranchParentImg

        self.finalImgWithShortlistedBranchesOnly = None

    def getClosestBranchListEndpointWise(self):
        for i, branchObj in enumerate(self):
            branchObjAdjBranchs = []

            for j, branchObjToCompare in enumerate(self):
                if i!=j:
                    branchEndpointsObj = branchObj.enpointsBtmUp
                    branchEndpointsObjToCompare = branchObjToCompare.enpointsBtmUp
                    ### endpt1, endpt2 of Brnch1 and endpt3 and endpt4 of branch2
                    # compare distances and find min distance pair
                    endPt1, endPt2 = branchEndpointsObj
                    endPt3, endPt4 = branchEndpointsObjToCompare
                    endPointPairList = [(endPt1, endPt3), (endPt1, endPt4), (endPt2, endPt3), (endPt2, endPt4)]
                    distList = [find_dist(p1, p2) for p1,p2 in endPointPairList]
                    minDistIndex = distList.index(min(distList))
                    minDistEndpointPair = endPointPairList[minDistIndex]
                    minDistBetweenBranch = min(distList)
                  

                    if minDistBetweenBranch < self.maxDistBetweenEndptToAdjBranch:
                        ### Branch are adjacent branches
                        self.dict_close_endpoints[(branchObj.branchNo, branchObjToCompare.branchNo)] = minDistEndpointPair
                        self.listadjascentBranchPairs.append([branchObj, branchObjToCompare])
                        branchObjAdjBranchs.append(branchObjToCompare)


            self.dict_branch_adjascent_branches[branchObj] = branchObjAdjBranchs

    def print_adj_branch_dict(self):
        for branchKey, adjBranchList in self.dict_branch_adjascent_branches.items():
            print(f"Branch {branchKey.branchNo}  with length {len(branchKey.sortedPointList)} has adj branches as below:")
            for adjBranch in adjBranchList:
                print(f"adj branch {adjBranch.branchNo} with length {len(adjBranch.sortedPointList)} ")

    def shortList_Branches_for_single(self):

        ### Sort branch adj dictionary by length of branchs
        sorteBranches = [branch for branch in self.dict_branch_adjascent_branches.keys()]
        sorteBranches = sorted(sorteBranches, key= lambda x:x.branchLength, reverse=True)
        if len(sorteBranches)>0 and sorteBranches:
            self.shortlistedBranches = [sorteBranches[0]]
        else:
            self.shortlistedBranches = []
            
        for branch in sorteBranches:
            adjBranchList = self.dict_branch_adjascent_branches[branch]
            if len(adjBranchList)>0:
                maxAdjLengthBranch = max(adjBranchList, key= lambda x:x.branchLength)
                
                # if branch not in shortlistedBranches:
                #     shortlistedBranches.append(branch)
                if maxAdjLengthBranch not in self.shortlistedBranches:
                    self.shortlistedBranches.append(maxAdjLengthBranch)
            




        # print(f"Total branches = {len(self)}")
        # print("SHORT listed branches are")
        # print(len(self.shortlistedBranches))
        # print(self.shortlistedBranches)


    def get_final_single_path_binary_image(self):
        if len(self.shortlistedBranches) >0:

            list_branchNos_shortlisted = []

            blnkImg = np.zeros_like(self.shortlistedBranches[0].singlBranchImg)
            for branch_ in self.shortlistedBranches:
                list_branchNos_shortlisted.append(branch_.branchNo)
                blnkImg = blnkImg + branch_.singlBranchImg
            
            
            #### Join endpoints with line
            for branchNo1, branchNo2 in self.dict_close_endpoints.keys():
                if branchNo1 in list_branchNos_shortlisted and branchNo2 in list_branchNos_shortlisted:
                    endpointAdjBranch = self.dict_close_endpoints[(branchNo1, branchNo2)] 
                    y1,x1 = endpointAdjBranch[0]
                    y2,x2 = endpointAdjBranch[1]
                    
                    cv2.line(blnkImg,(x1,y1), (x2,y2), 255, 1)
                    
            
            combined = np.hstack((self.allBranchParentImg, blnkImg))
            # cv2.imshow("ShortListed Branches",combined)
            # cv2.waitKey(-1)

            self.finalImgWithShortlistedBranchesOnly=  blnkImg



        else:
            print("ERROR : No any shortlisted branch found...")

        return self.finalImgWithShortlistedBranchesOnly

class Branch:
    def __init__(self, branchRandomPointList_yx, allBranchSkeletonBinaryImg, branchNo):
        self.branchNo = branchNo
        self.branchRandomPointList_yx = branchRandomPointList_yx
        self.allBranchSkeletonBinaryImg = allBranchSkeletonBinaryImg
        self.singlBranchImg = None
        self.sortedPointList = []
        self.enpointsBtmUp = []
        self.btmMostEndpnt = None
        self.branchLength = 0

        self.__sort_branch_bottom_up()

    @classmethod
    def from_singlBranchImg(cls, singleBranchBinaryImg, allBranchSkeletonBinaryImg, branchNo):
        whitepixels = np.argwhere(singleBranchBinaryImg==255)
        
        whites = whitepixels.tolist()

        return cls(branchRandomPointList_yx=whites, allBranchSkeletonBinaryImg=allBranchSkeletonBinaryImg, branchNo=branchNo)

    def __sort_branch_bottom_up(self):
        """ function takes in branch point list, bottomEndpoint and sorts points it from bottom to up in linked sequence"""

        
        self.singlBranchImg = np.zeros_like(self.allBranchSkeletonBinaryImg, dtype=np.uint8)
        branch = np.array(self.branchRandomPointList_yx)
        # print(branch.shape)
        for i_row, j_col in branch:            
            self.singlBranchImg[i_row,j_col] = 255
            
        # cv2.imshow('singlBranchImg',self.singlBranchImg)
        # cv2.waitKey(-1)
        branchEndpoints = []

        count_whitesMaxFound = -1
        count_whiteMinFound = 9999
        for i_row, j_col in branch:
            cropped_window = self.singlBranchImg[i_row-1:i_row+2,j_col-1:j_col+2]        
            count_whites = np.sum(cropped_window==255)
            
            if count_whites==2:
                branchEndpoints.append([i_row,j_col])
            if count_whites<count_whiteMinFound:
                count_whiteMinFound = count_whites
            if count_whites>count_whitesMaxFound:
                count_whitesMaxFound = count_whites

        # print(f"count_white found minimum count {count_whiteMinFound} max found {count_whitesMaxFound}")
        
        endpoints = np.array(branchEndpoints)

        self.btmMostEndpnt = endpoints[np.argmax(endpoints[:,0], axis=0)]
        # print(btmMostEndpnt, endpoints)


        self.sortedPointList = []
        startPoint = self.btmMostEndpnt.tolist()
        for i in range(branch.shape[0]):
            ### start point
            # for i_row, j_col in branch:
            i_row, j_col = startPoint
            cropped_window = self.singlBranchImg[i_row-1:i_row+2,j_col-1:j_col+2]        
            whites = np.argwhere(cropped_window==255)
            for i, j in whites:
                i_row_cr =  startPoint[0] -1 + i
                j_col_cr = startPoint[1] -1 + j
                if [i_row_cr, j_col_cr] not in self.sortedPointList:
                    self.sortedPointList.append([i_row_cr, j_col_cr])
                    startPoint = [i_row_cr, j_col_cr]
                    break
        

        ### sort endpoint so that btm most endpoint is first and then others
        ### this is done for checking bottom up approach
        self.enpointsBtmUp = sorted(endpoints, key=lambda x :x[0])
        self.branchLength = len(self.sortedPointList)

        return self.singlBranchImg, self.sortedPointList,self. enpointsBtmUp, self.btmMostEndpnt

    def print_branch_details(self):

        print(f"Branch no {self.branchNo} :  - endpoints {self.enpointsBtmUp}")
        print(f"Count endpoints {len(self.enpointsBtmUp)} - LengthBranch {len(self.sortedPointList)}")
                
