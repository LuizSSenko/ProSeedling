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
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog
import os
import utils_pyqt5 as ut
import cv2
from req_classes.pixel_to_cm import get_pixel_to_cm

class CalibrationSettings(QWidget):
    def __init__(self, mainUi):
        super().__init__()
        loadUi(r'UI_files\pixel_cm_setting_ui.ui', self)
        self.mainUi = mainUi

        self.mainUi.read_settings()

        self.lineEdit_pixel_cm.setText(str(self.mainUi.dict_settings['factor_pixel_to_cm']))
        self.btn_load_calib_img.clicked.connect(self.load_calib_image)
        self.btnSave.clicked.connect(self.saveSetting)
        self.checkerboard_size = (28,20)


    def load_calib_image(self):
        qWid = QWidget()
        print("Select measurements calibration image")
        filepath, _ = QFileDialog.getOpenFileName(qWid, 'Select measurements calibration image','',"Image files (*.jpg)")
        if not os.path.exists(filepath):
            ut.showdialog("Please select a file")
        else:
            try:
                img = cv2.imread(filepath)
                if img is None:
                    raise ValueError("File is not a valid image.")
                
                result_pixel_per_cm = get_pixel_to_cm(img, self.checkerboard_size)
                if result_pixel_per_cm is not None:
                    self.mainUi.pixel_per_cm = result_pixel_per_cm

                    if self.mainUi.pixel_per_cm is None:
                        raise ValueError("Could not calculate pixels per centimeter.")
                    print("Pixels per centimeter is :", self.mainUi.pixel_per_cm)
                    # cv2.imshow('img', img)
                    self.mainUi.dict_settings['factor_pixel_to_cm'] = self.mainUi.pixel_per_cm
                    
                    # print("self.dict_settings['factor_pixel_to_cm']", self.mainUi.dict_settings['factor_pixel_to_cm'])
                    self.lineEdit_pixel_cm.setText(str(self.mainUi.dict_settings['factor_pixel_to_cm']))

                    ut.showdialog(f"Calibration done! \n {self.mainUi.pixel_per_cm} pixel = 1 cm. ")
                    self.mainUi.save_settings_to_file()
                    self.mainUi.process_img_and_display_results()
                else:
                    ut.showdialog(f"Calibration not done! \n Image could not be processed.")
            except Exception as e:
                ut.showdialog(f"Error: {str(e)}")
            self.close()

    def saveSetting(self):
        if len(self.lineEdit_pixel_cm.text()) > 0 and self.lineEdit_pixel_cm.text().isnumeric():
            self.mainUi.pixel_per_cm =  int(self.lineEdit_pixel_cm.text())
            self.mainUi.dict_settings['factor_pixel_to_cm'] = int(self.lineEdit_pixel_cm.text())

            self.mainUi.save_settings_to_file()
            ut.showdialog(f"Saved! \n {self.mainUi.pixel_per_cm} pixel = 1 cm. \n Saved in settings. ")
            self.mainUi.process_img_and_display_results()
        else:
            ut.showdialog(f"Please enter a positive integer value.")
        
        self.close()