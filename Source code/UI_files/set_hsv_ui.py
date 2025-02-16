from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 702)
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

        # Main horizontal layout divides controls and image display
        self.mainLayout = QtWidgets.QHBoxLayout(Form)

        # -------------------------------
        # Left side: Controls
        # -------------------------------
        self.controlsLayout = QtWidgets.QVBoxLayout()

        # Upload image button
        self.btn_upload_img = QtWidgets.QPushButton("Upload Image")
        self.btn_upload_img.setStyleSheet("font: 63 10pt 'Segoe UI';")
        self.controlsLayout.addWidget(self.btn_upload_img)

        # Radio buttons for seed parts
        self.radioHSV_seed_head = QtWidgets.QRadioButton("Set Values for cotyledon")
        self.radioHSV_seed_head.setStyleSheet("font: 63 10pt 'Segoe UI';")
        self.radioHSV_seed_head.setChecked(True)
        self.radio_hsv_seed_body = QtWidgets.QRadioButton("Set Values for hypocotyl and root")
        self.radio_hsv_seed_body.setStyleSheet("font: 63 10pt 'Segoe UI';")
        self.controlsLayout.addWidget(self.radioHSV_seed_head)
        self.controlsLayout.addWidget(self.radio_hsv_seed_body)

        # Group box for HSV sliders and their value labels
        sliderGroup = QtWidgets.QGroupBox("HSV Values")
        sliderGroup.setStyleSheet("font: 63 10pt 'Segoe UI';")
        sliderLayout = QtWidgets.QGridLayout()

        # H min
        sliderLayout.addWidget(QtWidgets.QLabel("H min"), 0, 0)
        self.slider_hmin = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_hmin.setRange(0, 179)
        self.slider_hmin.setValue(0)
        sliderLayout.addWidget(self.slider_hmin, 0, 1)
        self.label_hmin = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.label_hmin, 0, 2)

        # H max
        sliderLayout.addWidget(QtWidgets.QLabel("H max"), 1, 0)
        self.slider_hmax = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_hmax.setRange(0, 179)
        self.slider_hmax.setValue(179)
        sliderLayout.addWidget(self.slider_hmax, 1, 1)
        self.label_hmax = QtWidgets.QLabel("179")
        sliderLayout.addWidget(self.label_hmax, 1, 2)

        # S min
        sliderLayout.addWidget(QtWidgets.QLabel("S min"), 2, 0)
        self.slider_smin = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_smin.setRange(0, 255)
        self.slider_smin.setValue(0)
        sliderLayout.addWidget(self.slider_smin, 2, 1)
        self.label_smin = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.label_smin, 2, 2)

        # S max
        sliderLayout.addWidget(QtWidgets.QLabel("S max"), 3, 0)
        self.slider_smax = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_smax.setRange(0, 255)
        self.slider_smax.setValue(255)
        sliderLayout.addWidget(self.slider_smax, 3, 1)
        self.label_smax = QtWidgets.QLabel("255")
        sliderLayout.addWidget(self.label_smax, 3, 2)

        # V min
        sliderLayout.addWidget(QtWidgets.QLabel("V min"), 4, 0)
        self.slider_vmin = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_vmin.setRange(0, 255)
        self.slider_vmin.setValue(0)
        sliderLayout.addWidget(self.slider_vmin, 4, 1)
        self.label_vmin = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.label_vmin, 4, 2)

        # V max
        sliderLayout.addWidget(QtWidgets.QLabel("V max"), 5, 0)
        self.slider_vmax = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_vmax.setRange(0, 255)
        self.slider_vmax.setValue(255)
        sliderLayout.addWidget(self.slider_vmax, 5, 1)
        self.label_vmax = QtWidgets.QLabel("255")
        sliderLayout.addWidget(self.label_vmax, 5, 2)

        sliderGroup.setLayout(sliderLayout)
        self.controlsLayout.addWidget(sliderGroup)

        # Save and Cancel buttons
        self.btnLayout = QtWidgets.QHBoxLayout()
        self.btnSave = QtWidgets.QPushButton("Save")
        self.btnSave.setStyleSheet("font: 63 10pt 'Segoe UI';")
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        self.btnCancel.setStyleSheet("font: 63 10pt 'Segoe UI';")
        self.btnLayout.addWidget(self.btnSave)
        self.btnLayout.addWidget(self.btnCancel)
        self.controlsLayout.addLayout(self.btnLayout)

        # Connect slider signals to update their value labels
        self.slider_hmin.valueChanged.connect(lambda value: self.label_hmin.setText(str(value)))
        self.slider_hmax.valueChanged.connect(lambda value: self.label_hmax.setText(str(value)))
        self.slider_smin.valueChanged.connect(lambda value: self.label_smin.setText(str(value)))
        self.slider_smax.valueChanged.connect(lambda value: self.label_smax.setText(str(value)))
        self.slider_vmin.valueChanged.connect(lambda value: self.label_vmin.setText(str(value)))
        self.slider_vmax.valueChanged.connect(lambda value: self.label_vmax.setText(str(value)))

        self.mainLayout.addLayout(self.controlsLayout, 1)  # Left side takes 1/3 of the space

        # -------------------------------
        # Right side: Image Display
        # -------------------------------
        self.imageLayout = QtWidgets.QVBoxLayout()
        self.imgLabel_hsv = QtWidgets.QLabel()
        self.imgLabel_hsv.setScaledContents(True)
        self.imgLabel_hsv.setStyleSheet("background-color: #CCCCCC;")  # Gray background for visibility
        self.imgLabel_hsv.setMinimumSize(400, 400)
        self.imageLayout.addWidget(self.imgLabel_hsv)
        self.mainLayout.addLayout(self.imageLayout, 2)  # Right side gets more space

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Set HSV"))
