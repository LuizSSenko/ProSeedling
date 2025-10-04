# calibration_settings.py

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
# Import necessary libraries and modules.
import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog  # Helper function for showing dialogs.
import utils_pyqt5 as ut          # Import utility functions from utils_pyqt5.
from proj_settings import load_default_settings  # Function to load default settings.

def get_pixel_to_cm(img, checkerboard_size=(28,20)):
    """
    Given an image containing a checkerboard, calculates the average size of one square (in pixels)
    and returns the conversion factor: number of pixels that correspond to 1 cm.

    Parameters:
        img: The input image (expected to contain a checkerboard pattern).
        checkerboard_size: Tuple representing the number of inner corners per a chessboard row and column.
                           Defaults to (28, 20).

    Returns:
        pixel_per_cm: Integer representing the number of pixels per 1 cm, if successful.
                      Returns None if the checkerboard corners cannot be detected.
    """
    # Convert the input image to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Try to find chessboard corners in the grayscale image.
    ret, corners = cv2.findChessboardCorners(
        gray, checkerboard_size,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    )
    if ret:
        square_size_pixels = []
        # Calculate horizontal distances between adjacent corners.
        for i in range(checkerboard_size[1]-1):
            for j in range(checkerboard_size[0]-1):
                p1 = corners[j + i * checkerboard_size[0]]
                p2 = corners[j + i * checkerboard_size[0] + 1]
                distance = np.sqrt(((p1 - p2) ** 2).sum())
                square_size_pixels.append(distance)
        # Calculate vertical distances between adjacent corners.
        for i in range(checkerboard_size[0]):
            for j in range(checkerboard_size[1]-1):
                p1 = corners[i + j * checkerboard_size[0]]
                p2 = corners[i + (j+1) * checkerboard_size[0]]
                distance = np.sqrt(((p1 - p2) ** 2).sum())
                square_size_pixels.append(distance)
        # Compute the average square size in pixels.
        average_square_size_pixels = np.mean(square_size_pixels)
        # The conversion factor is the average size (rounded) which represents 1 cm.
        pixel_per_cm = np.round(average_square_size_pixels)
        print(f"Conversion factor: {pixel_per_cm} pixels = 1 cm")
        return int(pixel_per_cm)
    else:
        print("Could not find chessboard corners")
        return None

# Import the UI definition for the calibration dialog.
from UI_files.calibration_ui import Ui_Form

class CalibrationSettings(QtWidgets.QDialog, Ui_Form):
    def __init__(self, mainUi, parent=None):
        """
        Initialize the CalibrationSettings dialog.

        Parameters:
            mainUi: Reference to the main UI object which holds settings and methods for saving and processing images.
            parent: Parent widget, if any.
        """
        super().__init__(parent)
        self.mainUi = mainUi
        # Set up the UI elements as defined in the UI file.
        self.setupUi(self)  # Widgets are directly assigned to self.

        # Connect the "Restore" button to restore default settings.
        self.btn_restore.clicked.connect(self.restore_defaults)

        # Update the current settings by reading from settings.json.
        self.mainUi.read_settings()
        # Pre-fill the QLineEdit with the current conversion factor if available.
        self.lineEdit_pixel_cm.setText(str(self.mainUi.dict_settings.get('factor_pixel_to_cm', '')))

        # Connect buttons to their respective methods.
        self.btn_load_calib_img.clicked.connect(self.load_calib_image)
        self.btnSave.clicked.connect(self.saveSetting)

        # Define the checkerboard size used in calibration.
        self.checkerboard_size = (28,20)

    def load_calib_image(self):
        """
        Open a file dialog for the user to select a calibration image.
        Once selected, calculate the pixel-to-cm conversion factor using the checkerboard,
        update settings, and trigger reprocessing of the image.
        """
        # Open a file dialog to select an image file.
        filepath, _ = QFileDialog.getOpenFileName(self, 'Select Calibration Image', '', "Image Files (*.jpg *.png *.bmp)")
        if not filepath or not os.path.exists(filepath):
            ut.showdialog("Please select a file")
        else:
            try:
                # Read the image using OpenCV.
                img = cv2.imread(filepath)
                if img is None:
                    raise ValueError("File is not a valid image.")
                
                # Calculate the conversion factor (pixels per cm) from the image.
                result_pixel_per_cm = get_pixel_to_cm(img, self.checkerboard_size)
                if result_pixel_per_cm is not None:
                    # Update the main UI's settings with the new conversion factor.
                    self.mainUi.pixel_per_cm = result_pixel_per_cm
                    self.mainUi.dict_settings['factor_pixel_to_cm'] = result_pixel_per_cm
                    self.lineEdit_pixel_cm.setText(str(result_pixel_per_cm))
                    
                    ut.showdialog(f"Calibration done! \n {result_pixel_per_cm} pixels = 1 cm.")
                    # Save updated settings to file.
                    self.mainUi.save_settings_to_file()
                    # Process the image again and display the new results.
                    self.mainUi.process_img_and_display_results()
                else:
                    ut.showdialog("Calibration not done! \n Image could not be processed.")
            except Exception as e:
                ut.showdialog(f"Error: {str(e)}")
            self.close()

    def restore_defaults(self):
        """
        Restore default settings by loading default values and updating the conversion factor field.
        """
        # Load default settings.
        defaults = load_default_settings()
        # Retrieve the default conversion factor (if available) or use a fallback value.
        default_value = defaults.get('factor_pixel_to_cm', 40)
        self.lineEdit_pixel_cm.setText(str(default_value))

    def saveSetting(self):
        """
        Save the conversion factor entered manually by the user.
        The value must be a positive integer.
        """
        # Check if the input is a positive integer.
        if len(self.lineEdit_pixel_cm.text()) > 0 and self.lineEdit_pixel_cm.text().isnumeric():
            pixel_value = int(self.lineEdit_pixel_cm.text())
            # Update main UI settings with the new conversion factor.
            self.mainUi.pixel_per_cm = pixel_value
            self.mainUi.dict_settings['factor_pixel_to_cm'] = pixel_value
            print("Saving settings:", self.mainUi.dict_settings)
            # Save settings to file.
            self.mainUi.save_settings_to_file()
            ut.showdialog(f"Saved! \n {pixel_value} pixels = 1 cm.\nSaved in settings.")
            # Process the image again and update the display.
            self.mainUi.process_img_and_display_results()
        else:
            ut.showdialog("Please enter a positive integer value.")
        self.close()
