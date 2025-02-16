#pixel_cm_setting_ui.py


# -*- coding: utf-8 -*-
#
# Código gerado a partir do arquivo pixel_cm_setting_ui.ui, modificado manualmente.
# Alterações: os widgets são atribuídos diretamente a self e o style sheet foi atualizado
# para um visual moderno (estilo Windows 10).
#

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(879, 293)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: "Segoe UI", sans-serif;
                font-size: 10pt;
                color: #000000;
            }
            QPushButton {
                background-color: #5E86AB;
                color: #000000;
                border: 1px solid #3F5972;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #76A7D5;
            }
            QPushButton:pressed {
                background-color: #2F4355;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #AEC2D5;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel {
                color: #000000;
            }
            QToolTip {
                background-color: #FFFFDC;
                color: #000000;
                border: 1px solid #2F4355;
            }
        """)
        self.setWindowTitle("Calibration: Pixel to Centimeters")
        
        # Label principal
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(260, 30, 321, 51))
        self.label.setStyleSheet("font: 83 12pt \"Segoe UI\" bold;")
        self.label.setText("Calibration : Pixel to Centimeters")
        self.label.setObjectName("label")
        
        # Botão para carregar imagem de calibração
        self.btn_load_calib_img = QtWidgets.QPushButton(self)
        self.btn_load_calib_img.setGeometry(QtCore.QRect(50, 130, 211, 61))
        self.btn_load_calib_img.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.btn_load_calib_img.setText("Load Calibration Image")
        self.btn_load_calib_img.setObjectName("btn_load_calib_img")
        
        # Label: "Enter Value Manually"
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(440, 140, 161, 41))
        self.label_2.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.label_2.setText("Enter Value Manually")
        self.label_2.setObjectName("label_2")
        
        # QLineEdit para inserir o valor (pixels que equivalem a 1 cm)
        self.lineEdit_pixel_cm = QtWidgets.QLineEdit(self)
        self.lineEdit_pixel_cm.setGeometry(QtCore.QRect(610, 140, 113, 41))
        self.lineEdit_pixel_cm.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_pixel_cm.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_pixel_cm.setObjectName("lineEdit_pixel_cm")
        
        # Label: "Pixels = 1 cm"
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(740, 140, 101, 41))
        self.label_3.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.label_3.setText("Pixels = 1 cm")
        self.label_3.setObjectName("label_3")
        
        # Botão Save
        self.btnSave = QtWidgets.QPushButton(self)
        self.btnSave.setGeometry(QtCore.QRect(610, 220, 121, 41))
        self.btnSave.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.btnSave.setText("Save")
        self.btnSave.setObjectName("btnSave")
        
        QtCore.QMetaObject.connectSlotsByName(self)
