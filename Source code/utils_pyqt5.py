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
import os
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PIL.ImageQt import ImageQt
except ImportError:
    # For newer versions of Pillow
    from PIL import ImageQt
from PIL import Image
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
import cv2

def create_directory(path):
    try:
        os.mkdir(path)
    except Exception as e:
        print(e)
    
def showdialog(message_txt):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(message_txt)        
    msg.setWindowTitle("Info")             
    retval = msg.exec_()

def apply_img_to_label_object(imgPath, labelObject):
    imgPil = Image.open(imgPath)
    # imgPil_resized = imgPil.resize((266,150))
    im = ImageQt(imgPil).copy()
    pixmap = QtGui.QPixmap.fromImage(im)
    labelObject.setPixmap(pixmap)

def show_cv2_img_on_label_obj(uiObj, img):
    qformat = QImage.Format_BGR888
    print(img.shape)
    # bytes_per_line = img.shape[2] * 3 
    img_ = QImage(img, img.shape[1], img.shape[0], qformat)
    uiObj.setPixmap(QPixmap.fromImage(img_))

def browse_folder(self):
    qWid = QWidget()
    print("file browse")
    path_folder = QFileDialog.getExistingDirectory(qWid, 'Select folder', '')        
    return path_folder
