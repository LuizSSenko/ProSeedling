# -*- coding: utf-8 -*-
#
# Código gerado a partir do arquivo .ui
#
# Obs.: Qualquer alteração aqui poderá ser sobrescrita se o .ui for reconvertido.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(798, 633)
        # Style sheet customizado para um visual similar ao Windows 7
        Form.setStyleSheet("""
            QWidget {
                /* Usando o fundo Base (normalmente branco) para uma aparência moderna */
                background-color: #FFFFFF;
                font-family: "Segoe UI", sans-serif;
                font-size: 10pt;
                color: #000000;  /* WindowText */
            }
            QPushButton {
                /* Fundo do botão (Button) */
                background-color: #5E86AB;
                color: #000000;  /* ButtonText */
                border: 1px solid #3F5972;  /* Utilizando Mid (#3F5972) */
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                /* Estado hover usando Midlight (#76A7D5) */
                background-color: #76A7D5;
            }
            QPushButton:pressed {
                /* Estado pressed usando Dark (#2F4355) */
                background-color: #2F4355;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                /* Campos de entrada utilizam o fundo Base e uma borda com AlternateBase */
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #AEC2D5;  /* AlternateBase (#AEC2D5) */
                border-radius: 4px;
                padding: 4px;
            }
            QLabel {
                /* Texto dos labels (WindowText) */
                color: #000000;
            }
            QToolTip {
                background-color: #FFFFDC;  /* ToolTipBase */
                color: #000000;             /* ToolTipText */
                border: 1px solid #2F4355;   /* Dark */
            }
        """)


        self.btn_apply = QtWidgets.QPushButton(Form)
        self.btn_apply.setGeometry(QtCore.QRect(380, 530, 93, 28))
        # A fonte já definida (Segoe UI) complementa o visual do Windows 7
        self.btn_apply.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.btn_apply.setObjectName("btn_apply")
        
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(150, 10, 441, 488))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        
        self.formLayout_left = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout_left.setContentsMargins(0, 0, 0, 0)
        self.formLayout_left.setObjectName("formLayout_left")
        
        # Linha 4: No. of segments of each seed e spinBox_n_seg
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_9.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_9.setObjectName("label_9")
        self.formLayout_left.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_9)
        
        self.spinBox_n_seg = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_n_seg.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.spinBox_n_seg.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_n_seg.setMinimum(10)
        self.spinBox_n_seg.setMaximum(20)
        self.spinBox_n_seg.setProperty("value", 15)
        self.spinBox_n_seg.setObjectName("spinBox_n_seg")
        self.formLayout_left.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinBox_n_seg)
        
        # Linha 5: Average root thickness (pixels) e lineEdit_avg_rad_length
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_8.setObjectName("label_8")
        self.formLayout_left.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_8)
        
        self.lineEdit_avg_rad_length = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_avg_rad_length.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_avg_rad_length.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_avg_rad_length.setObjectName("lineEdit_avg_rad_length")
        self.formLayout_left.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_avg_rad_length)
        
        # Linha 7: Max dead seed length (cm) e lineEdit_deadSeedL
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label.setObjectName("label")
        self.formLayout_left.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label)
        
        self.lineEdit_deadSeedL = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_deadSeedL.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_deadSeedL.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_deadSeedL.setObjectName("lineEdit_deadSeedL")
        self.formLayout_left.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_deadSeedL)
        
        # Linha 8: Abnormal seed max length (cm) e lineEdit_abnormal_seedL
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_2.setObjectName("label_2")
        self.formLayout_left.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_2)
        
        self.lineEdit_abnormal_seedL = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_abnormal_seedL.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_abnormal_seedL.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_abnormal_seedL.setObjectName("lineEdit_abnormal_seedL")
        self.formLayout_left.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEdit_abnormal_seedL)
        
        # Linha 9: Normal seed max length (cm) e lineEdit_normal_seedL
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_5.setObjectName("label_5")
        self.formLayout_left.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_5)
        
        self.lineEdit_normal_seedL = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_normal_seedL.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_normal_seedL.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_normal_seedL.setObjectName("lineEdit_normal_seedL")
        self.formLayout_left.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lineEdit_normal_seedL)
        
        # Linha 10: Average seedling length (cm) e lineEdit_avg_seed_length
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_7.setObjectName("label_7")
        self.formLayout_left.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_7)
        
        self.lineEdit_avg_seed_length = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_avg_seed_length.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.lineEdit_avg_seed_length.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_avg_seed_length.setObjectName("lineEdit_avg_seed_length")
        self.formLayout_left.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEdit_avg_seed_length)
        
        # Linha 13: Spacer horizontal
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout_left.setItem(13, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        
        # Linha 16: Weight Factor Ph e doubleSpinBox_ph
        self.label_12 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_12.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_12.setObjectName("label_12")
        self.formLayout_left.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.label_12)
        
        self.doubleSpinBox_ph = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_ph.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.doubleSpinBox_ph.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_ph.setMinimum(0.0)
        self.doubleSpinBox_ph.setMaximum(1.0)
        self.doubleSpinBox_ph.setSingleStep(0.05)
        self.doubleSpinBox_ph.setValue(0.1)
        self.doubleSpinBox_ph.setObjectName("doubleSpinBox_ph")
        self.formLayout_left.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_ph)
        
        # Linha 17: Weight Factor Pr e doubleSpinBox_pr
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_13.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_13.setObjectName("label_13")
        self.formLayout_left.setWidget(17, QtWidgets.QFormLayout.LabelRole, self.label_13)
        
        self.doubleSpinBox_pr = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_pr.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.doubleSpinBox_pr.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_pr.setMinimum(0.0)
        self.doubleSpinBox_pr.setMaximum(1.0)
        self.doubleSpinBox_pr.setSingleStep(0.05)
        self.doubleSpinBox_pr.setValue(0.9)
        self.doubleSpinBox_pr.setObjectName("doubleSpinBox_pr")
        self.formLayout_left.setWidget(17, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_pr)
        
        # Linha 18: Weight Factor Pu e doubleSpinBox_pu
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_11.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_11.setObjectName("label_11")
        self.formLayout_left.setWidget(18, QtWidgets.QFormLayout.LabelRole, self.label_11)
        
        self.doubleSpinBox_pu = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_pu.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.doubleSpinBox_pu.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_pu.setMaximum(1.0)
        self.doubleSpinBox_pu.setSingleStep(0.05)
        self.doubleSpinBox_pu.setValue(0.7)
        self.doubleSpinBox_pu.setObjectName("doubleSpinBox_pu")
        self.formLayout_left.setWidget(18, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_pu)
        
        # Linha 19: Weight Factor Pc e doubleSpinBox_pc
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_10.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.label_10.setObjectName("label_10")
        self.formLayout_left.setWidget(19, QtWidgets.QFormLayout.LabelRole, self.label_10)
        
        self.doubleSpinBox_pc = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_pc.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.doubleSpinBox_pc.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_pc.setMinimum(0.0)
        self.doubleSpinBox_pc.setMaximum(1.0)
        self.doubleSpinBox_pc.setSingleStep(0.05)
        self.doubleSpinBox_pc.setValue(0.3)
        self.doubleSpinBox_pc.setObjectName("doubleSpinBox_pc")
        self.formLayout_left.setWidget(19, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_pc)
        
        self.btn_cancel = QtWidgets.QPushButton(Form)
        self.btn_cancel.setGeometry(QtCore.QRect(500, 530, 93, 28))
        self.btn_cancel.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.btn_cancel.setObjectName("btn_cancel")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Settings"))
        self.btn_apply.setText(_translate("Form", "Save"))
        self.label_9.setText(_translate("Form", "No. of segments of each seed"))
        self.label_8.setText(_translate("Form", "Average root thickness (pixels)"))
        self.lineEdit_avg_rad_length.setText(_translate("Form", "13"))
        self.label.setText(_translate("Form", "Max dead seed length (cm)"))
        self.lineEdit_deadSeedL.setText(_translate("Form", "80"))
        self.label_2.setText(_translate("Form", "Abnormal seed max length (cm)"))
        self.lineEdit_abnormal_seedL.setText(_translate("Form", "130"))
        self.label_5.setText(_translate("Form", "Normal seed max length (cm)"))
        self.lineEdit_normal_seedL.setText(_translate("Form", "150"))
        self.label_7.setText(_translate("Form", "Average seedling length (cm)"))
        self.lineEdit_avg_seed_length.setText(_translate("Form", "200"))
        self.label_12.setText(_translate("Form", "Weight Factor Ph"))
        self.label_13.setText(_translate("Form", "Weight Factor Pr"))
        self.label_11.setText(_translate("Form", "Weight Factor Pu"))
        self.label_10.setText(_translate("Form", "Weight Factor Pc"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))
