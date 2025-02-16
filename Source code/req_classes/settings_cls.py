#settings_cls.py

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
from utils_pyqt5 import showdialog
# Importe a classe gerada a partir do arquivo settings_ui.py
from UI_files.settings_ui import Ui_Form

class GlobalSettings(QWidget):
    def __init__(self, mainUi):
        super().__init__()
        # Em vez de loadUi, instancie a classe gerada e configure a interface
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.mainUi = mainUi
        # Conecta os botões usando os atributos definidos na interface
        self.ui.btn_apply.clicked.connect(self.apply_inputs)
        self.ui.btn_cancel.clicked.connect(self.close_window)

        self.mainUi.read_settings()
        self.set_stored_values()
    
    def set_stored_values(self):
        # Atualize os campos com os valores armazenados no mainUi
        self.ui.lineEdit_deadSeedL.setText(str(int(self.mainUi.dead_seed_max_length_r_h)))
        self.ui.lineEdit_abnormal_seedL.setText(str(self.mainUi.abnormal_seed_max_length_r_h))
        self.ui.lineEdit_normal_seedL.setText(str(self.mainUi.normal_seed_max_length_r_h))
        self.ui.lineEdit_avg_rad_length.setText(str(self.mainUi.thres_avg_max_radicle_thickness))
        self.ui.lineEdit_avg_seed_length.setText(str(self.mainUi.user_given_seedling_length))

        self.ui.spinBox_n_seg.setValue(self.mainUi.n_segments_each_skeleton)
        self.ui.doubleSpinBox_pc.setValue(self.mainUi.weights_factor_growth_Pc)
        self.ui.doubleSpinBox_pu.setValue(self.mainUi.weights_factor_uniformity_Pu)
        self.ui.doubleSpinBox_ph.setValue(self.mainUi.p_h)
        self.ui.doubleSpinBox_pr.setValue(self.mainUi.p_r)

    def apply_inputs(self):
        if len(self.ui.lineEdit_deadSeedL.text()) > 0 and self.ui.lineEdit_deadSeedL.text().isnumeric():
            self.mainUi.dead_seed_max_length_r_h = int(self.ui.lineEdit_deadSeedL.text())
            self.mainUi.dict_settings['dead_seed_max_length'] = int(self.ui.lineEdit_deadSeedL.text())
            
        if len(self.ui.lineEdit_abnormal_seedL.text()) > 0 and self.ui.lineEdit_abnormal_seedL.text().isnumeric():
            self.mainUi.abnormal_seed_max_length_r_h = int(self.ui.lineEdit_abnormal_seedL.text())
            self.mainUi.dict_settings['abnormal_seed_max_length'] = int(self.ui.lineEdit_abnormal_seedL.text())
            
        if len(self.ui.lineEdit_normal_seedL.text()) > 0 and self.ui.lineEdit_normal_seedL.text().isnumeric():
            self.mainUi.normal_seed_max_length_r_h = int(self.ui.lineEdit_normal_seedL.text())
            self.mainUi.dict_settings['normal_seed_max_length'] = int(self.ui.lineEdit_normal_seedL.text())

        if len(self.ui.lineEdit_avg_rad_length.text()) > 0 and self.ui.lineEdit_avg_rad_length.text().isnumeric():
            self.mainUi.thres_avg_max_radicle_thickness = int(self.ui.lineEdit_avg_rad_length.text())
            self.mainUi.dict_settings['thresh_avg_max_radicle_thickness'] = int(self.ui.lineEdit_avg_rad_length.text())

        if len(self.ui.lineEdit_avg_seed_length.text()) > 0 and self.ui.lineEdit_avg_seed_length.text().isnumeric():
            self.mainUi.user_given_seedling_length = int(self.ui.lineEdit_avg_seed_length.text())
            self.mainUi.dict_settings['user_given_seedling_length'] = int(self.ui.lineEdit_avg_seed_length.text())
            
        self.mainUi.n_segments_each_skeleton = self.ui.spinBox_n_seg.value()
        self.mainUi.dict_settings['no_of_segments_each_skeleton'] = self.ui.spinBox_n_seg.value()
        self.mainUi.weights_factor_growth_Pc = self.ui.doubleSpinBox_pc.value()
        self.mainUi.dict_settings['weights_factor_growth_Pc'] = self.ui.doubleSpinBox_pc.value()    
        self.mainUi.weights_factor_uniformity_Pu = self.ui.doubleSpinBox_pu.value()
        self.mainUi.dict_settings['weights_factor_uniformity_Pu'] = self.ui.doubleSpinBox_pu.value()

        self.mainUi.p_h = self.ui.doubleSpinBox_ph.value()
        self.mainUi.dict_settings['ph'] = self.ui.doubleSpinBox_ph.value()

        self.mainUi.p_r = self.ui.doubleSpinBox_pr.value()
        self.mainUi.dict_settings['pr'] = self.ui.doubleSpinBox_pr.value()
        
        # Salva as configurações e atualiza a interface principal
        self.mainUi.save_settings_to_file()
        showdialog("Settings saved successfully!!!")
        self.mainUi.process_img_and_display_results()
        self.close_window()

    def close_window(self):
        print("Closing window")
        self.close()