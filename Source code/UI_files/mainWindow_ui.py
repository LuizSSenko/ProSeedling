# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.setStyleSheet("""
        QMainWindow {
            background-color: rgb(94, 134, 171);
        }
    """)
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1321, 696)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 134, 171))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(142, 201, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(118, 167, 213))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(47, 67, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 89, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(94, 134, 171))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(174, 194, 213))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        # (As configurações de cor para Inactive e Disabled são repetidas...)
        # ... No código gerado pelo pyuic5, essas configurações se repetem
        MainWindow.setPalette(palette)
        MainWindow.setWindowTitle("Germination Vigor Analyser")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Layout para a imagem (horizontal)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 711, 401))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.h_layout_img = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.h_layout_img.setContentsMargins(0, 0, 0, 0)
        self.h_layout_img.setObjectName("h_layout_img")

        # Logo no canto superior (vertical layout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(840, 0, 451, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_logo = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.label_logo)

        # Botões 'anterior', 'próximo' e label de número de imagem
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(130, 430, 511, 61))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnPrev = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.btnPrev.setObjectName("btnPrev")
        self.btnPrev.setToolTip("Past image")
        self.btnPrev.setToolTipDuration(2000)
        self.btnPrev.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.horizontalLayout_3.addWidget(self.btnPrev)
        self.label_img_no = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_img_no.setObjectName("label_img_no")
        self.label_img_no.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_img_no.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_3.addWidget(self.label_img_no)
        self.btnNext = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.btnNext.setObjectName("btnNext")
        self.btnNext.setToolTip("Next image")
        self.btnNext.setToolTipDuration(1000)
        self.btnNext.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.horizontalLayout_3.addWidget(self.btnNext)

        # Grid layout (direita) - informações do arquivo, cultivar, analista, etc.
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(830, 70, 461, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_right = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_right.setObjectName("gridLayout_right")
        self.gridLayout_right.setHorizontalSpacing(17)

        # Labels e campos
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_right.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_fileName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_fileName.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_fileName.setText("")
        self.label_fileName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fileName.setObjectName("label_fileName")
        self.gridLayout_right.addWidget(self.label_fileName, 0, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_right.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_cult_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_cult_name.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_cult_name.setText("")
        self.label_cult_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cult_name.setObjectName("label_cult_name")
        self.gridLayout_right.addWidget(self.label_cult_name, 1, 1, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_right.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_analys_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_analys_name.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_analys_name.setText("")
        self.label_analys_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_analys_name.setObjectName("label_analys_name")
        self.gridLayout_right.addWidget(self.label_analys_name, 2, 1, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_right.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_batchNo = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_batchNo.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_batchNo.setText("")
        self.label_batchNo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_batchNo.setObjectName("label_batchNo")
        self.gridLayout_right.addWidget(self.label_batchNo, 3, 1, 1, 1)

        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_right.addWidget(self.label_8, 4, 0, 1, 1)
        self.label_n_plants = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_n_plants.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_n_plants.setText("")
        self.label_n_plants.setAlignment(QtCore.Qt.AlignCenter)
        self.label_n_plants.setObjectName("label_n_plants")
        self.gridLayout_right.addWidget(self.label_n_plants, 4, 1, 1, 1)

        # Tabela de resultados
        self.tableView_res = QtWidgets.QTableView(self.centralwidget)
        self.tableView_res.setEnabled(True)
        self.tableView_res.setGeometry(QtCore.QRect(830, 220, 461, 421))
        self.tableView_res.setAutoFillBackground(True)
        self.tableView_res.setObjectName("tableView_res")

        # Layout inferior (grid) - métricas, vigor, germinação etc.
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 510, 771, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")

        # Labels
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        self.label_13.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                    "font: 63 10pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(32, 24, 255);\n"
                                    "border-radius:4;")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_growth = QtWidgets.QLabel(self.layoutWidget)
        self.label_growth.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_growth.setText("")
        self.label_growth.setAlignment(QtCore.Qt.AlignCenter)
        self.label_growth.setObjectName("label_growth")
        self.gridLayout.addWidget(self.label_growth, 2, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_germination = QtWidgets.QLabel(self.layoutWidget)
        self.label_germination.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_germination.setText("")
        self.label_germination.setAlignment(QtCore.Qt.AlignCenter)
        self.label_germination.setObjectName("label_germination")
        self.gridLayout.addWidget(self.label_germination, 4, 0, 1, 1)

        self.label_16 = QtWidgets.QLabel(self.layoutWidget)
        self.label_16.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                    "font: 63 10pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(32, 24, 255);\n"
                                    "border-radius:4;")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_sd = QtWidgets.QLabel(self.layoutWidget)
        self.label_sd.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_sd.setText("")
        self.label_sd.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sd.setObjectName("label_sd")
        self.gridLayout.addWidget(self.label_sd, 2, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                 "font: 63 10pt \"Segoe UI Semibold\";\n"
                                 "color: rgb(32, 24, 255);\n"
                                 "border-radius:4;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)

        self.label_avg_hypocotyl = QtWidgets.QLabel(self.layoutWidget)
        self.label_avg_hypocotyl.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_avg_hypocotyl.setText("")
        self.label_avg_hypocotyl.setAlignment(QtCore.Qt.AlignCenter)
        self.label_avg_hypocotyl.setObjectName("label_avg_hypocotyl")
        self.gridLayout.addWidget(self.label_avg_hypocotyl, 4, 1, 1, 1)

        self.label_15 = QtWidgets.QLabel(self.layoutWidget)
        self.label_15.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                    "font: 63 10pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(32, 24, 255);\n"
                                    "border-radius:4;")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 0, 2, 1, 1)

        self.label_uniformity = QtWidgets.QLabel(self.layoutWidget)
        self.label_uniformity.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_uniformity.setText("")
        self.label_uniformity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_uniformity.setObjectName("label_uniformity")
        self.gridLayout.addWidget(self.label_uniformity, 2, 2, 1, 1)

        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                   "font: 63 10pt \"Segoe UI Semibold\";\n"
                                   "color: rgb(32, 24, 255);\n"
                                   "border-radius:4;")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 2, 1, 1)

        self.label_avg_root = QtWidgets.QLabel(self.layoutWidget)
        self.label_avg_root.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_avg_root.setText("")
        self.label_avg_root.setAlignment(QtCore.Qt.AlignCenter)
        self.label_avg_root.setObjectName("label_avg_root")
        self.gridLayout.addWidget(self.label_avg_root, 4, 2, 1, 1)

        self.label_12 = QtWidgets.QLabel(self.layoutWidget)
        self.label_12.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                    "font: 63 10pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(32, 24, 255);\n"
                                    "border-radius:4;")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 3, 1, 1)

        self.label_seedvigor = QtWidgets.QLabel(self.layoutWidget)
        self.label_seedvigor.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_seedvigor.setText("")
        self.label_seedvigor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_seedvigor.setObjectName("label_seedvigor")
        self.gridLayout.addWidget(self.label_seedvigor, 2, 3, 1, 1)

        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setStyleSheet("background-color:rgba(216, 229, 253,255);\n"
                                    "font: 63 10pt \"Segoe UI Semibold\";\n"
                                    "color: rgb(32, 24, 255);\n"
                                    "border-radius:4;")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 3, 1, 1)

        self.label_avg_total_length = QtWidgets.QLabel(self.layoutWidget)
        self.label_avg_total_length.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.label_avg_total_length.setText("")
        self.label_avg_total_length.setAlignment(QtCore.Qt.AlignCenter)
        self.label_avg_total_length.setObjectName("label_avg_total_length")
        self.gridLayout.addWidget(self.label_avg_total_length, 4, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu e status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1321, 23))
        self.menubar.setStyleSheet("font: 63 10pt \"Segoe UI\";")
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Actions
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionSelect_Output_Folder = QtWidgets.QAction(MainWindow)
        self.actionSelect_Output_Folder.setObjectName("actionSelect_Output_Folder")
        self.actionSet_HSV_threshold = QtWidgets.QAction(MainWindow)
        self.actionSet_HSV_threshold.setObjectName("actionSet_HSV_threshold")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Germination Vigor Analyser"))
        self.label_logo.setText(_translate("MainWindow", ""))

        self.btnPrev.setText(_translate("MainWindow", "<"))
        self.label_img_no.setText(_translate("MainWindow", ""))
        self.btnNext.setText(_translate("MainWindow", ">"))

        self.label_2.setText(_translate("MainWindow", "File Name"))
        self.label_3.setText(_translate("MainWindow", "Cultivar Name"))
        self.label_4.setText(_translate("MainWindow", "Analyst Name"))
        self.label_6.setText(_translate("MainWindow", "Lot No."))
        self.label_8.setText(_translate("MainWindow", "No. of Seedlings"))

        self.label_13.setText(_translate("MainWindow", "Growth"))
        self.label_5.setText(_translate("MainWindow", "Germination"))
        self.label_16.setText(_translate("MainWindow", "Standard Deviation"))
        self.label.setText(_translate("MainWindow", "Avg Hypocotyl Length (cm)"))
        self.label_15.setText(_translate("MainWindow", "Uniformity"))
        self.label_9.setText(_translate("MainWindow", "Avg Root length (cm)"))
        self.label_12.setText(_translate("MainWindow", "Vigor"))
        self.label_10.setText(_translate("MainWindow", "Avg Total Length (cm)"))

        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))
        self.actionSelect_Output_Folder.setText(_translate("MainWindow", "Select Output Folder"))
        self.actionSet_HSV_threshold.setText(_translate("MainWindow", "Set HSV threshold"))
