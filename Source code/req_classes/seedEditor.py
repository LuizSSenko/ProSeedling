# seedEditor.py is a class that allows the user to edit the seed's skeletonized image 
# by adding or removing points. It uses PyQt5 for the GUI, OpenCV and PIL for image processing,
# and custom modules for seed-related processing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog, show_cv2_img_on_label_obj
from utils import *
from req_classes.contour_processor import Seed
from proj_settings import SeedHealth
from PIL import Image
try:
    from PIL.ImageQt import ImageQt
except ImportError:
    # For newer versions of Pillow
    from PIL import ImageQt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import cv2
import numpy as np
from UI_files.seed_editor_ui import Ui_Form 

# Custom QLabel subclass to display and interact with the seed image canvas.
class CanvasLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set a minimum size for the label to ensure it's large enough for display.
        self.setMinimumSize(300, 300)
        # We no longer use setScaledContents(True) to maintain aspect ratio manually.
        
        # Store the original pixmap image
        self.originalPixmap = None
        # These attributes will be updated during painting to handle scaling and centering.
        self.scaledPixmap = None
        self.offset_x = 0
        self.offset_y = 0

        # Reference back to the SeedEditor dialog that created this canvas.
        self.seedEditor = None
        self.imgW = 0  # original image width
        self.imgH = 0  # original image height
        
        # Flags for different editing tools.
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = False

        # Store the last known image coordinates from mouse events.
        self.last_x, self.last_y = None, None

        # Drawing parameters for pen and eraser.
        self.pen_draw_color = [0, 255, 0]
        self.pen_thickness = 2
        self.pen_thickness_eraser = 20
        self.pen_color_mask = QtGui.QColor('black')

        # Change cursor to cross for better precision when drawing.
        self.setCursor(Qt.CursorShape.CrossCursor)

        # Updated image after modifications.
        self.updated_img = None

    def apply_cv2_image(self, imgcv2):
        """
        Convert a CV2 image to a QPixmap and update the canvas.
        """
        # Save image dimensions.
        self.imgH, self.imgW = imgcv2.shape[:2]
        # Convert the image from BGR (OpenCV) to RGB (PIL).
        rgb_image = cv2.cvtColor(imgcv2, cv2.COLOR_BGR2RGB)
        # Create a PIL image from the numpy array.
        PIL_image = Image.fromarray(rgb_image.copy()).convert('RGB')
        # Convert PIL image to a Qt image.
        imMask = ImageQt(PIL_image).copy()
        # Create a QPixmap from the Qt image.
        self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
        # Trigger a repaint to update the display.
        self.update() 

    def reset_img(self):
        """
        Reset the canvas image using the seed's cropped seed color image.
        """
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
        self.update()

    def paintEvent(self, event):
        """
        Overridden paint event to scale and center the pixmap within the label.
        """
        painter = QPainter(self)
        if self.originalPixmap:
            # Scale the original pixmap to fit the label while keeping aspect ratio.
            self.scaledPixmap = self.originalPixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Compute offsets to center the pixmap in the label.
            self.offset_x = (self.width() - self.scaledPixmap.width()) // 2
            self.offset_y = (self.height() - self.scaledPixmap.height()) // 2
            # Draw the pixmap at the computed offset.
            painter.drawPixmap(self.offset_x, self.offset_y, self.scaledPixmap)
        else:
            # If there is no pixmap, use the default paint event.
            super().paintEvent(event)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Capture the mouse press event and map the click coordinates from widget space 
        to image space.
        """
        # Calculate the position relative to the scaled pixmap.
        x = ev.x() - self.offset_x
        y = ev.y() - self.offset_y
        # Check if the click is within the bounds of the scaled pixmap.
        if self.scaledPixmap and 0 <= x <= self.scaledPixmap.width() and 0 <= y <= self.scaledPixmap.height():
            # Map widget coordinates to original image coordinates.
            self.last_x = int(x / self.scaledPixmap.width() * self.imgW)
            self.last_y = int(y / self.scaledPixmap.height() * self.imgH)
        else:
            # Reset last coordinates if click is outside.
            self.last_x, self.last_y = None, None
        return super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Handle mouse move events to update drawing on the canvas based on the selected tool.
        """
        # Calculate the relative x, y position on the scaled pixmap.
        x = ev.x() - self.offset_x
        y = ev.y() - self.offset_y
        if self.scaledPixmap and 0 <= x <= self.scaledPixmap.width() and 0 <= y <= self.scaledPixmap.height():
            # Map widget coordinates to original image coordinates.
            drawX = int(x / self.scaledPixmap.width() * self.imgW)
            drawY = int(y / self.scaledPixmap.height() * self.imgH)
        else:
            return super().mouseMoveEvent(ev)

        # Ensure we have a valid starting point for drawing.
        if self.last_x is None:
            self.last_x, self.last_y = drawX, drawY
            return super().mouseMoveEvent(ev)

        # Process drawing based on the active tool.
        if self.breakPointActive:
            # When break point tool is active, update the canvas to mark a breakpoint.
            rgb_image = cv2.cvtColor(self.seedObj.singlBranchBinaryImg, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image).convert('RGB')        
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()  # Force repaint so offsets update

            # Start drawing on the original pixmap.
            painter = QPainter(self.originalPixmap)
            p = painter.pen()
            # Find the closest point on the contour to the mouse pointer.
            closest_point_cnt = find_closest_point(contour=self.seedObj.sorted_point_list, point=(drawY, drawX))
            self.pen_color_mask = QtGui.QColor('blue')
            p.setWidth(20)
            p.setColor(self.pen_color_mask)
            painter.setPen(p)
            # Draw the point using QPainter.
            qPoint = QPoint(closest_point_cnt[1], closest_point_cnt[0])
            painter.drawPoint(qPoint)
            painter.end()
            # Update the seed object with the new break point.
            self.seedObj.reassign_points(new_break_point=closest_point_cnt)
            self.last_x, self.last_y = drawX, drawY

            # Refresh the canvas image.
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()

        elif self.eraserActive:
            # When eraser is active, identify nearby points to erase.
            closest_points_list_ = find_closest_n_points(
                contour=self.seedObj.sorted_point_list,
                point=(drawY, drawX),
                no_points=self.pen_thickness_eraser
            )
            self.update()
            self.seedEditor.update()
            # Erase points that are close enough.
            for pnt in closest_points_list_:
                if find_dist(pnt, (drawY, drawX)) < 10:
                    self.seedObj.erase_points(point=pnt)
            self.last_x, self.last_y = drawX, drawY
            # Refresh the canvas image after erasing.
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()

        elif self.penHypActive or self.penRootActive:
            # When drawing with pen tools, create a temporary blank image.
            blank = np.zeros((self.imgH, self.imgW), np.uint8)
            cv2.line(blank, (self.last_x, self.last_y), (drawX, drawY), 255, thickness=1)
            # Extract the drawn points from the blank image.
            points = np.argwhere(blank == 255).tolist()
            if self.penHypActive:
                # Add points as part of the hypocotyl.
                self.seedObj.add_hypercotyl_points(points)
            elif self.penRootActive:
                # Add points as part of the root.
                self.seedObj.add_root_points(points)
            self.last_x, self.last_y = drawX, drawY
            # Refresh the canvas image.
            rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)
            imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')
            imMask = ImageQt(imgPilMask).copy()
            self.originalPixmap = QtGui.QPixmap.fromImage(imMask)
            self.update()

        # Update the seed editor values after processing the mouse event.
        self.seedEditor.update_values()
        QApplication.restoreOverrideCursor()
        return super().mouseMoveEvent(ev)

