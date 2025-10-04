from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 100)
        Form.setStyleSheet("""
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
        Form.setWindowTitle("Calibration: Pixel to Centimeters")
        
        # Layout principal (vertical)
        mainLayout = QtWidgets.QVBoxLayout(Form)
        
        # Título centralizado no topo
        self.label = QtWidgets.QLabel("Calibration : Pixel to Centimeters", Form)
        self.label.setStyleSheet("font: 83 12pt \"Segoe UI\" bold;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.label)
        
        # Layout horizontal para o conteúdo central
        contentLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(contentLayout)
        
        # Coluna da esquerda: botão para carregar imagem de calibração
        leftLayout = QtWidgets.QVBoxLayout()
        self.btn_load_calib_img = QtWidgets.QPushButton("Load Calibration Image", Form)
        self.btn_load_calib_img.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        leftLayout.addWidget(self.btn_load_calib_img)
        leftLayout.addStretch()  # empurra o conteúdo para o topo
        contentLayout.addLayout(leftLayout)
        
        # Coluna da direita: entrada manual e botões
        rightLayout = QtWidgets.QVBoxLayout()
        
        # Linha de entrada manual: rótulo, QLineEdit e rótulo "Pixels = 1 cm"
        manualLayout = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel("Enter Value Manually", Form)
        self.label_2.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        manualLayout.addWidget(self.label_2)
        
        self.lineEdit_pixel_cm = QtWidgets.QLineEdit(Form)
        self.lineEdit_pixel_cm.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_pixel_cm.setAlignment(QtCore.Qt.AlignCenter)
        manualLayout.addWidget(self.lineEdit_pixel_cm)
        
        self.label_3 = QtWidgets.QLabel("Pixels = 1 cm", Form)
        self.label_3.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        manualLayout.addWidget(self.label_3)
        
        rightLayout.addLayout(manualLayout)
        
        # Linha para os botões: "Restore" à esquerda de "Save"
        saveLayout = QtWidgets.QHBoxLayout()
        saveLayout.addStretch()  # espaço à esquerda para alinhar à direita
        
        # Botão Restore
        self.btn_restore = QtWidgets.QPushButton("Restore", Form)
        self.btn_restore.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.btn_restore.setObjectName("btn_restore")
        saveLayout.addWidget(self.btn_restore)
        
        # Botão Save
        self.btnSave = QtWidgets.QPushButton("Save", Form)
        self.btnSave.setStyleSheet("font: 63 10pt \"Segoe UI\" bold;")
        self.btnSave.setObjectName("btnSave")
        saveLayout.addWidget(self.btnSave)
        
        rightLayout.addLayout(saveLayout)
        
        rightLayout.addStretch()
        contentLayout.addLayout(rightLayout)
        
        mainLayout.addStretch()
        
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Calibration: Pixel to Centimeters"))
        self.label.setText(_translate("Form", "Calibration : Pixel to Centimeters"))
        self.btn_load_calib_img.setText(_translate("Form", "Load Calibration Image"))
        self.label_2.setText(_translate("Form", "Enter Value Manually"))
        self.label_3.setText(_translate("Form", "Pixels = 1 cm"))
        self.btn_restore.setText(_translate("Form", "Restore"))
        self.btnSave.setText(_translate("Form", "Save"))
