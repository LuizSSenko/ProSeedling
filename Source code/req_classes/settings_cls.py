# settings_cls.py
import json
import os
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from utils_pyqt5 import showdialog

# Helper function to safely convert input text using a given conversion function.
def safe_convert(text, conv_func, default):
    # Replace comma with dot to handle locales with comma as decimal separator.
    text = text.replace(",", ".")
    try:
        return conv_func(text)
    except Exception:
        showdialog(f"Invalid input '{text}'. Using default value {default}.")
        return default

# Default settings dictionary used when no valid settings file exists.
DEFAULT_SETTINGS = {
    "dead_seed_max_length": 80,
    "abnormal_seed_max_length": 130,
    "normal_seed_max_length": 150,
    "thresh_avg_max_radicle_thickness": 13,
    "user_given_seedling_length": 200,
    "no_of_segments_each_skeleton": 15,
    "ph": 0.10,
    "pr": 0.90,
    "weights_factor_uniformity_Pu": 0.70,
    "weights_factor_growth_Pc": 0.30,
    # Other parameters (e.g. HSV) remain unchanged here.
}

class GlobalSettings(QtWidgets.QWidget):
    def __init__(self, mainUi):
        super().__init__()
        # Load UI from converted .ui file.
        from UI_files.settings_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.mainUi = mainUi

        # Mapping of settings keys to a tuple: (widget, conversion function, default value)
        self.fields = {
            "dead_seed_max_length": (self.ui.lineEdit_deadSeedL, float, 80),
            "abnormal_seed_max_length": (self.ui.lineEdit_abnormal_seedL, float, 130),
            "normal_seed_max_length": (self.ui.lineEdit_normal_seedL, float, 150),
            "thresh_avg_max_radicle_thickness": (self.ui.lineEdit_avg_rad_length, int, 13),
            "user_given_seedling_length": (self.ui.lineEdit_avg_seed_length, float, 200),
            "no_of_segments_each_skeleton": (self.ui.spinBox_n_seg, int, 15),
            "ph": (self.ui.doubleSpinBox_ph, float, 0.10),
            "pr": (self.ui.doubleSpinBox_pr, float, 0.90),
            "weights_factor_uniformity_Pu": (self.ui.doubleSpinBox_pu, float, 0.70),
            "weights_factor_growth_Pc": (self.ui.doubleSpinBox_pc, float, 0.30),
        }

        # Connect buttons to their methods.
        self.ui.btn_apply.clicked.connect(self.apply_inputs)
        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_import.clicked.connect(self.import_settings)
        self.ui.btn_export.clicked.connect(self.export_settings)
        self.ui.btn_restore_defaults.clicked.connect(self.restore_defaults)
        
        # Load settings from file (or create defaults if needed) and update UI.
        self.load_settings_from_file()
        self.set_stored_values()

    def load_settings_from_file(self):
        """Loads the settings JSON file. If the file is missing or corrupted,
        warns the user and writes the default settings to file."""
        settings_file = self.mainUi.settings_json_file_path
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as f:
                    self.mainUi.dict_settings = json.load(f)
            except Exception as e:
                showdialog(f"Error reading settings file: {e}. Restoring default settings.")
                self.mainUi.dict_settings = DEFAULT_SETTINGS.copy()
                self.mainUi.save_settings_to_file()
        else:
            self.mainUi.dict_settings = DEFAULT_SETTINGS.copy()
            self.mainUi.save_settings_to_file()

    def set_stored_values(self):
        """Populates the UI fields with values from the settings dictionary."""
        for key, (widget, conv_func, default) in self.fields.items():
            value = self.mainUi.dict_settings.get(key, default)
            # Assume that QLineEdit widgets use setText while spin boxes use setValue.
            if hasattr(widget, "setText"):
                widget.setText(str(value))
            elif hasattr(widget, "setValue"):
                widget.setValue(value)

    def restore_defaults(self):
        """Restores default values to the UI and updates the settings file.
        If a default settings file exists, it is used; otherwise, hardcoded defaults are used."""
        from proj_settings import load_default_settings, MainSettings
        import os
        default_settings_path = os.path.join(MainSettings.settings_dir, "default_settings.json")
        defaults = load_default_settings()

        # Warn user if the default settings file does not exist.
        if not os.path.exists(default_settings_path):
            showdialog("Default settings file not found. Using hardcoded default values.")
        
        # Update UI fields using the defaults.
        for key, (widget, conv_func, default) in self.fields.items():
            value = defaults.get(key, default)
            if hasattr(widget, "setText"):
                widget.setText(str(value))
            elif hasattr(widget, "setValue"):
                widget.setValue(value)

        # Update the main settings dictionary.
        self.mainUi.dict_settings.update({
            key: defaults.get(key, default) for key, (_, _, default) in self.fields.items()
        })
        self.mainUi.save_settings_to_file()
        showdialog("Settings restored to default values for this window.")

    def apply_inputs(self):
        """Reads values from UI widgets, validates them, updates the main settings,
        saves the settings file, and refreshes the main UI."""
        for key, (widget, conv_func, default) in self.fields.items():
            # For QLineEdit widgets use text(), for spin boxes use value()
            if hasattr(widget, "text"):
                text_val = widget.text().strip()
                # Use the safe conversion helper function.
                value = safe_convert(text_val, conv_func, default)
            elif hasattr(widget, "value"):
                value = widget.value()
            else:
                value = default

            self.mainUi.dict_settings[key] = value

        self.mainUi.save_settings_to_file()
        showdialog("Settings saved successfully!")
        self.mainUi.read_settings()
        self.mainUi.mainProcessor.dict_settings = self.mainUi.dict_settings
        self.mainUi.process_img_and_display_results()
        self.close()

    def import_settings(self):
        """Imports settings from a user-selected JSON file."""
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Settings File", "", "JSON Files (*.json)"
        )
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    self.mainUi.dict_settings = json.load(f)
                self.set_stored_values()
                showdialog("Settings imported successfully!")
            except Exception as e:
                showdialog(f"Error importing settings: {e}")
        else:
            showdialog("Please select a valid settings file.")

    def export_settings(self):
        """Exports the current settings to a user-selected JSON file."""
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Settings", "", "JSON Files (*.json)", options=options
        )
        if filePath:
            if not filePath.endswith(".json"):
                filePath += ".json"
            try:
                with open(filePath, "w+") as f:
                    json.dump(self.mainUi.dict_settings, f, indent=4)
                showdialog("Settings exported successfully!")
            except Exception as e:
                showdialog(f"Error exporting settings: {e}")
        else:
            showdialog("Please select a file name to export settings.")
