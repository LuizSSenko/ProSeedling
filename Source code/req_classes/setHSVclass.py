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
from PyQt5.QtWidgets import  QWidget
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog, show_cv2_img_on_label_obj
from utils import *
import os
from PyQt5.QtWidgets import QWidget, QFileDialog
from proj_settings import MainSettings
import json


settings_path = MainSettings.settings_json_file_path


class SetHSV(QWidget):
    def __init__(self, mainUi):
        super().__init__()
        loadUi(r'UI_files\set_hsv_ui.ui', self)
        self.mainUi = mainUi
        self.setWindowIconText("HSV")

        self.dict_settings = {}

        settings_path = MainSettings.settings_json_file_path

        with open(settings_path, 'r') as f:
            self.dict_settings = json.load(f)


        self.slider_hmin.setMinimum(0)
        self.slider_hmax.setMaximum(179)
        self.slider_smin.setMinimum(0)
        self.slider_smax.setMaximum(255)
        self.slider_vmin.setMinimum(0)
        self.slider_vmax.setMaximum(255)

        self.hsvValuesToread = [self.dict_settings['hmin_head'], self.dict_settings['hmax_head'],
                                self.dict_settings['smin_head'], self.dict_settings['smax_head'],
                                self.dict_settings['vmin_head'], self.dict_settings['vmax_head']]
        
        self.updateValuesForPartType()

        self.slider_hmin.valueChanged.connect(self.updateValues)
        self.slider_hmax.valueChanged.connect(self.updateValues)
        self.slider_smin.valueChanged.connect(self.updateValues)
        self.slider_smax.valueChanged.connect(self.updateValues)
        self.slider_vmin.valueChanged.connect(self.updateValues)
        self.slider_vmax.valueChanged.connect(self.updateValues)



        self.radioHSV_seed_head.seed_part = 'Head'
        self.radioHSV_seed_head.clicked.connect(self.onClicked)
        self.radio_hsv_seed_body.seed_part = 'Body'
        self.radio_hsv_seed_body.clicked.connect(self.onClicked)
        self.radioHSV_seed_head.setChecked(True)

        self.seedPart = 'Head'
        self.btnSave.clicked.connect(self.save_values)
        self.btnCancel.clicked.connect(self.close_window)
        self.btn_upload_img.clicked.connect(self.uploadImg)
        # self.imgPath = "self.mainUi.imagePaths[self.mainUi.currentImgIndex]"
    
    
        self.imgPath = ""
        self.img = None

    def uploadImg(self):
        qWid = QWidget()
        print("file browse")
        filepath, _ = QFileDialog.getOpenFileName(qWid, 'Select measurements caliberation image','',"Image files (*.jpg)")
        if not os.path.exists(filepath):
            showdialog("Please select a file")
        else:
            self.img = cv2.imread(filepath)
            self.load_img()
    
    def load_img(self):
        
        
        self.maskHSV = get_HSV_mask(self.img, self.hsvValuesToread)
        self.maskConcat = get_Concat_img_with_hsv_mask(self.img, self.maskHSV)
        # cv2.imshow('self.maskConcat', self.maskConcat)
        # cv2.waitKey(1)

        show_cv2_img_on_label_obj(self.imgLabel_hsv, self.maskConcat)
        # self.updateValuesForPartType()


    def updateValuesForPartType(self):
        print("executing updateValuesForPartType function..")
        self.set_hsv_values()
        self.show_current_values()

    def updateValues(self):
        # print("executing updateValues function..")
        # self.set_hsv_values()
        newHSV_values = [int(self.slider_hmin.value()), int(self.slider_hmax.value()),
                            int(self.slider_smin.value()),int(self.slider_smax.value()),
                            int(self.slider_vmin.value()), int(self.slider_vmax.value())]
        

        self.show_current_values()

        if self.img is not None:
            self.maskHSV = get_HSV_mask(self.img, newHSV_values)
            self.maskConcat = get_Concat_img_with_hsv_mask(self.img, self.maskHSV)
            show_cv2_img_on_label_obj(self.imgLabel_hsv, self.maskConcat)

    def save_values(self): 
        print("saving the values...")
        self.hsvValuesToread[0] = int(self.slider_hmin.value())
        self.hsvValuesToread[1] = int(self.slider_hmax.value())
        self.hsvValuesToread[2] = int(self.slider_smin.value())
        self.hsvValuesToread[3] = int(self.slider_smax.value())
        self.hsvValuesToread[4] = int(self.slider_vmin.value())
        self.hsvValuesToread[5] = int(self.slider_vmax.value())  

        print("final hsv values to save", self.hsvValuesToread)
        if self.seedPart=="Head":
            self.mainUi.dict_settings['hmin_head'] = self.hsvValuesToread[0]
            self.mainUi.dict_settings['hmax_head'] = self.hsvValuesToread[1]
            self.mainUi.dict_settings['smin_head'] = self.hsvValuesToread[2]
            self.mainUi.dict_settings['smax_head'] = self.hsvValuesToread[3]
            self.mainUi.dict_settings['vmin_head'] = self.hsvValuesToread[4]
            self.mainUi.dict_settings['vmax_head'] = self.hsvValuesToread[5]


            print("setting hsvValuesToread of head",self.hsvValuesToread)

        elif self.seedPart=="Body":
            self.mainUi.dict_settings['hmin_body'] = self.hsvValuesToread[0]
            self.mainUi.dict_settings['hmax_body'] = self.hsvValuesToread[1]
            self.mainUi.dict_settings['smin_body'] = self.hsvValuesToread[2]
            self.mainUi.dict_settings['smax_body'] = self.hsvValuesToread[3]
            self.mainUi.dict_settings['vmin_body'] = self.hsvValuesToread[4]
            self.mainUi.dict_settings['vmax_body'] = self.hsvValuesToread[5]

            print("setting hsvValuesToread of body", self.hsvValuesToread)

        self.mainUi.save_settings_to_file()
        self.mainUi.process_img_and_display_results()
        showdialog("HSV settings saved successfully!!")
        self.close_window()

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Seed part is %s" % (radioButton.seed_part))
            self.seedPart = radioButton.seed_part

            if self.seedPart=="Head":
                self.hsvValuesToread= [self.dict_settings['hmin_head'], self.dict_settings['hmax_head'],
                                self.dict_settings['smin_head'], self.dict_settings['smax_head'],
                                self.dict_settings['vmin_head'], self.dict_settings['vmax_head']]
                
                print("setting hsvValuesToread of head", self.hsvValuesToread)
            elif self.seedPart=="Body":
                self.hsvValuesToread= [self.dict_settings['hmin_body'], self.dict_settings['hmax_body'],
                                self.dict_settings['smin_body'], self.dict_settings['smax_body'],
                                self.dict_settings['vmin_body'], self.dict_settings['vmax_body']]
                print("setting hsvValuesToread of body", self.hsvValuesToread)
            
            self.updateValuesForPartType()

    def set_hsv_values(self):
        
        print("setting hsv values", self.hsvValuesToread)

        self.slider_hmin.setValue(self.hsvValuesToread[0])
        self.slider_hmax.setValue(self.hsvValuesToread[1])
        self.slider_smin.setValue(self.hsvValuesToread[2])
        self.slider_smax.setValue(self.hsvValuesToread[3])
        self.slider_vmin.setValue(self.hsvValuesToread[4])
        self.slider_vmax.setValue(self.hsvValuesToread[5])

        

    def show_current_values(self):
        
        self.label_hmin.setText(str(self.slider_hmin.value()))
        self.label_hmax.setText(str(self.slider_hmax.value()))
        self.label_smin.setText(str(self.slider_smin.value()))
        self.label_smax.setText(str(self.slider_smax.value()))
        self.label_vmin.setText(str(self.slider_vmin.value()))
        self.label_vmax.setText(str(self.slider_vmax.value()))

    def close_window(self):
        self.close()