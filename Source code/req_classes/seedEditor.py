from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog, show_cv2_img_on_label_obj
from utils import *
from req_classes.contour_processor import Seed
from proj_settings import SeedHealth
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import cv2
import numpy as np
from UI_files.seed_editor_ui import Ui_Form 


class CanvasLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Remove hardcoded geometry and scaling of contents
        self.setMinimumSize(300, 300)
        # We no longer use setScaledContents(True)
        
        # Store the original pixmap here
        self.originalPixmap = None
        # These values will be updated during painting:
        self.scaledPixmap = None
        self.offset_x = 0
        self.offset_y = 0

        self.seedEditor = None
        self.imgW = 0  # original image width
        self.imgH = 0  # original image height
        
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = False
        self.last_x, self.last_y = None, None
        self.pen_draw_color = [0, 255, 0]
        self.pen_thickness = 2
        self.pen_thickness_eraser = 20
        self.pen_color_mask = QtGui.QColor('black')
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.updated_img = None

    def apply_cv2_image(self, imgcv2):
        self.imgH, self.imgW = imgcv2.shape[:2]
        rgb_image = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
        PIL_image = Image.fromarray(rgb_image.copy()).convert('RGB')
        imMask = ImageQt(PIL_image).copy()
        self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
        self.update()  # trigger repaint

    def reset_img(self):
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.originalPixmap:
            # Scale the original pixmap to fit the label while keeping aspect ratio
            self.scaledPixmap = self.originalPixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Center the pixmap in the label
            self.offset_x = (self.width() - self.scaledPixmap.width()) // 2
            self.offset_y = (self.height() - self.scaledPixmap.height()) // 2
            painter.drawPixmap(self.offset_x, self.offset_y, self.scaledPixmap)
        else:
            super().paintEvent(event)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        # Map widget coordinate to image coordinate using the scaled pixmap's size and offsets
        x = ev.x() - self.offset_x
        y = ev.y() - self.offset_y
        if self.scaledPixmap and 0 <= x <= self.scaledPixmap.width() and 0 <= y <= self.scaledPixmap.height():
            self.last_x = int(x / self.scaledPixmap.width() * self.imgW)
            self.last_y = int(y / self.scaledPixmap.height() * self.imgH)
        else:
            self.last_x, self.last_y = None, None
        return super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        x = ev.x() - self.offset_x
        y = ev.y() - self.offset_y
        if self.scaledPixmap and 0 <= x <= self.scaledPixmap.width() and 0 <= y <= self.scaledPixmap.height():
            drawX = int(x / self.scaledPixmap.width() * self.imgW)
            drawY = int(y / self.scaledPixmap.height() * self.imgH)
        else:
            return super().mouseMoveEvent(ev)

        # Now use drawX and drawY as before
        if self.last_x is None:
            self.last_x, self.last_y = drawX, drawY
            return super().mouseMoveEvent(ev)

        # (Your existing drawing logic follows, replacing self.drawX/self.drawY with these computed values)
        if self.breakPointActive:
            rgb_image = cv2.cvtColor(self.seedObj.singlBranchBinaryImg, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()  # Force repaint so offsets update
            painter = QPainter(self.originalPixmap)
            p = painter.pen()
            closest_point_cnt = find_closest_point(contour=self.seedObj.sorted_point_list, point=(drawY, drawX))
            self.pen_color_mask = QtGui.QColor('blue')
            p.setWidth(20)
            p.setColor(self.pen_color_mask)
            painter.setPen(p)
            qPoint = QPoint(closest_point_cnt[1], closest_point_cnt[0])
            painter.drawPoint(qPoint)
            painter.end()
            self.seedObj.reassign_points(new_break_point=closest_point_cnt)
            self.last_x, self.last_y = drawX, drawY
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()
        elif self.eraserActive:
            closest_points_list_ = find_closest_n_points(
                contour=self.seedObj.sorted_point_list,
                point=(drawY, drawX),
                no_points=self.pen_thickness_eraser
            )
            self.update()
            self.seedEditor.update()
            for pnt in closest_points_list_:
                if find_dist(pnt, (drawY, drawX)) < 10:
                    self.seedObj.erase_points(point=pnt)
            self.last_x, self.last_y = drawX, drawY
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()
        elif self.penHypActive or self.penRootActive:
            # For drawing lines, create a temporary blank image matching the original dimensions
            blank = np.zeros((self.imgH, self.imgW), np.uint8)
            cv2.line(blank, (self.last_x, self.last_y), (drawX, drawY), 255, thickness=1)
            points = np.argwhere(blank == 255).tolist()
            if self.penHypActive:
                self.seedObj.add_hypercotyl_points(points)
            elif self.penRootActive:
                self.seedObj.add_root_points(points)
            self.last_x, self.last_y = drawX, drawY
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()

        self.seedEditor.update_values()
        QApplication.restoreOverrideCursor()
        return super().mouseMoveEvent(ev)


class SeedEditor(QtWidgets.QDialog, Ui_Form):
    def __init__(self, mainUi, parent=None):
        super().__init__(parent)
        self.mainUi = mainUi
        self.setupUi()  # This method comes from Ui_Form.
        self.setWindowIconText("Seed ")
        
        # SEED RELATED
        self.seedObj: Seed = None
        self.seedNo = 0
        
        # CHECK BUTTONS
        self.btngroup1 = QtWidgets.QButtonGroup()
        self.btngroup1.addButton(self.radioBtnNormalSeed)
        self.btngroup1.addButton(self.radioBtnAbnormalSeed)
        self.btngroup1.addButton(self.radioBtnDeadSeed)
        self.radioBtnNormalSeed.toggle()
        self.radioBtnNormalSeed.toggled.connect(self.checkRadio)
        self.radioBtnAbnormalSeed.toggled.connect(self.checkRadio)
        self.radioBtnDeadSeed.toggled.connect(self.checkRadio)
        self.radioBtnNormalSeed.setShortcut('n')
        self.radioBtnAbnormalSeed.setShortcut('a')
        self.radioBtnDeadSeed.setShortcut('d')
        
        # EDITION BUTTONS
        self.btnEraser.clicked.connect(self.use_eraser)
        self.btnPoint.clicked.connect(self.use_breakPoint)
        self.btnDrawHyp.clicked.connect(self.use_pen_hyp)
        self.btnEraser.setShortcut('e')
        self.btnPoint.setShortcut('b')
        self.btnDrawHyp.setShortcut('1')
        self.btnDrawRoot.setShortcut('2')
        self.eraserActive = False
        self.breakPointActive = False
        
        # CANVAS RELATED
        self.btnDrawRoot.clicked.connect(self.use_pen_root)
        self.canvasMask_seededitor = None
        self.last_x, self.last_y = None, None
        self.pen_draw_color = [0, 255, 0]
        self.pen_thickness = 2
        self.pen_color_mask = QtGui.QColor('white')
        self.imgH = 0
        self.imgW = 0
        self.delta_x = 390 
        self.delta_y = 30
        self.maxImgHt = 800

        # Instead of directly adding the canvas, wrap it in a scroll area
        self.imgLabel.hide()  # Hide the placeholder
        self.scrollArea = QtWidgets.QScrollArea(self.leftWidget)
        self.scrollArea.setWidgetResizable(True)
        self.customLabel = CanvasLabel(self.scrollArea)
        self.customLabel.setObjectName("img_label_mask")
        self.customLabel.seedEditor = self
        self.scrollArea.setWidget(self.customLabel)
        self.leftLayout.addWidget(self.scrollArea)

        # BUTTONS STYLESHEET
        self.btnClickedStylesheet = '''background-color:rgba(216, 229, 253,50);
                        font: 63 10pt "Segoe UI Semibold";
                        color: rgb(32, 24, 255);
                        border-radius:4;'''
        self.btnNotClickedStylesheet = '''background-color:rgba(216, 229, 253,255);
                        font: 63 10pt "Segoe UI Semibold";
                        color: rgb(32, 24, 255);
                        border-radius:4;'''

    def save_changes(self):
        print("saving changes")
        # Save the current pixmap (you may want to save the original image)
        if self.customLabel.originalPixmap:
            self.customLabel.originalPixmap.save('customCanvas.png')
        imgUpdated = cv2.imread('customCanvas.png')
        self.seedObj.singlBranchBinaryImg = imgUpdated
        self.mainUi.save_results_to_csv()
        self.mainUi.show_analyzed_results()
        self.mainUi.update_result_img()
        self.close()
    
    # __________ TOOLS DEFINITION __________________________________________
    def use_eraser(self):
        print("Eraser clicked")
        self.pen_color_mask = QtGui.QColor('black')
        self.eraserActive = True
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = False
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = True

        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)
    
    def use_breakPoint(self):
        print("Breakpoint clicked")
        self.eraserActive = False
        self.breakPointActive = True
        self.penHypActive = False
        self.penRootActive = False
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = True
        self.customLabel.eraserActive = False

        print(f"Initial hyperCotyl_length_pixels , radicle_length_pixels : {self.seedObj.hyperCotyl_length_cm}, {self.seedObj.radicle_length_cm}")
      
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnClickedStylesheet)

    def use_pen_hyp(self):
        print("Pen use_pen_hyp clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = True
        self.penRootActive = False
        self.customLabel.penHypActive = True
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = False

        self.btnDrawHyp.setStyleSheet(self.btnClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)

    def use_pen_root(self):
        print("Pen use_pen_root clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = True
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = True
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = False
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)

    def display_mask(self):
        cv2.imshow('mask_skeleton', self.seedObj.singlBranchBinaryImg)
        cv2.waitKey(1)

    def checkRadio(self):
        if self.radioBtnNormalSeed.isChecked():
            print("radio NormalSeed is checked")
            self.seedObj.seed_health = SeedHealth.NORMAL_SEED
        elif self.radioBtnAbnormalSeed.isChecked():
            print("radio Abnormal is checked")
            self.seedObj.seed_health = SeedHealth.ABNORMAL_SEED
        elif self.radioBtnDeadSeed.isChecked():
            print('radio Dead Seed is checked')
            self.seedObj.seed_health = SeedHealth.DEAD_SEED

        self.mainUi.summarize_results()

    def setColorPixmap(self):
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask_seededitor = QtGui.QPixmap.fromImage(imMask)

    def setSeedObj(self, seedObj):
        self.seedObj = seedObj
        self.update_values()
        self.imgH, self.imgW = self.seedObj.singlBranchBinaryImg.shape[:2]
        print(self.imgH, self.imgW)

        # Instead of hardcoding geometry, set the minimum size of the canvas (if desired)
        self.customLabel.setMinimumSize(self.imgW, self.imgH)

        self.customLabel.seedObj = seedObj
        # Remove hardcoded setGeometry; let the layout manage the size.
        self.customLabel.apply_cv2_image(self.seedObj.cropped_seed_color)

    def setSeedIndex(self, seedIndex):
        self.seedNo = seedIndex + 1
        print('set seed index no', self.seedNo)

    def update_values(self):
        self.label_seed_no.setText(str(self.seedNo))
        self.label_hypocotyl_length.setText(str(self.seedObj.hyperCotyl_length_cm))
        self.label_root_length.setText(str(self.seedObj.radicle_length_cm))
        self.label_total_length.setText(str(self.seedObj.total_length_cm))
        self.label_seed_health.setText(self.seedObj.seed_health)

        self.mainUi.mainProcessor.batchAnalyser.recalculate_all_metrics()
        self.mainUi.show_analyzed_results()
        self.mainUi.save_results_to_csv()
        self.mainUi.update_result_img()

    def closeEvent(self, event):
        print("Window is being closed...")
        self.save_changes()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.save_changes()
