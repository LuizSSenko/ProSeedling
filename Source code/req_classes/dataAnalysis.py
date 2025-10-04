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

# Import required modules and classes.
from .contour_processor import Seed
from proj_settings import MainSettings, SeedHealth
import json
import numpy as np
import traceback

# Get the path to the JSON settings file from the main settings.
settings_path = MainSettings.settings_json_file_path

class BatchAnalysisNew:
    def __init__(self, img_path, batchNumber, seedObjList:list[Seed]):
        """
        Initialize the BatchAnalysisNew instance.
        
        Parameters:
            img_path: Path to the image being analyzed.
            batchNumber: Identifier for the current batch.
            seedObjList: List of Seed objects representing individual seed analyses.
        """
        self.batchNumber = batchNumber
        self.dict_settings = None   # Will hold settings loaded from a JSON file.
        self.seedObjList = seedObjList

        # Initialize lists and counters for seed length metrics.
        self.list_total_seed_lengths = []

        # Counters for different seed classes.
        self.n_total_seeds_in_image = 0
        self.germinated_seed_count = 0
        self.dead_seed_count = 0
        self.abnormal_seed_count = 0

        # Metrics that will be calculated.
        self.growth = 0
        self.penalization = 0
        self.uniformity = 0
        self.seed_vigor_index = 0
        
        # Average lengths in different units.
        self.avg_total_length_settings = 0    # User-given average seedling length (in cm or pixels as defined by settings)
        self.avg_total_length_cm = 0          # Average total length in centimeters.
        self.avg_hypocotyl_length_cm = 0      # Average hypocotyl length in centimeters.
        self.avg_root_length_cm = 0           # Average root length in centimeters.

        self.avg_hypocotyl_length_pixels = 0  # Average hypocotyl length in pixels.
        self.avg_root_length_pixels = 0       # Average root length in pixels.
        self.std_deviation = 0                # Standard deviation of total seed lengths.
        self.germination_percent = 0          # Germination percentage.

        # Recalculate all metrics using the provided seed data.
        self.recalculate_all_metrics()


    def recalculate_all_metrics(self):
        """
        Load the settings and recalculate all metrics based on the seed data.
        This includes counts, averages, growth, penalization, uniformity,
        seed vigor index, and standard deviation.
        """
        settings_path = MainSettings.settings_json_file_path
        # Load user and system settings from a JSON file.
        with open(settings_path, 'r') as f:
            self.dict_settings = json.load(f)

        # Count the number of seeds per class.
        self.get_seed_class_count()
        # Calculate averages for various seed length measurements.
        self.calculate_averages()
        # Calculate the growth metric.
        self.calculate_growth_or_Crescimento()
        # Calculate penalization based on dead seed count.
        self.calc_penalization()
        # Calculate uniformity based on deviations in seed lengths.
        self.calculate_uniformity_or_Uniformidade()
        # Calculate the overall seed vigor index.
        self.calculate_seed_vigor_index()
        # Calculate standard deviation and germination percentage.
        self.calculate_std_deviation_and_other()

    def get_seed_class_count(self):
        """
        Count the number of seeds in each health category (dead, abnormal, normal)
        and compute the total number of seeds.
        """
        # Reset counts.
        self.dead_seed_count, self.abnormal_seed_count, self.germinated_seed_count = 0,0,0

        # Iterate through each seed object and update counts based on its health.
        for seedObj in self.seedObjList:
            if seedObj.seed_health == SeedHealth.DEAD_SEED:
                self.dead_seed_count+=1
            elif seedObj.seed_health == SeedHealth.ABNORMAL_SEED:
                self.abnormal_seed_count+=1
            elif seedObj.seed_health == SeedHealth.NORMAL_SEED:
                self.germinated_seed_count+=1

        # Debug print statements for counts.
        print("Dead seed count", self.dead_seed_count)
        print("Abnormal seed count", self.abnormal_seed_count)
        print("Normal seed count", self.germinated_seed_count)

        # Total seeds is the sum of all counts.
        self.n_total_seeds_in_image = self.dead_seed_count + self.abnormal_seed_count+self.germinated_seed_count


    def calc_penalization(self):
        """
        Calculate the penalization metric, which is based on the number of dead seeds.
        The formula applies a penalty proportional to the dead seed count.
        
        Returns:
            The calculated penalization value.
        """
        self.penalization = self.dead_seed_count *( 50 / self.n_total_seeds_in_image) # Correto!
        return self.penalization


    def calculate_averages(self):
        """
        Calculate average seed lengths (both in cm and pixels) for total, hypocotyl, and root lengths.
        Also retrieves the user-given average seedling length from settings.
        """

        # Initialize lists to collect individual seed measurements.
        # Measurements in centimeters.
        self.list_total_seed_lengths_cm = []
        self.list_hypocotyl_seed_lengths_cm = []
        self.list_root_lengths_cm = []
        # Measurements in pixels.
        self.list_total_seed_lengths_pixels = []
        self.list_hypocotyl_seed_lengths_pixels = []
        self.list_root_lengths_pixels = [] 

        # Iterate through each seed object to collect measurements.
        for seedObj in self.seedObjList:
            # Collect lengths in cm.
            self.list_total_seed_lengths_cm.append(seedObj.total_length_cm)
            self.list_hypocotyl_seed_lengths_cm.append(seedObj.hyperCotyl_length_cm)
            self.list_root_lengths_cm.append(seedObj.radicle_length_cm)
            # Collect lengths in pixels.
            self.list_total_seed_lengths_pixels.append(seedObj.total_length_pixels)
            self.list_hypocotyl_seed_lengths_pixels.append(seedObj.hyperCotyl_length_pixels)
            self.list_root_lengths_pixels.append(seedObj.radicle_length_pixels)

        # Calculate average total seed length in centimeters.
        self.avg_total_length_cm = np.round(np.sum(self.list_total_seed_lengths_cm) /  len(self.seedObjList), 2)
        # Calculate average total seed length in pixels.
        self.avg_total_length_pixels = np.round(np.sum(self.list_total_seed_lengths_pixels) /  len(self.seedObjList), 2)
        # Retrieve user-given average seedling length from settings.
        self.avg_total_length_Settings = self.dict_settings['user_given_seedling_length']
        try:
            # Calculate average hypocotyl and root lengths (in cm).
            self.avg_hypocotyl_length_cm = np.round(np.sum(self.list_hypocotyl_seed_lengths_cm) /  len(self.seedObjList),2)
            self.avg_root_length_cm = np.round(np.sum(self.list_root_lengths_cm) /  len(self.seedObjList), 2)
            # Calculate average hypocotyl and root lengths (in pixels).
            self.avg_hypocotyl_length_pixels = np.round(np.sum(self.list_hypocotyl_seed_lengths_pixels) /  len(self.seedObjList),2)
            self.avg_root_length_pixels = np.round(np.sum(self.list_root_lengths_pixels) /  len(self.seedObjList), 2)
        except Exception as e:
            # Print the full traceback if an error occurs during calculation.
            print(traceback.format_exc())
    
    def calculate_std_deviation_and_other(self):
        """
        Calculate the standard deviation of the total seed lengths (in cm)
        and compute the germination percentage.
        """
        self.std_deviation = np.round(np.std(self.list_total_seed_lengths_cm),2)
        self.germination_percent =  np.round(self.germinated_seed_count/ self.n_total_seeds_in_image * 100, 2)
            
    
    def calculate_uniformity_or_Uniformidade(self):
        """
        Calculate the uniformity score, which measures the consistency of seed lengths.
        A higher uniformity indicates that seed lengths are more similar to each other.
        The formula adjusts the uniformity score by subtracting the penalization.
        """
        # Calculate the sum of absolute differences between each seed length and the average (in pixels).
        abs_sum = np.sum([np.abs(l_seed - self.avg_total_length_pixels) for l_seed in self.list_total_seed_lengths_pixels])
        # Calculate uniformity using the formula:
        # Uniformity = (1 - (absolute sum / (total seeds * average length))) * 1000 - penalization
        uni_ = (1 -  (abs_sum / (self.n_total_seeds_in_image * self.avg_total_length_pixels))) * 1000 - self.penalization
        # Ensure the uniformity score is not negative.
        self.uniformity = int(max(0, uni_))

        #"avg_total_length_settings" ----> mudar para "avg_total_length", não é de settings, é o tamanho médio das plântulas na imagem.
        # Uniformidade mede com o Comp.médio das plantulas na imagem.
        # Crescimento que usa o fato 12.05.

    def calculate_growth_or_Crescimento(self):
        """
        Calculate the growth (or 'Crescimento') metric, which represents the relative 
        growth of the seedlings. It is computed as the ratio of the average total seed length 
        to the user-defined average length, scaled by 1000.
        
        Formula:
            Growth = (avg_total_length_cm / user_given_length) * 1000
        """
        self.growth = np.round((self.avg_total_length_cm/ self.avg_total_length_Settings) * 1000)
        # The lenghts are in pixels.
        # 12.05 is the user given lenght, wich correlates 99% to the Vigor-S results.
        
    def calculate_seed_vigor_index(self):
        """
        Calculate the seed vigor index using weighted contributions from the growth and uniformity metrics.
        
        Formula:
            Seed Vigor Index = (Pc * growth) + (Pu * uniformity)
        where Pc and Pu are weight factors defined in the settings.
        """
        # Retrieve weight factors from the settings.
        self.Pc = self.dict_settings['weights_factor_growth_Pc']
        self.Pu = self.dict_settings['weights_factor_uniformity_Pu']

        # Calculate the seed vigor index using the weighted sum.
        self.seed_vigor_index = np.round(self.Pc * self.growth + self.Pu * self.uniformity)
