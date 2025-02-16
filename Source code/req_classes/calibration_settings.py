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
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog
import utils_pyqt5 as ut

# ----------------------------------------------------------------------------
# FUNÇÃO DE CONVERSÃO: get_pixel_to_cm
# ----------------------------------------------------------------------------
def get_pixel_to_cm(img, checkerboard_size=(28,20)):
    """
    Dada uma imagem contendo um checkerboard (tabuleiro de xadrez),
    calcula o tamanho médio de um quadrado (em pixels) e retorna o fator
    de conversão: número de pixels que equivalem a 1 cm.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(
        gray, checkerboard_size,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    )
    if ret:
        square_size_pixels = []
        # Cálculo das distâncias horizontais
        for i in range(checkerboard_size[1]-1):
            for j in range(checkerboard_size[0]-1):
                p1 = corners[j + i * checkerboard_size[0]]
                p2 = corners[j + i * checkerboard_size[0] + 1]
                distance = np.sqrt(((p1 - p2) ** 2).sum())
                square_size_pixels.append(distance)
        # Cálculo das distâncias verticais
        for i in range(checkerboard_size[0]):
            for j in range(checkerboard_size[1]-1):
                p1 = corners[i + j * checkerboard_size[0]]
                p2 = corners[i + (j+1) * checkerboard_size[0]]
                distance = np.sqrt(((p1 - p2) ** 2).sum())
                square_size_pixels.append(distance)
        average_square_size_pixels = np.mean(square_size_pixels)
        # Se 1 cm corresponde a average_square_size_pixels, o fator (pixels por cm) é:
        pixel_per_cm = np.round(average_square_size_pixels)
        print(f"Conversion factor: {pixel_per_cm} pixels = 1 cm")
        return int(pixel_per_cm)
    else:
        print("Could not find chessboard corners")
        return None

# ----------------------------------------------------------------------------
# CLASSE DE CALIBRAÇÃO: CalibrationSettings
# ----------------------------------------------------------------------------
# Aqui usamos a interface convertida para Python (já que você quer trabalhar com o .py, não com o .ui)
from UI_files.pixel_cm_setting_ui import Ui_Form

class CalibrationSettings(QtWidgets.QDialog, Ui_Form):
    def __init__(self, mainUi, parent=None):
        super().__init__(parent)
        self.mainUi = mainUi  # Referência à interface principal para acessar e salvar configurações
        self.setupUi()       # Configura a interface a partir do arquivo .py convertido

        # Atualiza as configurações atuais (por exemplo, lendo settings.json)
        self.mainUi.read_settings()
        # Preenche o QLineEdit com o valor atual, se houver, para o fator de conversão
        self.lineEdit_pixel_cm.setText(str(self.mainUi.dict_settings.get('factor_pixel_to_cm', '')))

        # Conecta os botões aos métodos correspondentes
        self.btn_load_calib_img.clicked.connect(self.load_calib_image)
        self.btnSave.clicked.connect(self.saveSetting)

        # Define o tamanho do checkerboard (ajuste conforme necessário)
        self.checkerboard_size = (28,20)

    def load_calib_image(self):
        # Abre um diálogo para selecionar a imagem de calibração
        filepath, _ = QFileDialog.getOpenFileName(self, 'Select Calibration Image', '', "Image Files (*.jpg *.png *.bmp)")
        if not filepath or not os.path.exists(filepath):
            ut.showdialog("Please select a file")
        else:
            try:
                img = cv2.imread(filepath)
                if img is None:
                    raise ValueError("File is not a valid image.")
                
                # Calcula o fator de conversão
                result_pixel_per_cm = get_pixel_to_cm(img, self.checkerboard_size)
                if result_pixel_per_cm is not None:
                    self.mainUi.pixel_per_cm = result_pixel_per_cm
                    self.mainUi.dict_settings['factor_pixel_to_cm'] = result_pixel_per_cm
                    self.lineEdit_pixel_cm.setText(str(result_pixel_per_cm))
                    
                    ut.showdialog(f"Calibration done! \n {result_pixel_per_cm} pixels = 1 cm.")
                    self.mainUi.save_settings_to_file()
                    self.mainUi.process_img_and_display_results()
                else:
                    ut.showdialog("Calibration not done! \n Image could not be processed.")
            except Exception as e:
                ut.showdialog(f"Error: {str(e)}")
            self.close()

    def saveSetting(self):
        # Salva o valor inserido manualmente, se for um número inteiro positivo
        if len(self.lineEdit_pixel_cm.text()) > 0 and self.lineEdit_pixel_cm.text().isnumeric():
            pixel_value = int(self.lineEdit_pixel_cm.text())
            self.mainUi.pixel_per_cm = pixel_value
            self.mainUi.dict_settings['factor_pixel_to_cm'] = pixel_value
            print("Saving settings:", self.dict_settings)
            self.mainUi.save_settings_to_file()
            ut.showdialog(f"Saved! \n {pixel_value} pixels = 1 cm.\nSaved in settings.")
            self.mainUi.process_img_and_display_results()
        else:
            ut.showdialog("Please enter a positive integer value.")
        self.close()
