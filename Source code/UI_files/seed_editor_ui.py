# seed_editor_ui.py



from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(856, 533)
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
            QLineEdit, QSpinBox, QDoubleSpinBox {
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
        self.setWindowTitle("Seed Editor")

        # --- Main Horizontal Layout ---
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # Left Side: Image/Drawing Area
        self.leftWidget = QtWidgets.QWidget(self)
        self.leftWidget.setObjectName("leftWidget")
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(0)
        self.imgLabel = QtWidgets.QLabel(self.leftWidget)
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLabel.setStyleSheet("background-color: #CCCCCC;")
        self.imgLabel.setMinimumSize(400, 400)
        self.imgLabel.setText("Image / Drawing Area")
        self.leftLayout.addWidget(self.imgLabel)
        self.mainLayout.addWidget(self.leftWidget, 2)  # Give left side more space


        # Right Side: Controls (arranged vertically)
        self.rightWidget = QtWidgets.QWidget(self)
        self.rightWidget.setObjectName("rightWidget")
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightWidget)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(10)

        # --- Top: Information Grid ---
        self.gridLayoutWidget = QtWidgets.QWidget(self.rightWidget)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        # Row 0: Seed No.
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0)
        self.label_seed_no = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_seed_no.setObjectName("label_seed_no")
        self.gridLayout.addWidget(self.label_seed_no, 0, 1)
        # Row 1: Hypocotyl Length
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0)
        self.label_hypocotyl_length = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_hypocotyl_length.setObjectName("label_hypocotyl_length")
        self.gridLayout.addWidget(self.label_hypocotyl_length, 1, 1)
        # Row 2: Root Length
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0)
        self.label_root_length = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_root_length.setObjectName("label_root_length")
        self.gridLayout.addWidget(self.label_root_length, 2, 1)
        # Row 3: Total Length
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0)
        self.label_total_length = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_total_length.setObjectName("label_total_length")
        self.gridLayout.addWidget(self.label_total_length, 3, 1)
        # Row 4: Status
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0)
        self.label_seed_health = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_seed_health.setObjectName("label_seed_health")
        self.gridLayout.addWidget(self.label_seed_health, 4, 1)
        self.rightLayout.addWidget(self.gridLayoutWidget)

        # --- Middle: Drawing Buttons (Hypocotyl & Root) ---
        self.drawButtonsLayout = QtWidgets.QHBoxLayout()
        self.drawButtonsLayout.setSpacing(10)
        self.btnDrawHyp = QtWidgets.QPushButton(self.rightWidget)
        self.btnDrawHyp.setCheckable(True)
        self.btnDrawHyp.setObjectName("btnDrawHyp")
        self.drawButtonsLayout.addWidget(self.btnDrawHyp)
        self.btnDrawRoot = QtWidgets.QPushButton(self.rightWidget)
        self.btnDrawRoot.setCheckable(True)
        self.btnDrawRoot.setObjectName("btnDrawRoot")
        self.drawButtonsLayout.addWidget(self.btnDrawRoot)
        self.rightLayout.addLayout(self.drawButtonsLayout)

        # --- Next: Other Buttons (Eraser and BreakPoint) ---
        self.otherButtonsLayout = QtWidgets.QHBoxLayout()
        self.otherButtonsLayout.setSpacing(10)
        self.btnEraser = QtWidgets.QPushButton(self.rightWidget)
        self.btnEraser.setCheckable(True)
        self.btnEraser.setObjectName("btnEraser")
        self.otherButtonsLayout.addWidget(self.btnEraser)
        self.btnPoint = QtWidgets.QPushButton(self.rightWidget)
        self.btnPoint.setObjectName("btnPoint")
        self.otherButtonsLayout.addWidget(self.btnPoint)
        self.rightLayout.addLayout(self.otherButtonsLayout)

        # --- Bottom: Group Box for "Change to" ---
        self.groupBox = QtWidgets.QGroupBox(self.rightWidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBoxLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.groupBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBoxLayout.setSpacing(5)
        self.radioBtnNormalSeed = QtWidgets.QRadioButton(self.groupBox)
        self.radioBtnNormalSeed.setObjectName("radioBtnNormalSeed")
        self.groupBoxLayout.addWidget(self.radioBtnNormalSeed)
        self.radioBtnAbnormalSeed = QtWidgets.QRadioButton(self.groupBox)
        self.radioBtnAbnormalSeed.setObjectName("radioBtnAbnormalSeed")
        self.groupBoxLayout.addWidget(self.radioBtnAbnormalSeed)
        self.radioBtnDeadSeed = QtWidgets.QRadioButton(self.groupBox)
        self.radioBtnDeadSeed.setObjectName("radioBtnDeadSeed")
        self.groupBoxLayout.addWidget(self.radioBtnDeadSeed)
        self.rightLayout.addWidget(self.groupBox)

        # Add right side to main layout
        self.mainLayout.addWidget(self.rightWidget, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Seed Editor"))
        self.label_7.setText(_translate("Form", "Seed No."))
        self.label.setText(_translate("Form", "Hypocotyl Length"))
        self.label_2.setText(_translate("Form", "Root Length"))
        self.label_3.setText(_translate("Form", "Total Length"))
        self.label_4.setText(_translate("Form", "Status"))
        self.label_total_length.setText(_translate("Form", ""))
        self.label_seed_no.setText(_translate("Form", ""))
        self.label_seed_health.setText(_translate("Form", ""))
        self.label_root_length.setText(_translate("Form", ""))
        self.label_hypocotyl_length.setText(_translate("Form", ""))
        self.btnDrawHyp.setText(_translate("Form", "Draw Hypocotyl (1)"))
        self.btnDrawRoot.setText(_translate("Form", "Draw Root (2)"))
        self.btnEraser.setText(_translate("Form", "Eraser (e)"))
        self.btnPoint.setText(_translate("Form", "BreakPoint (b)"))
        self.groupBox.setTitle(_translate("Form", "Change to"))
        self.radioBtnNormalSeed.setText(_translate("Form", " Normal Seed (n)"))
        self.radioBtnAbnormalSeed.setText(_translate("Form", " Abnormal Seed (a)"))
        self.radioBtnDeadSeed.setText(_translate("Form", " Dead Seed (d)"))
