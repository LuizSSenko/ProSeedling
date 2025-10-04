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
import os
import json

class MainSettings:
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    settings_dir = os.path.join(PROJECT_DIR, "settings")
    output_dir = os.path.join(PROJECT_DIR, 'output')
    settings_json_file_path =  os.path.join(settings_dir, "current_settings.json")

class SeedHealth:
    NORMAL_SEED = 'NORMAL_SEED'
    ABNORMAL_SEED = 'ABNORMAL_SEED'
    DEAD_SEED = 'DEAD_SEED'

def load_default_settings():
    """
    Attempts to load default values ​​from the default_settings.json file
    located in the settings folder. If the file does not exist or occurs
    any error, returns a dictionary with hardcoded default values.
    """
    default_settings_path = os.path.join(MainSettings.settings_dir, "default_settings.json")
    hardcoded_defaults = {
        "dead_seed_max_length": 80,
        "abnormal_seed_max_length": 130,
        "normal_seed_max_length": 150,
        "no_of_segments_each_skeleton": 15,
        "weights_factor_growth_Pc": 0.3,
        "weights_factor_uniformity_Pu": 0.7,
        "thresh_avg_max_radicle_thickness": 13,
        "user_given_seedling_length": 200,
        "hmin_head": 0,
        "hmax_head": 127,
        "smin_head": 0,
        "smax_head": 255,
        "vmin_head": 0,
        "vmax_head": 191,
        "hmin_body": 0,
        "hmax_body": 179,
        "smin_body": 0,
        "smax_body": 255,
        "vmin_body": 0,
        "vmax_body": 162,
        "factor_pixel_to_cm": 40,
        "ph": 0.1,
        "pr": 0.9
    }
    if os.path.exists(default_settings_path):
        try:
            with open(default_settings_path, "r") as f:
                loaded_defaults = json.load(f)
            # Se algum parâmetro estiver faltando, preenche com o valor hardcoded
            for key, value in hardcoded_defaults.items():
                if key not in loaded_defaults:
                    loaded_defaults[key] = value
            return loaded_defaults
        except Exception as e:
            print("Error loading default_settings.json:", e)
            return hardcoded_defaults
    else:
        return hardcoded_defaults
