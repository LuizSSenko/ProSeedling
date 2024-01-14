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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMainWindow, QStackedWidget, QWidget, QProgressBar, QDialog
import utils_pyqt5 as ut
from PyQt5.uic import loadUi
from PIL.ImageQt import ImageQt
from PIL import Image
import os
import cv2
import numpy as np

class PaintImg(QWidget):
    
    pen_thickness = 2
    alphaValue = 25
    def __init__(self, imgGenObj) -> None:
        super().__init__()
        self.imgGenObj = imgGenObj
        loadUi(r'uiFIles\painterScreen.ui', self)
        self.currentImgpath = os.path.join(self.imgGenObj.imgDirPath, self.imgGenObj.imageFileNameList[self.imgGenObj.currentImgIndex])
        
        self.currentMaskImgPath = self.get_img_mask_file_path(self.currentImgpath)
        
        
        imgPil = Image.open(self.currentImgpath)
        im = ImageQt(imgPil).copy()
        self.canvas = QtGui.QPixmap.fromImage(im)       
        self.label_img_org.setPixmap(self.canvas)

        self.label_paint_w = 900
        self.label_paint_h = 780

        imgPilMask = Image.open(self.currentMaskImgPath)
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask= QtGui.QPixmap.fromImage(imMask)       
        self.label_paint_area.setPixmap(self.canvasMask)


        self.imgH, self.imgW = imgPil.height, imgPil.width

        self.btngroup1 = QtWidgets.QButtonGroup()      
        
        self.btngroup1.addButton(self.radio_white)
        self.btngroup1.addButton(self.radio_black)

        self.radio_black.toggle()
        self.radio_white.toggled.connect(self.checkRadio)
        self.radio_black.toggled.connect(self.checkRadio)

        self.last_x, self.last_y = None, None 
        # self.pen_thickness = 2
        self.pen_color_mask = QtGui.QColor('black')
        self.pen_draw_color = [0,255,0]

        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)
        self.slider_pen_thickness.setValue(PaintImg.pen_thickness)
        self.label_pen_th.setText(str(PaintImg.pen_thickness))

        self.slider_alpha_value.setValue(PaintImg.alphaValue)
        self.label_transparency.setText(str(PaintImg.alphaValue))
        self.slider_pen_thickness.valueChanged.connect(self.change_pen_thickness)
        self.slider_alpha_value.valueChanged.connect(self.change_alpha_value)

        self.btn_save.clicked.connect(self.save_canvas)
        self.btn_updateImg.clicked.connect(self.updateOrgImgAsperMask)
        # self.draw_something() 
        self.img_mask = cv2.imread(self.currentMaskImgPath)
        self.update_image_with_mask(self.img_mask)

    def get_img_mask_file_path(self, imgPath):
        fileName = os.path.basename(imgPath)
        fileNameWoExt= fileName.split(".")[0]
        maskFileName = fileNameWoExt + "_mask.png"
        maskFilePath = os.path.join(self.imgGenObj.imgDirPath, maskFileName)
        return maskFilePath


    def update_image_with_mask(self, img_mask):
        
        if img_mask is not None:
            b,g,r = cv2.split(img_mask)
            img_mask = cv2.merge((img_mask, b))    
            layer = np.zeros((self.imgH, self.imgW, 4),np.uint8)
            layer[:] = (0,0,0,0)
            layer[b==255] = (0,255,0,20)
            # layer[b==255] = (0,255,0,int(PaintImg.alphaValue))
        
        imgOrg = cv2.imread(self.currentImgpath)
        layerNew = np.zeros((self.imgH, self.imgW,1),np.uint8)
        layerNew[:] = 255
        imgOrg = cv2.merge((imgOrg,layerNew))
        # print("imgOrg.shape",imgOrg.shape,"layer.shape",layer.shape)
        imgOrg = cv2.add(imgOrg, layer)
        b,g,r,a = cv2.split(imgOrg)
        imgOrg = cv2.merge((r,g,b,a))
        
        
        imgPil = Image.fromarray(imgOrg, mode="RGBA")
        im = ImageQt(imgPil).copy()
        self.canvas = QtGui.QPixmap.fromImage(im)       
        self.label_img_org.setPixmap(self.canvas)

    def checkRadio(self):
        if self.radio_white.isChecked():
            self.pen_color_mask=QtGui.QColor('white')
            self.pen_draw_color = [0,0,255]
        elif self.radio_black.isChecked():
            self.pen_color_mask=QtGui.QColor('black')
            self.pen_draw_color = [0,255,0]
        
        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)
        # self.pen_color_img=QtGui.QColor(0,0,255,PaintImg.alphaValue)
        # self.pen_color_img=QtGui.QColor(0,255,0,PaintImg.alphaValue)


    def change_pen_thickness(self):
        PaintImg.pen_thickness = int(self.slider_pen_thickness.value())
        self.label_pen_th.setText(str(PaintImg.pen_thickness))

    def change_alpha_value(self):
        PaintImg.alphaValue = int(self.slider_alpha_value.value())        
        self.label_transparency.setText(str(PaintImg.alphaValue))
        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)


    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.last_x is None:
            self.last_x = int(a0.x() / self.label_paint_w * self.imgW)
            self.last_y = int(a0.y() / self.label_paint_h * self.imgH)
            return # ignore the first frame
        
        
        ################ paint mask ###################
        # painter = QtGui.QPainter(self.label_paint_area.pixmap())
        painter = QtGui.QPainter(self.canvasMask)
       

        # SET PEN
        p = painter.pen()
        p.setWidth(self.pen_thickness)
        p.setColor(self.pen_color_mask)
        painter.setPen(p)

        self.drawX = int(a0.x() / self.label_paint_w * self.imgW)
        self.drawY = int(a0.y() / self.label_paint_h * self.imgH)

    
        painter.drawLine(self.last_x, self.last_y, self.drawX, self.drawY)
        painter.end()
        self.label_paint_area.setPixmap(self.canvasMask)
        # self.update()
        
        ################ paint MainImg ###################

        painter1 = QtGui.QPainter(self.canvas)
       

        # SET PEN
        p1 = painter1.pen()
        p1.setWidth(self.pen_thickness)
        p1.setColor(self.pen_color_img)
        # painter1.setBrush(QtGui.QColor(0, 255, 0, 200))
        painter1.setPen(p1)

        self.drawX = int(a0.x() / self.label_paint_w * self.imgW)
        self.drawY = int(a0.y() / self.label_paint_h * self.imgH)

    
        painter1.drawLine(self.last_x, self.last_y, self.drawX, self.drawY)
        painter1.end()
        self.label_img_org.setPixmap(self.canvas)
        self.update()
        



        # update origin
        self.last_x = self.drawX
        self.last_y = self.drawY


        
        return super().mouseMoveEvent(a0)
    


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.last_x = None
        self.last_y = None

        return super().mouseReleaseEvent(a0)


    def save_canvas(self):
        filePath = "imageCanvas.png"
        self.canvas.save(filePath)
        
    def draw_something(self):
        painter =  QtGui.QPainter(self.label_paint_area.pixmap())
        painter.drawLine(10, 10, 400, 200)
        painter.end()


    def drawRectActive(self):
        p = QtGui.QPainter(self.canvasMask)
        p.setBrush(self.pen_color_mask)
        # p.drawRect()
    
    def updateOrgImgAsperMask(self):
        # 1. Save mask canvas
        # 2. load as image and update org image with mask
        tempMaskPath = self.currentMaskImgPath
        self.canvasMask.save(tempMaskPath)

        imgMask = cv2.imread(tempMaskPath)
        self.update_image_with_mask(imgMask)

         