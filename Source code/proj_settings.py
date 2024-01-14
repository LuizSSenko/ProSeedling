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



class MainSettings:
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    settings_dir = os.path.join(PROJECT_DIR, "settings")
    output_dir = os.path.join(PROJECT_DIR, 'output')
    settings_json_file_path =  os.path.join(settings_dir, "settings.json")
    # settings_file_path = os.path.join(settings_dir, "settings.csv")
    # settings_hsv_path = os.path.join(settings_dir, "settings_hsv.csv")

class SeedHealth:
    NORMAL_SEED = 'NORMAL_SEED'
    ABNORMAL_SEED = 'ABNORMAL_SEED'
    DEAD_SEED = 'DEAD_SEED'