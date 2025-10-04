#setHSVclass.py

"""
This file is part of the ProSeedling project.
The ProSeedling Project, funded by FAPESP, has been developed by
Luiz Gustavo Schultz Senko as part of his Master's Thesis at USP.
"""

import os
import json
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog
from UI_files.set_hsv_ui import Ui_Form
from utils_pyqt5 import showdialog, show_cv2_img_on_label_obj  # your helper functions
from utils import *  # your other helper functions
from proj_settings import MainSettings  # project settings module
from proj_settings import load_default_settings


# Path to the settings JSON file
settings_path = MainSettings.settings_json_file_path

class SetHSV(QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None, mainUi=None):
        super().__init__(parent)
        self.setupUi(self)  # Cria a interface
        self.setWindowIconText("HSV")
        # Agora o widget btn_restore já foi criado, podemos conectar o sinal:
        self.btn_restore.clicked.connect(self.restore_defaults)

        if mainUi is None:
            raise ValueError("The parameter mainUi must be provided for SetHSV.")
        self.mainUi = mainUi

        # Load settings from JSON file
        with open(settings_path, 'r') as f:
            self.dict_settings = json.load(f)

        # Configure slider limits
        self.slider_hmin.setMinimum(0)
        self.slider_hmax.setMaximum(179)
        self.slider_smin.setMinimum(0)
        self.slider_smax.setMaximum(255)
        self.slider_vmin.setMinimum(0)
        self.slider_vmax.setMaximum(255)

        # Initialize HSV values for "Head"
        self.hsvValuesToread = [
            self.dict_settings.get('hmin_head', 0),
            self.dict_settings.get('hmax_head', 179),
            self.dict_settings.get('smin_head', 0),
            self.dict_settings.get('smax_head', 255),
            self.dict_settings.get('vmin_head', 0),
            self.dict_settings.get('vmax_head', 255)
        ]
        self.updateValuesForPartType()

        # Connect slider signals to update values dynamically
        self.slider_hmin.valueChanged.connect(self.updateValues)
        self.slider_hmax.valueChanged.connect(self.updateValues)
        self.slider_smin.valueChanged.connect(self.updateValues)
        self.slider_smax.valueChanged.connect(self.updateValues)
        self.slider_vmin.valueChanged.connect(self.updateValues)
        self.slider_vmax.valueChanged.connect(self.updateValues)

        # Configure radio buttons with a custom property and connect clicks
        self.radioHSV_seed_head.seed_part = 'Head'
        self.radioHSV_seed_head.clicked.connect(self.onClicked)
        self.radio_hsv_seed_body.seed_part = 'Body'
        self.radio_hsv_seed_body.clicked.connect(self.onClicked)
        self.radioHSV_seed_head.setChecked(True)
        self.seedPart = 'Head'

        # Connect buttons
        self.btnSave.clicked.connect(self.save_values)
        self.btnCancel.clicked.connect(self.close_window)
        self.btn_upload_img.clicked.connect(self.uploadImg)

        self.imgPath = ""
        self.img = None

    def uploadImg(self):
        temp_widget = QWidget()
        print("Opening file dialog...")
        filepath, _ = QFileDialog.getOpenFileName(
            temp_widget,
            'Select measurements calibration image',
            '',
            "Image files (*.jpg *.png *.bmp)"
        )
        if not filepath or not os.path.exists(filepath):
            showdialog("Please select a valid file")
        else:
            self.img = cv2.imread(filepath)
            self.load_img()

    def load_img(self):
        self.maskHSV = get_HSV_mask(self.img, self.hsvValuesToread)
        self.maskConcat = get_Concat_img_with_hsv_mask(self.img, self.maskHSV)
        show_cv2_img_on_label_obj(self.imgLabel_hsv, self.maskConcat)

    def updateValuesForPartType(self):
        print("Executing updateValuesForPartType...")
        self.set_hsv_values()
        self.show_current_values()

    def updateValues(self):
        newHSV_values = [
            int(self.slider_hmin.value()),
            int(self.slider_hmax.value()),
            int(self.slider_smin.value()),
            int(self.slider_smax.value()),
            int(self.slider_vmin.value()),
            int(self.slider_vmax.value())
        ]
        self.show_current_values()
        if self.img is not None:
            self.maskHSV = get_HSV_mask(self.img, newHSV_values)
            self.maskConcat = get_Concat_img_with_hsv_mask(self.img, self.maskHSV)
            show_cv2_img_on_label_obj(self.imgLabel_hsv, self.maskConcat)
    
    def restore_defaults(self):
        # Carrega os valores padrão a partir de default_settings.json (ou os hardcoded, se não existir)
        defaults = load_default_settings()
        
        if self.seedPart == "Head":
            new_values = [
                defaults.get('hmin_head', 0),
                defaults.get('hmax_head', 127),
                defaults.get('smin_head', 0),
                defaults.get('smax_head', 255),
                defaults.get('vmin_head', 0),
                defaults.get('vmax_head', 191)
            ]
        else:  # Para "Body"
            new_values = [
                defaults.get('hmin_body', 0),
                defaults.get('hmax_body', 179),
                defaults.get('smin_body', 0),
                defaults.get('smax_body', 255),
                defaults.get('vmin_body', 0),
                defaults.get('vmax_body', 162)
            ]
        # Atualiza a variável que armazena os valores que serão aplicados
        self.hsvValuesToread = new_values
        # Atualiza os sliders e os labels
        self.set_hsv_values()
        self.show_current_values()


    def save_values(self):
        print("Saving values...")
        self.hsvValuesToread = [
            int(self.slider_hmin.value()),
            int(self.slider_hmax.value()),
            int(self.slider_smin.value()),
            int(self.slider_smax.value()),
            int(self.slider_vmin.value()),
            int(self.slider_vmax.value())
        ]
        print("Final HSV values to save:", self.hsvValuesToread)
        if self.seedPart == "Head":
            self.mainUi.dict_settings['hmin_head'] = self.hsvValuesToread[0]
            self.mainUi.dict_settings['hmax_head'] = self.hsvValuesToread[1]
            self.mainUi.dict_settings['smin_head'] = self.hsvValuesToread[2]
            self.mainUi.dict_settings['smax_head'] = self.hsvValuesToread[3]
            self.mainUi.dict_settings['vmin_head'] = self.hsvValuesToread[4]
            self.mainUi.dict_settings['vmax_head'] = self.hsvValuesToread[5]
            print("Setting HSV for Head:", self.hsvValuesToread)
        elif self.seedPart == "Body":
            self.mainUi.dict_settings['hmin_body'] = self.hsvValuesToread[0]
            self.mainUi.dict_settings['hmax_body'] = self.hsvValuesToread[1]
            self.mainUi.dict_settings['smin_body'] = self.hsvValuesToread[2]
            self.mainUi.dict_settings['smax_body'] = self.hsvValuesToread[3]
            self.mainUi.dict_settings['vmin_body'] = self.hsvValuesToread[4]
            self.mainUi.dict_settings['vmax_body'] = self.hsvValuesToread[5]
            print("Setting HSV for Body:", self.hsvValuesToread)
        self.mainUi.save_settings_to_file()
        self.mainUi.process_img_and_display_results()
        showdialog("HSV settings saved successfully!!")
        self.close_window()

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Seed part is %s" % (radioButton.seed_part))
            self.seedPart = radioButton.seed_part
            if self.seedPart == "Head":
                self.hsvValuesToread = [
                    self.dict_settings.get('hmin_head', 0),
                    self.dict_settings.get('hmax_head', 179),
                    self.dict_settings.get('smin_head', 0),
                    self.dict_settings.get('smax_head', 255),
                    self.dict_settings.get('vmin_head', 0),
                    self.dict_settings.get('vmax_head', 255)
                ]
                print("Setting HSV for Head:", self.hsvValuesToread)
            elif self.seedPart == "Body":
                self.hsvValuesToread = [
                    self.dict_settings.get('hmin_body', 0),
                    self.dict_settings.get('hmax_body', 179),
                    self.dict_settings.get('smin_body', 0),
                    self.dict_settings.get('smax_body', 255),
                    self.dict_settings.get('vmin_body', 0),
                    self.dict_settings.get('vmax_body', 255)
                ]
                print("Setting HSV for Body:", self.hsvValuesToread)
            self.updateValuesForPartType()

    def set_hsv_values(self):
        print("Setting HSV values:", self.hsvValuesToread)
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
