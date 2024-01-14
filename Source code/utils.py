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

def get_HSV_mask(img, hsv_values):
    hmin, hmax, smin, smax, vmin, vmax =hsv_values

    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])

    maskHSV = cv2.inRange(hsvImg, lower, upper)

    return maskHSV

def get_Concat_img_with_hsv_mask(img, hsvMask1Ch):
    mask3ch = cv2.merge((hsvMask1Ch, hsvMask1Ch, hsvMask1Ch))
    maskConcat = np.hstack((img, mask3ch))
    return maskConcat

def display_img(title,img):
    cv2.namedWindow(title,cv2.WINDOW_NORMAL)
    cv2.imshow(title,img)


def get_contour_center(contour):
    x,y,w,h = cv2.boundingRect(contour)
    c_x = int(x+ w/2)
    c_y = int(y+h/2)
    return (c_x, c_y)

def check_if_point_lies_in_contour(point, point_format:"yx" ,contour):
    """point(y,x)
    point_format = "yx"or "xy"
     """
    
    if point_format=='xy':
        x,y = point
        pointNew = (y,x)
        point_to_parse = pointNew
    else:
        point_to_parse = point

    result = cv2.pointPolygonTest(contour, point_to_parse, False)
    print(result)

    if result>=0:
        ## Point inside contour
        return True
    else:
        ## Point outside contour
        return False


def cropImg(img, tuple_xywh):
    x,y,w,h = tuple_xywh
    cropped = img[y:y+h+1, x:x+w+1]
    return cropped 


def cropImg_with_margin(img, tuple_xywh, percent_margin= 5):
    x,y,w,h = tuple_xywh
    margin_h = int(h * percent_margin/100)  # 5 percent
    margin_w = int(w * percent_margin/100)  # 5 percent

    y1 = y - margin_h if y -margin_h>0 else 0
    x1 = x - margin_w if x - margin_w>0 else 0
    y2 = y + h + margin_h + 1
    x2 = x + w + margin_w + 1  

    
    cropped = img[y1:y2, x1:x2]
    return cropped 



def get_line_endpoints_intersections(skeletonized_img_np_array):
    whitepixels = np.argwhere(skeletonized_img_np_array==255)
    
    isolated_points = []  ## having only one white count(itselt)
    line_end_points = [] ## having two white count(itselt)
    continuous_line_points = [] ## having three white count(itselt)
    intersetion_points = [] ## having > three white count(itselt)

    for i_row,j_col in whitepixels:
        cropped_window = skeletonized_img_np_array[i_row-1:i_row+2,j_col-1:j_col+2]        
        count_whites = np.sum(cropped_window==255)
        if count_whites ==1:
            isolated_points.append([i_row,j_col])
        elif count_whites==2:
            line_end_points.append([i_row,j_col])
        elif count_whites==3:
            continuous_line_points.append([i_row,j_col])
        elif count_whites>3:
            intersetion_points.append([i_row,j_col])

    # print(f"Total points {whitepixels.shape}")
    # print(f"Intersection_points ={len(intersetion_points)}, endpoints = {len(line_end_points)}, continuous line points = {len(continuous_line_points)}, isolated point = {len(isolated_points)}")

    return [intersetion_points, line_end_points]

def get_seperate_lines_from_intersections(skeletonized_img_np_array, intersection_points):
    
    for intersection_pnt in intersection_points:
        y,x = intersection_pnt
        skeletonized_img_np_array[y,x] = 0
    
    # cv2.imshow('skeletonized_img_np_array',skeletonized_img_np_array)


def find_dist(pt1, pt2):
    y1,x1 = pt1
    y2,x2 = pt2

    dist = ((y2-y1)**2 + (x2-x1)**2)**(1/2)
    return dist

def find_closest_point(contour, point):
    closest_point = None
    min_distance = float('inf')

    for contour_point in contour:
        distance = find_dist(contour_point, point)  # Euclidean distance
        if distance < min_distance:
            min_distance = distance
            closest_point = contour_point

    return closest_point

def find_closest_n_points(contour, point, no_points=2):
    sortedPoints = sorted(contour, key=lambda x:find_dist(x, point))
    
    return sortedPoints[:no_points]

def check_if_point_lies_xywh_box(point, xywh_bbox):
    x1,y1,w,h = xywh_bbox
    x,y = point
    if x >= x1 and x <= (x1+w):
        if y >=y1 and y<= y1+h:
            return True

    return False


def sort_xywh_l_to_r(xywh_list):

    ## 
    y_list = [xywh[1] for xywh in xywh_list]
    x_list = [xywh[0] for xywh in xywh_list]

    avg_y = sum(y_list)/len(y_list)

    top_half_indices = [i for i, y in enumerate(y_list) if y <=avg_y]
    btm_half_indices = [i for i, y in enumerate(y_list) if i not in top_half_indices]

    ## sort top and btm from left to right
    top_half_indices_sorted_lr = sorted(top_half_indices, key= lambda x:x_list[x] )
    btm_half_indices_sorted_lr = sorted(btm_half_indices, key= lambda x:x_list[x] )

    final_sorted_list_indices = []
    final_sorted_list_indices.extend(top_half_indices_sorted_lr)
    final_sorted_list_indices.extend(btm_half_indices_sorted_lr)
    
    final_sorted_list = [xywh_list[i] for i in final_sorted_list_indices]
    print(final_sorted_list)
    return final_sorted_list

##
# l = [[9,5,10,20], [5,7,10,20], [2,5,10,20],[8,6,10,20],
#      [9,20,10,20], [5,21,10,20], [2,25,10,20],[8,28,10,20]]
# sort_xywh_l_to_r(l)