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
    # Class attributes for default pen thickness and transparency (alpha value)
    pen_thickness = 2
    alphaValue = 25

    def __init__(self, imgGenObj) -> None:
        """
        Initialize the painting widget.
        
        Parameters:
            imgGenObj: Object that holds image generation parameters (like image directory, file list, etc.)
        """
        super().__init__()
        self.imgGenObj = imgGenObj

        # Load the UI design from a .ui file
        loadUi(r'uiFIles\painterScreen.ui', self)

        # Determine the current image file path based on the image generation object.
        self.currentImgpath = os.path.join(self.imgGenObj.imgDirPath, self.imgGenObj.imageFileNameList[self.imgGenObj.currentImgIndex])

        # Get the corresponding mask file path for the current image.
        self.currentMaskImgPath = self.get_img_mask_file_path(self.currentImgpath)
        
        # Load the original image using PIL and convert it to a QPixmap.
        imgPil = Image.open(self.currentImgpath)
        im = ImageQt(imgPil).copy()
        self.canvas = QtGui.QPixmap.fromImage(im)
        # Display the original image in the designated label.     
        self.label_img_org.setPixmap(self.canvas)

        # Set the dimensions for the painting area.
        self.label_paint_w = 900
        self.label_paint_h = 780

        # Load the mask image and convert it to a QPixmap.
        imgPilMask = Image.open(self.currentMaskImgPath)
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask= QtGui.QPixmap.fromImage(imMask)
        # Display the mask image in the painting area label.  
        self.label_paint_area.setPixmap(self.canvasMask)

        # Store image dimensions (height and width) from the original image.
        self.imgH, self.imgW = imgPil.height, imgPil.width

        # Set up a button group for radio buttons that determine the pen color mode.
        self.btngroup1 = QtWidgets.QButtonGroup()      
        self.btngroup1.addButton(self.radio_white)
        self.btngroup1.addButton(self.radio_black)

        # Set default selection and connect the radio button toggles to the checkRadio method.
        self.radio_black.toggle()
        self.radio_white.toggled.connect(self.checkRadio)
        self.radio_black.toggled.connect(self.checkRadio)

        # Initialize variables for tracking the last drawn point.
        self.last_x, self.last_y = None, None

        # Set initial drawing parameters.
        self.pen_color_mask = QtGui.QColor('black') # Color used on the mask drawing.
        self.pen_draw_color = [0,255,0]     # Color used on the main image drawing.

        # Set pen color for image drawing with transparency (alpha value).
        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)

        # Initialize slider values and their corresponding labels.
        self.slider_pen_thickness.setValue(PaintImg.pen_thickness)
        self.label_pen_th.setText(str(PaintImg.pen_thickness))
        self.slider_alpha_value.setValue(PaintImg.alphaValue)
        self.label_transparency.setText(str(PaintImg.alphaValue))

        # Connect slider changes to their respective methods.
        self.slider_pen_thickness.valueChanged.connect(self.change_pen_thickness)
        self.slider_alpha_value.valueChanged.connect(self.change_alpha_value)

        # Connect button clicks to the save and update methods.
        self.btn_save.clicked.connect(self.save_canvas)
        self.btn_updateImg.clicked.connect(self.updateOrgImgAsperMask)
        
        # Load the mask image using OpenCV for further processing.
        self.img_mask = cv2.imread(self.currentMaskImgPath)
        self.update_image_with_mask(self.img_mask)

    def get_img_mask_file_path(self, imgPath):
        """
        Generate the file path for the mask image corresponding to a given image path.
        
        Parameters:
            imgPath: The full file path of the original image.
            
        Returns:
            maskFilePath: The file path for the associated mask image (with '_mask.png' appended).
        """
        fileName = os.path.basename(imgPath)
        fileNameWoExt= fileName.split(".")[0]
        maskFileName = fileNameWoExt + "_mask.png"
        maskFilePath = os.path.join(self.imgGenObj.imgDirPath, maskFileName)
        return maskFilePath


    def update_image_with_mask(self, img_mask):
        """
        Update the main image display by blending the mask overlay onto the original image.
        
        Parameters:
            img_mask: The mask image loaded using OpenCV.
        """
        if img_mask is not None:
            # Split the mask into color channels.
            b,g,r = cv2.split(img_mask)
            # Merge back with an extra channel (the original image is used here; merging with itself)
            img_mask = cv2.merge((img_mask, b))

            # Create a transparent layer with the same dimensions as the image.
            layer = np.zeros((self.imgH, self.imgW, 4),np.uint8)
            layer[:] = (0,0,0,0)
            # Apply a green overlay where the mask is active.
            layer[b==255] = (0,255,0,20)
            # Alternatively, one could set the alpha channel using the current alpha value:
            # layer[b == 255] = (0, 255, 0, int(PaintImg.alphaValue))
        
        # Load the original image using OpenCV.
        imgOrg = cv2.imread(self.currentImgpath)
        # Create a single channel layer filled with 255 (for alpha channel).
        layerNew = np.zeros((self.imgH, self.imgW,1),np.uint8)
        layerNew[:] = 255
        # Merge the original image with the alpha channel.
        imgOrg = cv2.merge((imgOrg,layerNew))

        # Blend the original image with the mask overlay.
        imgOrg = cv2.add(imgOrg, layer)
        # Split channels and re-order them if necessary.
        b,g,r,a = cv2.split(imgOrg)
        imgOrg = cv2.merge((r,g,b,a))
        
        # Convert the blended image to a PIL image and then to QPixmap.
        imgPil = Image.fromarray(imgOrg, mode="RGBA")
        im = ImageQt(imgPil).copy()
        self.canvas = QtGui.QPixmap.fromImage(im)
        # Update the displayed original image.
        self.label_img_org.setPixmap(self.canvas)

    def checkRadio(self):
        """
        Check which radio button is selected and update the pen colors accordingly.
        """
        if self.radio_white.isChecked():
            # When white is selected, set the mask drawing color to white
            # and the main drawing color to blue.
            self.pen_color_mask=QtGui.QColor('white')
            self.pen_draw_color = [0,0,255]
        elif self.radio_black.isChecked():
            # When black is selected, set the mask drawing color to black
            # and the main drawing color to green.
            self.pen_color_mask=QtGui.QColor('black')
            self.pen_draw_color = [0,255,0]
        
        # Update the main pen color with the new RGB values and current alpha.
        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)


    def change_pen_thickness(self):
        """
        Update the pen thickness based on the slider value and update the label display.
        """
        PaintImg.pen_thickness = int(self.slider_pen_thickness.value())
        self.label_pen_th.setText(str(PaintImg.pen_thickness))

    def change_alpha_value(self):
        """
        Update the transparency (alpha) value based on the slider and update the display label.
        Also refresh the pen color with the new transparency.
        """
        PaintImg.alphaValue = int(self.slider_alpha_value.value())        
        self.label_transparency.setText(str(PaintImg.alphaValue))
        self.pen_color_img = QtGui.QColor(self.pen_draw_color[0],self.pen_draw_color[1],self.pen_draw_color[2],PaintImg.alphaValue)


    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Handle mouse movement events to draw on both the mask and the main image.
        """
        # If no previous point is set, initialize it and ignore the first event.
        if self.last_x is None:
            self.last_x = int(a0.x() / self.label_paint_w * self.imgW)
            self.last_y = int(a0.y() / self.label_paint_h * self.imgH)
            return # ignore the first frame
        
        
        ################## Draw on the Mask Canvas ##################
        # Create a QPainter object for the mask canvas.
        painter = QtGui.QPainter(self.canvasMask)
        # Set pen properties for drawing on the mask.
        p = painter.pen()
        p.setWidth(self.pen_thickness)
        p.setColor(self.pen_color_mask)
        painter.setPen(p)

        # Compute the current drawing coordinates scaled to the original image dimensions.
        self.drawX = int(a0.x() / self.label_paint_w * self.imgW)
        self.drawY = int(a0.y() / self.label_paint_h * self.imgH)

        # Draw a line from the previous point to the current point
        painter.drawLine(self.last_x, self.last_y, self.drawX, self.drawY)
        painter.end()
        # Update the mask label with the new canvas.
        self.label_paint_area.setPixmap(self.canvasMask)
        
        ################## Draw on the Main Image Canvas ##################
        # Create a QPainter object for the main image canvas.
        painter1 = QtGui.QPainter(self.canvas)
        p1 = painter1.pen()
        p1.setWidth(self.pen_thickness)
        # Use the pen color with transparency for the main image.
        p1.setColor(self.pen_color_img)
        painter1.setPen(p1)

        # Redefine drawX and drawY (they are already computed above, but here for clarity).
        self.drawX = int(a0.x() / self.label_paint_w * self.imgW)
        self.drawY = int(a0.y() / self.label_paint_h * self.imgH)

        # Draw the line on the main image.
        painter1.drawLine(self.last_x, self.last_y, self.drawX, self.drawY)
        painter1.end()

        # Update the displayed main image.
        self.label_img_org.setPixmap(self.canvas)
        self.update()

        # Update the last drawn coordinates for the next event.
        self.last_x = self.drawX
        self.last_y = self.drawY

        return super().mouseMoveEvent(a0)


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Reset the last known drawing coordinates when the mouse is released.
        """
        self.last_x = None
        self.last_y = None

        return super().mouseReleaseEvent(a0)


    def save_canvas(self):
        """
        Save the current main image canvas to a file.
        """
        filePath = "imageCanvas.png"
        self.canvas.save(filePath)
        
    def draw_something(self):
        """
        A test/demonstration method to draw a predefined line on the mask canvas.
        """
        painter =  QtGui.QPainter(self.label_paint_area.pixmap())
        painter.drawLine(10, 10, 400, 200)
        painter.end()


    def drawRectActive(self):
        """
        Placeholder method for drawing a rectangle on the mask canvas (currently not implemented).
        """
        p = QtGui.QPainter(self.canvasMask)
        p.setBrush(self.pen_color_mask)
        # Intended to draw a rectangle. Code is currently commented out.
        # p.drawRect()
    
    def updateOrgImgAsperMask(self):
        """
        Update the main image based on the current mask canvas.
        
        This involves:
          1. Saving the current state of the mask canvas to disk.
          2. Loading the saved mask as an image.
          3. Blending the mask with the original image.
        """
        # Save the current mask canvas to the designated mask file path.
        tempMaskPath = self.currentMaskImgPath
        self.canvasMask.save(tempMaskPath)

        # Read the saved mask image using OpenCV.
        imgMask = cv2.imread(tempMaskPath)
        # Update the main image with the new mask overlay.
        self.update_image_with_mask(imgMask)