# Main dialog for editing seeds.
class SeedEditor(QtWidgets.QDialog, Ui_Form):
    def __init__(self, mainUi, parent=None):
        super().__init__(parent)
        # Store reference to the main UI.
        self.mainUi = mainUi
        # Setup UI from the designer file.
        self.setupUi()  # This method comes from Ui_Form.
        self.setWindowIconText("Seed ")
        # Ensure the dialog can receive keyboard focus.
        self.setFocusPolicy(Qt.StrongFocus)
        
        # SEED RELATED
        self.seedObj: Seed = None   # Current seed object to be edited.
        self.seedNo = 0 # Index of the seed object in the list.
        
        # CHECK BUTTONS
        self.btngroup1 = QtWidgets.QButtonGroup() 
        self.btngroup1.addButton(self.radioBtnNormalSeed)
        self.btngroup1.addButton(self.radioBtnAbnormalSeed)
        self.btngroup1.addButton(self.radioBtnDeadSeed)
        self.radioBtnNormalSeed.toggle()
        self.radioBtnNormalSeed.toggled.connect(self.checkRadio)
        self.radioBtnAbnormalSeed.toggled.connect(self.checkRadio)
        self.radioBtnDeadSeed.toggled.connect(self.checkRadio)
        # Shortcuts for quick selection.
        self.radioBtnNormalSeed.setShortcut('n')
        self.radioBtnAbnormalSeed.setShortcut('a')
        self.radioBtnDeadSeed.setShortcut('d')
        
        # EDITION BUTTONS: Connect buttons to their respective functions.
        self.btnEraser.clicked.connect(self.use_eraser)
        self.btnPoint.clicked.connect(self.use_breakPoint)
        self.btnDrawHyp.clicked.connect(self.use_pen_hyp)
        # Set shortcuts for editing tools.
        self.btnEraser.setShortcut('e')
        self.btnPoint.setShortcut('b')
        self.btnDrawHyp.setShortcut('1')
        self.btnDrawRoot.setShortcut('2')
        self.eraserActive = False
        self.breakPointActive = False
        
        # CANVAS RELATED: Initialize canvas parameters.
        self.btnDrawRoot.clicked.connect(self.use_pen_root)
        self.canvasMask_seededitor = None
        self.last_x, self.last_y = None, None
        self.pen_draw_color = [0, 255, 0]
        self.pen_thickness = 2
        self.pen_color_mask = QtGui.QColor('white')
        self.imgH = 0
        self.imgW = 0
        # Offsets and maximum image height for display.
        self.delta_x = 390 
        self.delta_y = 30
        self.maxImgHt = 800

        # Instead of directly adding the canvas, wrap it in a scroll area for better navigation.
        self.imgLabel.hide()  # Hide the placeholder image label.
        self.scrollArea = QtWidgets.QScrollArea(self.leftWidget)
        self.scrollArea.setWidgetResizable(True)
        # Create the custom canvas label and assign it to the scroll area.
        self.customLabel = CanvasLabel(self.scrollArea)
        self.customLabel.setObjectName("img_label_mask")
        self.customLabel.seedEditor = self
        self.scrollArea.setWidget(self.customLabel)
        self.leftLayout.addWidget(self.scrollArea)

        # BUTTONS STYLESHEET: Define styles for active and inactive buttons.
        self.btnClickedStylesheet = '''background-color:rgba(216, 229, 253,50);
                        font: 63 10pt "Segoe UI Semibold";
                        color: rgb(32, 24, 255);
                        border-radius:4;'''
        self.btnNotClickedStylesheet = '''background-color:rgba(216, 229, 253,255);
                        font: 63 10pt "Segoe UI Semibold";
                        color: rgb(32, 24, 255);
                        border-radius:4;'''

    def save_changes(self, close_window=True):
        """
        Save the current canvas state to an image file and update the seed object.
        Then, update the main UI and optionally close the window.
        """
        print("saving changes")
        if self.customLabel.originalPixmap:
            # Save the pixmap to a file.
            self.customLabel.originalPixmap.save('customCanvas.png')
        # Read the updated image using OpenCV.
        imgUpdated = cv2.imread('customCanvas.png')
        self.seedObj.singlBranchBinaryImg = imgUpdated
        # Save and update results in the main UI.
        self.mainUi.save_results_to_csv()
        self.mainUi.show_analyzed_results()
        self.mainUi.update_result_img()
        if close_window:
            self.close()
    
    # __________ TOOLS DEFINITION __________________________________________
    def use_eraser(self):
        """
        Activate the eraser tool.
        """
        print("Eraser clicked")
        self.pen_color_mask = QtGui.QColor('black')
        self.eraserActive = True
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = False
        # Update tool flags on the canvas.
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = True

        # Update button styles to reflect active tool.
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)
    
    def use_breakPoint(self):
        """
        Activate the breakpoint tool for marking specific points on the seed skeleton.
        """
        print("Breakpoint clicked")
        self.eraserActive = False
        self.breakPointActive = True
        self.penHypActive = False
        self.penRootActive = False
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = True
        self.customLabel.eraserActive = False

        # Log the initial seed measurements.
        print(f"Initial hyperCotyl_length_pixels , radicle_length_pixels : {self.seedObj.hyperCotyl_length_cm}, {self.seedObj.radicle_length_cm}")

        # Update button styles.
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnClickedStylesheet)

    def use_pen_hyp(self):
        """
        Activate the pen tool for drawing on the hypocotyl.
        """
        print("Pen use_pen_hyp clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = True
        self.penRootActive = False
        # Update tool flags on the canvas.
        self.customLabel.penHypActive = True
        self.customLabel.penRootActive = False
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = False

        # Update button styles.
        self.btnDrawHyp.setStyleSheet(self.btnClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)

    def use_pen_root(self):
        """
        Activate the pen tool for drawing on the root.
        """
        print("Pen use_pen_root clicked")
        self.pen_color_mask = QtGui.QColor('white')
        self.eraserActive = False
        self.breakPointActive = False
        self.penHypActive = False
        self.penRootActive = True
        # Update tool flags on the canvas.
        self.customLabel.penHypActive = False
        self.customLabel.penRootActive = True
        self.customLabel.breakPointActive = False
        self.customLabel.eraserActive = False

        # Update button styles.
        self.btnDrawHyp.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnDrawRoot.setStyleSheet(self.btnClickedStylesheet)
        self.btnEraser.setStyleSheet(self.btnNotClickedStylesheet)
        self.btnPoint.setStyleSheet(self.btnNotClickedStylesheet)

    def display_mask(self):
        """
        Display the current skeletonized mask in a separate OpenCV window.
        """
        cv2.imshow('mask_skeleton', self.seedObj.singlBranchBinaryImg)
        cv2.waitKey(1)

    def checkRadio(self):
        """
        Handle changes in seed health radio buttons.
        Update the seed object's health status and refresh the main UI.
        """
        if self.radioBtnNormalSeed.isChecked():
            print("Radio NormalSeed is checked")
            self.seedObj.seed_health = SeedHealth.NORMAL_SEED
        elif self.radioBtnAbnormalSeed.isChecked():
            print("Radio Abnormal is checked")
            self.seedObj.seed_health = SeedHealth.ABNORMAL_SEED
        elif self.radioBtnDeadSeed.isChecked():
            print("Radio Dead Seed is checked")
            self.seedObj.seed_health = SeedHealth.DEAD_SEED

        # Update main UI with the new seed health information.
        self.mainUi.summarize_results()
        self.mainUi.save_results_to_csv()
        self.mainUi.update_result_img()

    def setColorPixmap(self):
        """
        Convert the seed's cropped color image to a QPixmap for display.
        """
        rgb_image = cv2.cvtColor(self.seedObj.cropped_seed_color, cv2.COLOR_BGR2RGB)        
        imgPilMask = Image.fromarray(rgb_image.copy()).convert('RGB')        
        imMask = ImageQt(imgPilMask).copy()
        self.canvasMask_seededitor = QtGui.QPixmap.fromImage(imMask)

    def setSeedObj(self, seedObj):
        """
        Set the current seed object for editing and update the UI.
        """
        self.seedObj = seedObj
        self.update_values()

        # Select the appropriate radio button based on seed health.
        if self.seedObj.seed_health == SeedHealth.NORMAL_SEED:
            self.radioBtnNormalSeed.setChecked(True)
        elif self.seedObj.seed_health == SeedHealth.ABNORMAL_SEED:
            self.radioBtnAbnormalSeed.setChecked(True)
        elif self.seedObj.seed_health == SeedHealth.DEAD_SEED:
            self.radioBtnDeadSeed.setChecked(True)

        # If a skeleton image exists, update the canvas.
        if self.seedObj.singlBranchBinaryImg is not None:
            self.imgH, self.imgW = self.seedObj.singlBranchBinaryImg.shape[:2]
            print(f"Skeletonized image: height={self.imgH}, width={self.imgW}")
            self.customLabel.setMinimumSize(self.imgW, self.imgH)
            self.customLabel.seedObj = seedObj
            self.customLabel.apply_cv2_image(self.seedObj.cropped_seed_color)
        else:
            # Display error message if the seed lacks a skeleton image.
            error_msg = "Seedling without skeleton, adjust the HSV values"
            print("Error: The seedling has no skeleton (singlBranchBinaryImg is None). " + error_msg)
            showdialog(error_msg)


    def setSeedIndex(self, seedIndex):
        """
        Update the seed number/index and log the change.
        """
        self.seedNo = seedIndex + 1
        print('set seed index no', self.seedNo)

    def update_values(self):
        """
        Refresh displayed seed metrics and update the main UI.
        """
        self.label_seed_no.setText(str(self.seedNo))
        self.label_hypocotyl_length.setText(str(self.seedObj.hyperCotyl_length_cm))
        self.label_root_length.setText(str(self.seedObj.radicle_length_cm))
        self.label_total_length.setText(str(self.seedObj.total_length_cm))
        self.label_seed_health.setText(self.seedObj.seed_health)

        # Recalculate all metrics and update the main UI.
        self.mainUi.mainProcessor.batchAnalyser.recalculate_all_metrics()
        self.mainUi.show_analyzed_results()
        self.mainUi.save_results_to_csv()
        self.mainUi.update_result_img()

    def closeEvent(self, event):
        """
        Overridden close event to save changes before the window closes.
        """
        print("Window is being closed...")
        self.save_changes()

    def keyPressEvent(self, event):
        """
        Handle key press events for shortcuts such as Escape, Left, and Right arrows.
        """
        if event.key() == Qt.Key_Escape:
            # Save and close when Escape is pressed.
            self.save_changes()  # close_window defaults to True.
        elif event.key() == Qt.Key_Right:
            print("Right key pressed")
            self.switch_to_next_seed()
        elif event.key() == Qt.Key_Left:
            print("Left key pressed")
            self.switch_to_previous_seed()


    def switch_to_next_seed(self):
        """
        Save changes and switch to the next seed in the list without closing the window.
        """
        # Save without closing the window, then switch seed.
        self.save_changes(close_window=False)
        current_index = self.seedNo - 1  # Convert seed number to 0-based index.
        if current_index < len(self.mainUi.mainProcessor.SeedObjList) - 1:
            next_seed = self.mainUi.mainProcessor.SeedObjList[current_index + 1]
            self.setSeedObj(next_seed)
            self.setSeedIndex(current_index + 1)


    def switch_to_previous_seed(self):
        """
        Save changes and switch to the previous seed in the list without closing the window.
        """
        # Save without closing the window, then switch seed.
        self.save_changes(close_window=False)
        current_index = self.seedNo - 1
        if current_index > 0:
            prev_seed = self.mainUi.mainProcessor.SeedObjList[current_index - 1]
            self.setSeedObj(prev_seed)
            self.setSeedIndex(current_index - 1)
    
    def showEvent(self, event):
        """
        Overridden show event to set focus on the dialog when it becomes visible.
        """
        super().showEvent(event)
        self.setFocus()

