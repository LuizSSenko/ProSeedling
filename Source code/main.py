# main.py
import sys, os, json, csv, cv2, numpy as np, traceback
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QLocale
from UI_files.mainWindow_ui import Ui_MainWindow
from main_processor import Main_Processor
from req_classes.settings_cls import GlobalSettings
from req_classes.setHSVclass import SetHSV
from class_photo_viewer import PhotoViewer
from req_classes.seedEditor import SeedEditor
import utils_pyqt5 as ut
from utils import check_if_point_lies_xywh_box
from req_classes.dataConcat import dataConcat 

# MainWindow class combines the UI design from Ui_MainWindow with application logic.
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Build the UI using the imported UI design.
        self.initUIComponents()  # Set up additional UI elements.
        self.initVariables()       # Initialize instance variables (settings, paths, parameters, etc.)
        self.createMenus()         # Create menu items (File, Configuration, etc.)
        self.connectSignals()      # Connect UI signals (button clicks, table clicks, etc.) to handlers.
        self.loadSettings()        # Load persistent settings from JSON file.
        
        # Instantiate processing objects
        self.dataConcat = dataConcat()  # object that joins the CSVs
        self.mainProcessor = Main_Processor(mainUi=self)
        # Pass HSV values and settings dictionary to the processor.
        self.mainProcessor.hsv_values_seed = self.hsv_values_seed
        self.mainProcessor.hsv_values_seed_heads = self.hsv_values_seed_heads
        self.mainProcessor.dict_settings = self.dict_settings
        
        # Create and configure the image viewer widget.
        self.viewer = PhotoViewer(self)
        # Replace the placeholder widget with the viewer widget
        self.leftLayout.replaceWidget(self.imageArea, self.viewer)
        self.imageArea.hide() # Hide the placeholder widget 
        self.viewer.mainUiObj = self # Allow the viewer to access MainWindow methods.
        
        # Create a persistent SeedEditor window for editing seed data.
        self.seedEditorObj = SeedEditor(mainUi=self)
        

    def initUIComponents(self):
        """Initialize additional UI components and set initial status message."""
        self.statusbar.showMessage("Ready")
        

    def initVariables(self):
        """
        Initialize all necessary variables:
        - Input folder and image paths.
        - Default processing parameters (e.g., segmentation count, thresholds).
        - Settings and output directories.
        """
        self.input_folder_path = None
        self.imagePaths = []
        self.currentImgIndex = 0
        self.currentResultImg = None
        
        # Input parameters for seed analysis.
        self.n_segments_each_skeleton = 15
        self.thres_avg_max_radicle_thickness = 13
        self.dead_seed_max_length_r_h = 2.0
        self.abnormal_seed_max_length_r_h = 3.25
        self.normal_seed_max_length_r_h = 3.75
        self.user_given_seedling_length = 12.5
        self.weights_factor_growth_Pc = 0.7
        self.weights_factor_uniformity_Pu = 0.3
        self.p_h = 0.10
        self.p_r = 0.90
        self.pixel_per_cm = 72
        # HSV values for detecting seed head and seed body.
        self.hsv_values_seed_heads = [0, 127, 0, 255, 0, 34]
        self.hsv_values_seed = [0, 179, 0, 255, 0, 162]
        
        # Metadata inputs.
        self.cultivatorName = ""
        self.analystsName = ""
        self.batchNo = 0
        self.n_seeds = 20
        self.data_each_seed = []
        self.germination_percent = 0
        
        # Directories for project files.
        self.PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
        self.settings_dir = os.path.join(self.PROJECT_DIR, "settings")
        self.output_dir = os.path.join(self.PROJECT_DIR, "output")
        self.output_results_dir = os.path.join(self.output_dir, "results")
        self.output_images_dir = os.path.join(self.output_dir, "processed_images")
        self.settings_json_file_path = os.path.join(self.settings_dir, "current_settings.json")
        
        # Build settings dictionary to pass to other modules
        self.dict_settings = {
            "dead_seed_max_length": self.dead_seed_max_length_r_h,
            "abnormal_seed_max_length": self.abnormal_seed_max_length_r_h,
            "normal_seed_max_length": self.normal_seed_max_length_r_h,
            "no_of_segments_each_skeleton": self.n_segments_each_skeleton,
            "weights_factor_growth_Pc": self.weights_factor_growth_Pc,
            "weights_factor_uniformity_Pu": self.weights_factor_uniformity_Pu,
            "ph": self.p_h,
            "pr": self.p_r,
            "thresh_avg_max_radicle_thickness": self.thres_avg_max_radicle_thickness,
            "user_given_seedling_length": self.user_given_seedling_length,
            "hmin_head": self.hsv_values_seed_heads[0],
            "hmax_head": self.hsv_values_seed_heads[1],
            "smin_head": self.hsv_values_seed_heads[2],
            "smax_head": self.hsv_values_seed_heads[3],
            "vmin_head": self.hsv_values_seed_heads[4],
            "vmax_head": self.hsv_values_seed_heads[5],
            "hmin_body": self.hsv_values_seed[0],
            "hmax_body": self.hsv_values_seed[1],
            "smin_body": self.hsv_values_seed[2],
            "smax_body": self.hsv_values_seed[3],
            "vmin_body": self.hsv_values_seed[4],
            "vmax_body": self.hsv_values_seed[5],
            "factor_pixel_to_cm": self.pixel_per_cm
        }
    

    def createMenus(self):
        """Configure the menu bar with File and Configuration menus and add actions."""

        self.menubar.setStyleSheet("""
        QMenuBar {
            background-color: rgb(255, 255, 255);
            font: 63 10pt 'Segoe UI';
        }
        QMenuBar::item {
            background-color: transparent;
        }
        QMenuBar::item:selected {
            background-color: rgb(235, 235, 235);
        }
    """)
        # Create File menu actions.
        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction("Open Folder", self.browse_input_folder)
        fileMenu.addAction("Inputs", self.give_inputs)
        
        # Create Configuration menu actions.
        configMenu = self.menuBar().addMenu("Configuration")
        configMenu.addAction("Change Settings", self.change_settings)
        configMenu.addAction("Set HSV Values", self.set_hsv_values)
        configMenu.addAction("Set Calibration", self.set_pixel_cm_values)
    

    def connectSignals(self):
        """Connect UI signals (button clicks, table clicks) to their corresponding handlers."""
        self.btnNext.clicked.connect(self.loadNextImg)
        self.btnPrev.clicked.connect(self.loadPrevImg)
        self.resultsTable.clicked.connect(self.get_selected_row)
    

    def loadSettings(self):
        """
        Load settings from the JSON file.
        If the file exists, update internal parameters; otherwise, save the current settings.
        """
        if os.path.exists(self.settings_json_file_path):
            with open(self.settings_json_file_path, "r") as f:
                self.dict_settings = json.load(f)
            self.n_segments_each_skeleton = self.dict_settings["no_of_segments_each_skeleton"]
            self.thres_avg_max_radicle_thickness = self.dict_settings["thresh_avg_max_radicle_thickness"]
            self.dead_seed_max_length_r_h = self.dict_settings["dead_seed_max_length"]
            self.abnormal_seed_max_length_r_h = self.dict_settings["abnormal_seed_max_length"]
            self.normal_seed_max_length_r_h = self.dict_settings["normal_seed_max_length"]
            self.user_given_seedling_length = self.dict_settings["user_given_seedling_length"]
            self.weights_factor_growth_Pc = self.dict_settings["weights_factor_growth_Pc"]
            self.weights_factor_uniformity_Pu = self.dict_settings["weights_factor_uniformity_Pu"]
            self.p_h = self.dict_settings["ph"]
            self.p_r = self.dict_settings["pr"]
        else:
            self.save_settings_to_file()
    

    def check_if_all_valid_inputs(self):
        """
        Verify that all critical input parameters are valid (non-negative).
        Returns True if all inputs are valid.
        """
        inputs = [
            self.dead_seed_max_length_r_h,
            self.abnormal_seed_max_length_r_h,
            self.normal_seed_max_length_r_h,
            self.n_segments_each_skeleton,
            self.weights_factor_growth_Pc,
            self.weights_factor_uniformity_Pu
        ]
        return all(x >= 0 for x in inputs)

    
    def restore_default_settings(self):
        """
        Reset all parameters to their default values.
        Update the settings dictionary, save it to file, show a dialog and re-process the image.
        """
        self.n_segments_each_skeleton = 15
        self.thres_avg_max_radicle_thickness = 13
        self.dead_seed_max_length_r_h = 2.0
        self.abnormal_seed_max_length_r_h = 3.25
        self.normal_seed_max_length_r_h = 3.75
        self.user_given_seedling_length = 12.5
        self.weights_factor_growth_Pc = 0.7
        self.weights_factor_uniformity_Pu = 0.3
        self.p_h = 0.10
        self.p_r = 0.90
        self.pixel_per_cm = 40
        self.hsv_values_seed_heads = [0, 127, 0, 255, 0, 34]
        self.hsv_values_seed = [0, 179, 0, 255, 0, 162]
        self.dict_settings = {
            "dead_seed_max_length": self.dead_seed_max_length_r_h,
            "abnormal_seed_max_length": self.abnormal_seed_max_length_r_h,
            "normal_seed_max_length": self.normal_seed_max_length_r_h,
            "no_of_segments_each_skeleton": self.n_segments_each_skeleton,
            "weights_factor_growth_Pc": self.weights_factor_growth_Pc,
            "weights_factor_uniformity_Pu": self.weights_factor_uniformity_Pu,
            "thresh_avg_max_radicle_thickness": self.thres_avg_max_radicle_thickness,
            "user_given_seedling_length": self.user_given_seedling_length,
            "hmin_head": self.hsv_values_seed_heads[0],
            "hmax_head": self.hsv_values_seed_heads[1],
            "smin_head": self.hsv_values_seed_heads[2],
            "smax_head": self.hsv_values_seed_heads[3],
            "vmin_head": self.hsv_values_seed_heads[4],
            "vmax_head": self.hsv_values_seed_heads[5],
            "hmin_body": self.hsv_values_seed[0],
            "hmax_body": self.hsv_values_seed[1],
            "smin_body": self.hsv_values_seed[2],
            "smax_body": self.hsv_values_seed[3],
            "vmin_body": self.hsv_values_seed[4],
            "vmax_body": self.hsv_values_seed[5],
            "factor_pixel_to_cm": self.pixel_per_cm,
            "ph": self.p_h,
            "pr": self.p_r
        }
        self.save_settings_to_file()
        ut.showdialog("Default settings restored successfully!")
        self.process_img_and_display_results()
    

    def set_pixel_cm_values(self):
        """
        Launch the calibration settings window to update the conversion factor (pixels per cm).
        After the window is closed, re-process the image to apply new calibration.
        """
        from req_classes.calibration_settings import CalibrationSettings
        self.window = CalibrationSettings(mainUi=self)
        self.window.show()
        self.process_img_and_display_results()
    

    def change_settings(self):
        """Launch the GlobalSettings window to change advanced parameters."""

        self.window = GlobalSettings(self)
        self.window.show()
    

    def read_settings(self):
        """Read settings from file and update local variables and HSV values."""
        if os.path.exists(self.settings_json_file_path):
            with open(self.settings_json_file_path, "r") as f:
                self.dict_settings = json.load(f)
            self.n_segments_each_skeleton = self.dict_settings["no_of_segments_each_skeleton"]
            self.thres_avg_max_radicle_thickness = self.dict_settings["thresh_avg_max_radicle_thickness"]
            self.dead_seed_max_length_r_h = self.dict_settings["dead_seed_max_length"]
            self.abnormal_seed_max_length_r_h = self.dict_settings["abnormal_seed_max_length"]
            self.normal_seed_max_length_r_h = self.dict_settings["normal_seed_max_length"]
            self.user_given_seedling_length = self.dict_settings["user_given_seedling_length"]
            self.weights_factor_growth_Pc = self.dict_settings["weights_factor_growth_Pc"]
            self.weights_factor_uniformity_Pu = self.dict_settings["weights_factor_uniformity_Pu"]
            self.p_h = self.dict_settings["ph"]
            self.p_r = self.dict_settings["pr"]
        self.apply_new_hsv_values()
    

    def apply_new_hsv_values(self):
        """Update the HSV values in the processor based on current settings."""
        self.mainProcessor.hsv_values_seed = self.hsv_values_seed
        self.mainProcessor.hsv_values_seed_heads = self.hsv_values_seed_heads
    

    def set_hsv_values(self):
        """Launch the SetHSV dialog for adjusting HSV thresholds."""
        self.window = SetHSV(parent=self, mainUi=self)
        self.window.show()
    

    def give_inputs(self):
        """
        Open an input dialog to get cultivar, analyst, batch number, and number of seeds.
        Update the info labels on the right-side of the UI.
        """
        inputDialog = QtWidgets.QInputDialog()
        inputDialog.setStyleSheet("font: 63 10pt \"Segoe UI Semibold\";")
        self.cultivatorName, ok1 = inputDialog.getText(self, "Inputs", "Enter cultivar name:")
        self.analystsName, ok2 = inputDialog.getText(self, "Inputs", "Enter Analyst name:")
        self.batchNo, ok3 = inputDialog.getInt(self, "Inputs", "Enter Lot no:")
        self.n_seeds, ok4 = inputDialog.getInt(self, "Inputs", "Enter no of seeds:", value=20, min=1)
        if self.n_seeds < 1:
            ut.showdialog("No of seeds cannot be less than 1. Please select proper value.")
            self.n_seeds, ok4 = inputDialog.getInt(self, "Inputs", "Enter no of seeds:")
        if ok1 and ok2 and ok3:
            # Update metadata labels with new input values.
            self.label_cult_name_info.setText(str(self.cultivatorName))
            self.label_analys_name_info.setText(str(self.analystsName))
            self.label_batchNo_info.setText(str(self.batchNo))
            self.label_n_plants_info.setText(str(self.n_seeds))
    

    def save_settings_to_file(self):
        """
        Save the current settings dictionary to a JSON file.
        Remove any existing settings file before writing a new one.
        """
        try:
            if os.path.exists(self.settings_json_file_path):
                os.remove(self.settings_json_file_path)
        except Exception as e:
            print(e)
        with open(self.settings_json_file_path, "w+") as f:
            json.dump(self.dict_settings, f)
    

    def create_dirs(self, dir_list):
        """Create directories from a list if they don't already exist."""
        for dir_path in dir_list:
            os.makedirs(dir_path, exist_ok=True)
    

    def browse_input_folder(self):
        """
        Open a folder selection dialog.
        If an input folder was previously chosen, automatically concatenate CSV files from the previous session.
        Load images from the new folder and initialize output directories.
        """
        if self.input_folder_path is not None:
            # Executa dataConcat antes de mudar a pasta
            self.auto_concat_csv(self.output_results_dir)

        # Abre o diálogo para escolher nova pasta
        self.input_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", "")
        self.load_images()
        
        if self.imagePaths:
            self.give_inputs()
            self.output_dir = os.path.join(self.input_folder_path, str(self.batchNo))
            self.output_results_dir = os.path.join(self.output_dir, "results")
            self.output_images_dir = os.path.join(self.output_dir, "processed_images")

            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(self.output_results_dir, exist_ok=True)
            os.makedirs(self.output_images_dir, exist_ok=True)

            self.setCursor(Qt.CursorShape.BusyCursor)
            self.process_img_and_display_results()
            self.label_img_no.setText(f"1 / {len(self.imagePaths)}")
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            ut.showdialog("This folder does not contain image files. Please choose another one.")

        return self.input_folder_path


    def load_images(self):
        """Load image file paths from the input folder, filtering by common image extensions."""
        imgExtensions = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
        if self.input_folder_path:
            files = os.listdir(self.input_folder_path)
            self.imagePaths = [os.path.join(self.input_folder_path, f) for f in files if f.split(".")[-1].lower() in imgExtensions]
    

    def showImg(self):
        """Display the current image in the PhotoViewer and update the file name label."""
        if self.imagePaths:
            imgPath = self.imagePaths[self.currentImgIndex]
            self.viewer.setPhoto(QtGui.QPixmap(imgPath))
            self.label_img_no.setText(f"{self.currentImgIndex + 1} / {len(self.imagePaths)}")
        self.set_file_name()
    

    def set_file_name(self):
        """Update the label with the base file name of the current image."""
        if self.imagePaths:
            self.label_fileName_info.setText(os.path.basename(self.imagePaths[self.currentImgIndex]))
    

    def showResultImg(self, imgNumpy):
        """
        Convert a NumPy image array to a QPixmap and display it in the PhotoViewer.
        This is used to show processed images.
        """
        h, w, ch = imgNumpy.shape
        bytesPerLine = 3 * w
        qImg = QtGui.QImage(imgNumpy.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.pixmap = QtGui.QPixmap.fromImage(qImg)
        self.viewer.setPhoto(self.pixmap)


    def check_position_in_seed(self, mouse_loc):
        """
        Convert the mouse click coordinates (on the scaled image) to the actual image coordinates.
        Check if the click lies within any seed bounding box; if so, open the SeedEditor for that seed.
        """
        # print('position in seed', mouse_loc)
        x_mouse, y_mouse = mouse_loc
        # Get the size of the viewer widget.
        windowH, windowW = self.viewer.height(), self.viewer.width()
        if self.currentResultImg is not None:
            imgSize = self.currentResultImg.shape
            # print("imgSize", imgSize)
            hImg, wImg = imgSize[:2]
            if self.viewer.factor is not None:
                scaleFactor = self.viewer.factor
                resizedImgH, resizedImgW = int(hImg*scaleFactor), int(wImg * scaleFactor)
            
                diff_x = windowW - resizedImgW
                diff_y = windowH - resizedImgH
                dx_half = diff_x / 2
                dy_half = diff_y / 2
                
                # Adjust mouse position relative to the image.
                x_in_img = x_mouse - dx_half
                y_in_img = y_mouse - dy_half
            
                transformedMousePos = [int(x_in_img/scaleFactor), int(y_in_img/scaleFactor)]
                print("transformedMousePos", transformedMousePos)

            # Loop through each detected seed and check if the mouse position is inside its bounding box.
            for i, seedobj in enumerate(self.mainProcessor.SeedObjList):
                # print(i, seedobj.xywh)
                result_in = check_if_point_lies_xywh_box(transformedMousePos, seedobj.xywh)
                if result_in:
                    
                    self.seedEditorObj.setSeedObj(seedobj)
                    seedIndex= i +1
                    self.seedEditorObj.setSeedIndex(seedIndex)
                    # print('selected seed crop size',seedobj.xywh)

                    self.highlight_seed_with_rect(seedobj)
                    self.resultsTable.selectRow(i)
    
                    self.show_seed_editor_window()
                    break


    def highlight_seed_with_rect(self, seedobj):
        """Draw a blue rectangle around the seed region on the processed image and display it."""
        x1, y1, w, h = seedobj.xywh
        colorImgCopy = self.currentResultImg.copy()
        cv2.rectangle(colorImgCopy, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 15)
        colorImgCopy = cv2.cvtColor(colorImgCopy, cv2.COLOR_BGR2RGB)
        self.showResultImg(colorImgCopy)
    

    def auto_concat_csv(self, folder_path):
        try:
            # Set the folder path for the data concatenation object
            self.dataConcat.folder_path = folder_path
            # Define the output CSV file path using the given folder and the output filename property
            self.dataConcat.output_csv = os.path.join(folder_path, self.dataConcat.output_filename)
            # Process the CSV files: this function typically reads and concatenates multiple CSV files in the folder
            processed_files = self.dataConcat.process()
            # If there are any processed files, display a success dialog with the count of processed files
            if processed_files and processed_files > 0:
                ut.showdialog(f'"{processed_files}" CSV files have been saved and concatenated successfully!')
        except Exception as e:
            # If any error occurs during processing, display an error dialog with the error message
            ut.showdialog(f"Error concatenating CSV files: {e}")


    def get_selected_row(self):
        """
        When a row in the results table is selected,
        open the SeedEditor window for the corresponding seed.
        """
        index = self.resultsTable.selectedIndexes()[0]
        seedObjSelected = self.mainProcessor.SeedObjList[index.row()]
        self.seedEditorObj.setSeedObj(seedObjSelected)
        self.seedEditorObj.setSeedIndex(index.row())
        self.highlight_seed_with_rect(seedObjSelected)
        self.resultsTable.selectRow(index.row())
        self.show_seed_editor_window()


    def show_seed_editor_window(self):
        """Bring the persistent SeedEditor window to focus."""
        try:
            self.seedEditorObj.show()
            self.seedEditorObj.setFocus()
        except Exception as e:
            print(traceback.format_exc())


    def summarize_results(self):
        """
        Recalculate all metrics using the batch analyzer and update the UI to show analyzed results.
        """
        if self.batchAnalyzerObj:
            self.batchAnalyzerObj.recalculate_all_metrics()
            self.show_analyzed_results()
    

    def update_result_img(self):
        """
        Update the processed image by drawing the current seed regions (after editing) on top of the original image.
        """
        imgPath = self.imagePaths[self.currentImgIndex]
        updatedResImg = cv2.imread(imgPath)
        if self.mainProcessor.SeedObjList:
            for seedObj in self.mainProcessor.SeedObjList:
                x1, y1, w, h = seedObj.xywh
                updatedResImg[y1:y1+h+1, x1:x1+w+1] = seedObj.cropped_seed_color
        updatedResImg = cv2.cvtColor(updatedResImg, cv2.COLOR_BGR2RGB)
        self.showResultImg(updatedResImg)
    

    def save_results_to_csv(self):
        """
        Save the seed analysis results to a CSV file.
        The CSV includes per-seed measurements, summary data, and metadata.
        Also updates the UI table with the seed measurements.
        """
        # Get the current file's base name and remove its extension
        current_file_name = os.path.basename(self.imagePaths[self.currentImgIndex])
        print("saving results to", current_file_name)
        ext = current_file_name.split(".")[-1]
        fileNameWoExt = current_file_name[:-(len(ext) + 1)]
        outCsvFileName = fileNameWoExt + ".csv"
        output_result_csv_path = os.path.join(self.output_results_dir, outCsvFileName)
        
        # Format the date as dd/mm/YYYY (to match your sample, e.g. "15/09/2023")
        datetime_now = datetime.today()
        date_str = datetime_now.strftime("%d/%m/%Y")
        
        # Remove existing CSV file if it exists.
        try:
            os.remove(output_result_csv_path)
        except Exception:
            pass

        # Define header columns for seed data, summary, and metadata.
        header = [
            "Seedling", "Hypocotyl", "Root", "Total length", "Hypocotyl/root ratio",
            "Vigor Index", "Growth", "Uniformity", "Germination", "Average length", "Standard deviation",
            "Normal Seedlings", "Abnormal Seedlings", "Non germinated seeds",
            "Cultivar", "Lot number", "Number of seeds", "Analyst", "Date"
        ]

        # Summary data from batch analysis.
        summary_data = [
            self.seed_vigor_index, self.growth, self.uniformity, self.germination_percent,
            self.avg_length, self.std_deviation, self.count_germinated_seeds,
            self.count_abnormal_seeds, self.count_dead_seeds
        ]
        # Metadata for the analysis.
        metadata = [self.cultivatorName, self.batchNo, self.n_seeds, self.analystsName, date_str]

        try:
            with open(output_result_csv_path, 'w', newline="") as f:
                writer = csv.writer(f)
                
                # First line: specify the separator for Excel or other programs
                writer.writerow(["SEP=,"])
                
                # Write the single header row
                writer.writerow(header)

                # Write data rows
                # For the first seed, include summary and metadata
                # For subsequent seeds, write empty strings for those columns so they don't repeat
                for i, seed_row in enumerate(self.data_each_seed):
                    if i == 0:
                        # First row gets seed data + summary data + metadata
                        writer.writerow(seed_row + summary_data + metadata)
                    else:
                        # Subsequent rows: seed data + empty columns for summary & metadata
                        writer.writerow(seed_row + [""] * (len(summary_data) + len(metadata)))
                        
            # Update the results table in the UI.
            self.model = TableModel(self.data_each_seed)
            self.model.columns = ["Seedling", "hypocotyl", "root", "Total length", "hypocotyl/root ratio"]
            self.resultsTable.setModel(self.model)
            self.resultsTable.resizeColumnsToContents()
        except PermissionError:
            ut.showdialog('Please close the opened .csv file !! Changes would not be saved...')


    def show_analyzed_results(self):
        """
        Update the UI with analyzed results from the batch analyzer:
        - Update seed measurement list.
        - Update metrics (growth, standard deviation, uniformity, vigor, etc.).
        - Refresh the results table.
        """
        if self.batchAnalyzerObj:
            self.data_each_seed = []
            for i, seedObj in enumerate(self.batchAnalyzerObj.seedObjList):
                self.data_each_seed.append([i+1, seedObj.hyperCotyl_length_cm, seedObj.radicle_length_cm, seedObj.total_length_cm, seedObj.ratio_h_root])
            self.std_deviation = self.batchAnalyzerObj.std_deviation
            self.growth = int(self.batchAnalyzerObj.growth)
            self.penalization = round(self.batchAnalyzerObj.penalization, 2)
            self.uniformity = int(self.batchAnalyzerObj.uniformity)
            self.seed_vigor_index = int(self.batchAnalyzerObj.seed_vigor_index)
            self.count_abnormal_seeds = self.batchAnalyzerObj.abnormal_seed_count
            self.count_dead_seeds = self.batchAnalyzerObj.dead_seed_count
            self.count_germinated_seeds = self.batchAnalyzerObj.germinated_seed_count
            self.germination_percent = round(self.batchAnalyzerObj.germination_percent, 2)
            # Update metric labels on the UI.
            self.label_growth_value.setText(str(self.growth))
            self.label_sd_value.setText(str(self.std_deviation))
            self.label_uniformity_value.setText(str(self.uniformity))
            self.label_vigor_value.setText(str(self.seed_vigor_index))
            self.label_germ_value.setText(f"{self.germination_percent} %")
            self.label_avg_hypocotyl_value.setText(str(self.batchAnalyzerObj.avg_hypocotyl_length_cm))
            self.label_avg_root_value.setText(str(self.batchAnalyzerObj.avg_root_length_cm))
            self.label_avg_total_value.setText(str(self.batchAnalyzerObj.avg_total_length_cm))
            self.model = TableModel(self.data_each_seed)
            self.model.columns = ["Seedling", "Hypocotyl", "Root", "Total", "Hypocotyl/root ratio"]
            self.resultsTable.setModel(self.model)
    

    def process_img_and_display_results(self):
        """
        Process the current image by passing it to the main processor.
        Save the processed image, update metrics, and refresh the UI display.
        """
        if self.imagePaths:
            self.setCursor(Qt.CursorShape.BusyCursor)
            if self.check_if_all_valid_inputs():
                imgPath = self.imagePaths[self.currentImgIndex]
                self.list_hypercotyl_radicle_lengths, colorImg, self.batchAnalyzerObj = self.mainProcessor.process_main(imgPath)
                self.std_deviation = self.batchAnalyzerObj.std_deviation
                self.growth = round(self.batchAnalyzerObj.growth, 2)
                os.makedirs(self.output_images_dir, exist_ok=True)
                output_img_path = os.path.join(self.output_images_dir, os.path.basename(imgPath))
                cv2.imwrite(output_img_path, colorImg)
                self.currentResultImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2RGB)
                self.showResultImg(self.currentResultImg)
            total_lengths = 0
            list_total_lengths = []
            self.data_each_seed = []
            # Aggregate per-seed data for summary and CSV output.
            for i, seedObj in enumerate(self.batchAnalyzerObj.seedObjList):
                self.data_each_seed.append([i+1, seedObj.hyperCotyl_length_cm, seedObj.radicle_length_cm, seedObj.total_length_cm, seedObj.ratio_h_root])
                total_lengths += seedObj.total_length_pixels
                list_total_lengths.append(seedObj.total_length_pixels)
            self.avg_length = total_lengths / self.n_seeds
            self.show_analyzed_results()
            self.save_results_to_csv()
            self.setCursor(Qt.CursorShape.ArrowCursor)
    

    def loadNextImg(self):
        """Load and process the next image in the list, if available."""
        if self.currentImgIndex < len(self.imagePaths) - 1:
            self.currentImgIndex += 1
            self.showImg()
            self.process_img_and_display_results()
    

    def loadPrevImg(self):
        """Load and process the previous image in the list, if available."""
        if self.currentImgIndex > 0:
            self.currentImgIndex -= 1
            self.showImg()
            self.process_img_and_display_results()


    def closeEvent(self, event):
        """Executa dataConcat antes de fechar o programa."""
        try:
            if self.input_folder_path and self.imagePaths:
                self.auto_concat_csv(self.output_results_dir)
                print("Concatenate CSV files before output.")
        except Exception as e:
            print(f"Error concatenating CSVs before closing: {e}")
        event.accept()


# A custom TableModel to show seed measurements in the UI table.
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = []   # Column headers to be set later.
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    
    def rowCount(self, index):
        return len(self._data)
    
    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]
        return super().headerData(section, orientation, role)
    


        
if __name__ == "__main__":
    # Entry point of the application.
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("ProSeedling Software")
    window.setWindowIcon(QtGui.QIcon("resources/icon.png"))
    window.show()
    sys.exit(app.exec_())
