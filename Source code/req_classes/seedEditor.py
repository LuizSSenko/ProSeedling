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
from PyQt5.QtWidgets import  QWidget, QLabel
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog, show_cv2_img_on_label_obj
from utils import *
from req_classes.contour_processor import Seed
from proj_settings import SeedHealth
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication

class CanvasLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.text = "Custom Canvas"
        self.background_color = QColor(0, 255, 0)
        self.x = 50
        self.y = 30
        self.w = 301
        self.h = 781
        self.seedEditor = None
        self.setGeometry(self.x,self.y,self.w,self.h)
        self.imgW = 0
        self.imgH = 0
        self.margin_x = 0
        self.margin_y = 0
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = False

        self.canvasMask = None
        self.last_x, self.last_y = None, None
        self.pen_draw_color = [0,255,0]
        self.pen_thickness= 2
        self.pen_thickness_eraser = 20
        self.pen_color_mask = QtGui.QColor('black')
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.updated_img = None

    def apply_cv2_image(self, imgcv2):
        self.imgH, self.imgW = imgcv2.shape[:2]
        rgb_image_ = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
        # cv2.imshow('cv2.image', imgcv2)
        # cv2.waitKey(1)
        PIL_image = Image.fromarray(rgb_image_.copy()).convert('RGB')
        imMask = ImageQt(PIL_image).copy()
        self.canvasMask = QtGui.QPixmap.fromImage(imMask)
        # PIL_image.show('pil image')
        self.setPixmap(self.canvasMask)

   
    
    def reset_img(self):
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask_seededitor= QtGui.QPixmap.fromImage(imMask)
        self.setPixmap(self.canvasMask_seededitor)


    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print('pressed', ev.localPos())
        self.last_x = int((ev.x()) / self.w * self.imgW) 
        self.last_y = int((ev.y()) / self.h * self.imgH)
        return super().mousePressEvent(ev)


    

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        # print("ev", a0.x(), a0.y())
        
        if self.last_x is None:
            self.last_x = int((a0.x()) / self.w * self.imgW)
            self.last_y = int((a0.y()) / self.h * self.imgH)
                      
            return # ignore the first frame


        self.drawX = int((a0.x()) / self.w * self.imgW)
        self.drawY = int((a0.y()) / self.h * self.imgH)
        
        

        if self.breakPointActive:
            ## find closest point on contour 
            # QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
            ## Reload pixmap
            # Load skeletonized mask for editing
            # rgb_image = cv2.cvtColor(self.seedObj.skeltonized, cv2.COLOR_BGR2RGB)
            rgb_image = cv2.cvtColor(self.seedObj.singlBranchBinaryImg, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.canvasMask= QtGui.QPixmap.fromImage(imMask)
            self.setPixmap(QPixmap.fromImage(ImageQt(imgPilMask)))
            painter = QtGui.QPainter(self.canvasMask)
            
            # SET PEN
            p = painter.pen()

            closest_point_cnt = find_closest_point(contour=self.seedObj.sorted_point_list, point = (self.drawY, self.drawX))
            self.pen_color_mask = QtGui.QColor('blue')
            print('setting pen to blue')
            p.setWidth(20)
            p.setColor(self.pen_color_mask)
            painter.setPen(p)
            qPoint = QPoint(closest_point_cnt[1], closest_point_cnt[0])
            painter.drawPoint(qPoint)
            painter.end()
            self.setPixmap(self.canvasMask)
            self.update()
            
            self.seedObj.reassign_points(new_break_point=closest_point_cnt)
            
            self.last_x = self.drawX
            self.last_y = self.drawY

            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.canvasMask_seededitor= QtGui.QPixmap.fromImage(imMask)
            self.setPixmap(self.canvasMask_seededitor)

        if self.eraserActive:

            # painter = QtGui.QPainter(self.canvasMask)
           
            # p = painter.pen()
            # self.pen_color_mask = QtGui.QColor('black')
            # # print('setting pen to black')
            
            # p.setWidth(self.pen_thickness_eraser)
            # p.setColor(self.pen_color_mask)
            # painter.setPen(p)
            
            closest_points_list_ =  find_closest_n_points(contour=self.seedObj.sorted_point_list, point = (self.drawY, self.drawX), no_points=self.pen_thickness_eraser)
            # closest_point_cnt = find_closest_point(contour=self.seedObj.sorted_point_list, point = (self.drawY, self.drawX))
            closest_point_cnt = closest_points_list_[0]

            
            # qPoint = QPoint(closest_point_cnt[1], closest_point_cnt[0])
            # painter.drawPoint(qPoint)
            # painter.end()
            self.setPixmap(self.canvasMask)
            self.update()
            self.seedEditor.update()
            
            # print("erasing points function")          
            for pnt in closest_points_list_:
                # painter.drawLine(self.last_x, self.last_y, self.drawX, self.drawY)
                dist_pnt = find_dist(pnt, (self.drawY, self.drawX))
                if dist_pnt < 10:
                    self.seedObj.erase_points(point=pnt)

            
            # update origin
            self.last_x = self.drawX
            self.last_y = self.drawY

            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.canvasMask_seededitor= QtGui.QPixmap.fromImage(imMask)
            self.setPixmap(self.canvasMask_seededitor)


        if self.penHypActive or self.penRootActive:
           
            painter = QtGui.QPainter(self.canvasMask)

            blnkImg = np.zeros((self.h, self.w), np.uint8)
            cv2.line(blnkImg, (self.last_x, self.last_y),(self.drawX, self.drawY), 255,thickness=1)
            # cv2.imshow('line',blnkImg)
            # cv2.waitKey(1)
            points = np.argwhere(blnkImg==255)
            # print('white _ points', points)
            points = list(points)
            # print('white _ points list', points)
            points = [list(point) for point in points]

            if self.penHypActive:
                self.seedObj.add_hypercotyl_points(points)
            elif self.penRootActive:
                self.seedObj.add_root_points(points)

            painter.end()
            self.setPixmap(self.canvasMask)

            self.last_x = self.drawX
            self.last_y = self.drawY
            self.update()
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.canvasMask_seededitor= QtGui.QPixmap.fromImage(imMask)
            self.setPixmap(self.canvasMask_seededitor)

        self.seedEditor.update_values()

        QApplication.restoreOverrideCursor()
        return super().mouseMoveEvent(a0)


class SeedEditor(QWidget):
    def __init__(self, mainUi):
        super().__init__()
        loadUi(r'UI_files\seed_editor.ui', self)
        self.mainUi = mainUi
        self.setWindowIconText("Seed ")
        
        #_________ SEED RELATED ____________________________________________
        self.seedObj: Seed = None
        self.seedNo = 0
        
        
        #_________ CHECK BUTTONS ____________________________________________
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
        
        #_________ EDITION BUTTONS____________________________________________
        self.btnEraser.clicked.connect(self.use_eraser)
        self.btnPoint.clicked.connect(self.use_breakPoint)
        self.btnDrawHyp.clicked.connect(self.use_pen_hyp)
        self.btnEraser.setShortcut('e')
        self.btnPoint.setShortcut('b')
        self.btnDrawHyp.setShortcut('1')
        self.btnDrawRoot.setShortcut('2')
        
        self.eraserActive = False
        self.breakPointActive = False
        
        
        #_________ CANVAS RELATED ____________________________________________
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

        self.customLabel = CanvasLabel(self)
        self.customLabel.setObjectName("img_label_mask")
        self.customLabel.seedEditor = self

        #_________ BUTTONS STYLESHEET ____________________________________________

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
        self.customLabel.canvasMask.save('customCanvas.png')
        imgUpdated = cv2.imread('customCanvas.png')
        self.seedObj.singlBranchBinaryImg = imgUpdated
        self.mainUi.save_results_to_csv()
        self.mainUi.show_analyzed_results()
        self.mainUi.update_result_img()
        # cv2.imshow('updatedQIMG',self.seedObj.skeltonized)
        # cv2.imshow('self.customLabel.updated_img',self.customLabel.updated_img)
        # cv2.waitKey(1)
        self.close()
    
    #_________ TOOLS DEFINITION _______________________________________________
    def use_eraser(self):
        print("Eraser clicked")
        self.pen_color_mask = QtGui.QColor('black')
        self.eraserActive=True
        self.breakPointActive=False
        self.penHypActive = False
        self.penRootActive = False
        self.customLabel.penHypActive=False
        self.customLabel.penRootActive=False
        self.customLabel.breakPointActive=False
        self.customLabel.eraserActive=True

        # self.label_img_seed_mask.setVisible(True)

        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)
    
    def use_breakPoint(self):
        print("Breakpoint clicked")
        # self.pen_color_mask = QtGui.QColor('black')
        self.eraserActive=False
        self.breakPointActive=True
        self.penHypActive = False
        self.penRootActive = False
        self.customLabel.penHypActive=False
        self.customLabel.penRootActive=False
        self.customLabel.breakPointActive=True
        self.customLabel.eraserActive=False

        # self.label_img_seed_mask.setVisible(True)
        print(f"Initial hyperCotyl_length_pixels , radicle_length_pixels : {self.seedObj.hyperCotyl_length_cm}, {self.seedObj.radicle_length_cm}")
      
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnClickedStylesheet)

    def use_pen_hyp(self):
        print("Pen use_pen_hyp clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive=False
        self.breakPointActive=False
        self.penHypActive = True
        self.penRootActive = False
        self.customLabel.penHypActive=True
        self.customLabel.penRootActive=False
        self.customLabel.breakPointActive=False
        self.customLabel.eraserActive=False

        # self.label_img_seed_mask.setVisible(False)

        self.btnDrawHyp.setStyleSheet(self.btnClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)

    
    
    def use_pen_root(self):
        print("Pen use_pen_hyp clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive=False
        self.breakPointActive=False
        self.penHypActive = False
        self.penRootActive = True
        self.customLabel.penHypActive=False
        self.customLabel.penRootActive=True
        self.customLabel.breakPointActive=False
        self.customLabel.eraserActive=False
        # self.label_img_seed_mask.setVisible(False)
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)


    def display_mask(self):
        cv2.imshow('mask_skeleton', self.seedObj.singlBranchBinaryImg)
        # cv2.imshow('mask_head', self.seedObj.cropped_head_binary)
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
        # self.update_values()

    def setColorPixmap(self):
        # Load skeletonized mask for editing
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask_seededitor= QtGui.QPixmap.fromImage(imMask)

    def setSeedObj(self,seedObj):
        self.seedObj = seedObj

        self.update_values()

        self.imgH, self.imgW = self.seedObj.singlBranchBinaryImg.shape[:2]
        print(self.imgH, self.imgW)

        if not self.imgH < 781 :
            self.customLabel.h = 780
        if not self.imgW < 301:
            self.customLabel.w = 300
        
        # self.label_paint_h = self.imgH
        # self.label_paint_w = self.imgW 
        if self.imgH > self.maxImgHt:
            print("Image height is greater than max possible height.......")
        else: 
            self.customLabel.w = self.imgW
            self.customLabel.h = self.imgH

        self.customLabel.seedObj = seedObj
        self.customLabel.setGeometry(self.customLabel.x, self.customLabel.y, self.customLabel.w, self.customLabel.h)
        # self.customLabel.apply_cv2_image(self.seedObj.singlBranchBinaryImg)
        self.customLabel.apply_cv2_image(self.seedObj.cropped_seed_color)




    def setSeedIndex(self, seedIndex):
        self.seedNo = seedIndex + 1
        print('set seed index no', self.seedNo)

        # self.setColorPixmap()

    def update_values(self):
        
        self.label_seed_no.setText(str(self.seedNo))
        self.label_hypocotyl_length.setText(str(self.seedObj.hyperCotyl_length_cm))
        self.label_root_length.setText(str(self.seedObj.radicle_length_cm))

        self.label_total_length.setText(str(self.seedObj.total_length_cm))
        self.label_seed_health.setText(self.seedObj.seed_health)


        ###
        self.mainUi.mainProcessor.batchAnalyser.recalculate_all_metrics()
        self.mainUi.show_analyzed_results()
        self.mainUi.save_results_to_csv()
        self.mainUi.update_result_img()
    def closeEvent(self, event):
        # Perform your desired actions here
        print("Window is being closed...")
        self.save_changes()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # Check if the pressed key is the Escape key
            self.save_changes()