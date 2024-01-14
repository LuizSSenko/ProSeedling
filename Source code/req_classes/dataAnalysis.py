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
from .contour_processor import Seed
from proj_settings import MainSettings, SeedHealth
import json
import numpy as np
import traceback

settings_path = MainSettings.settings_json_file_path

# with open(settings_path, 'r') as f:
#     dict_settings = json.load(f)



class BatchAnalysisNew:
    def __init__(self, img_path, batchNumber, seedObjList:list[Seed]):
        self.batchNumber = batchNumber
        self.dict_settings = None
        self.seedObjList = seedObjList


        self.list_total_seed_lengths = []

        self.n_total_seeds_in_image = 0

        self.germinated_seed_count = 0
        self.dead_seed_count = 0
        self.abnormal_seed_count = 0

        self.growth = 0
        self.penalization = 0
        self.uniformity = 0
        self.seed_vigor_index = 0

        self.avg_total_length_settings = 0  # in pixels
        self.avg_total_length_cm = 0
        self.avg_hypocotyl_length_cm = 0  # in cm
        self.avg_root_length_cm = 0 # in cm

        self.avg_hypocotyl_length_pixels = 0
        self.avg_root_length_pixels = 0
        self.std_deviation = 0
        self.germination_percent = 0

        self.recalculate_all_metrics()


    def recalculate_all_metrics(self):

        settings_path = MainSettings.settings_json_file_path

        with open(settings_path, 'r') as f:
            self.dict_settings = json.load(f)



        self.get_seed_class_count()

        self.calculate_averages()
        self.calculate_growth_or_Crescimento()
        self.calc_penalization()
        self.calculate_uniformity_or_Uniformidade()
        self.calculate_seed_vigor_index()
        self.calculate_std_deviation_and_other()

    def get_seed_class_count(self):
        self.dead_seed_count, self.abnormal_seed_count, self.germinated_seed_count = 0,0,0

        for seedObj in self.seedObjList:
            
            if seedObj.seed_health == SeedHealth.DEAD_SEED:
                self.dead_seed_count+=1
                
            elif seedObj.seed_health == SeedHealth.ABNORMAL_SEED:
                self.abnormal_seed_count+=1
                
            elif seedObj.seed_health == SeedHealth.NORMAL_SEED:
                self.germinated_seed_count+=1

        print("Dead seed count", self.dead_seed_count)
        print("Abnormal seed count", self.abnormal_seed_count)
        print("Normal seed count", self.germinated_seed_count)

        self.n_total_seeds_in_image = self.dead_seed_count + self.abnormal_seed_count+self.germinated_seed_count


    def calc_penalization(self):

        # self.penalization = self.dead_seed_count * 50 / self.n_total_seeds_in_image # ERRADO!
        self.penalization = self.dead_seed_count *( 50 / self.n_total_seeds_in_image) # Correto!

        return self.penalization


    def calculate_averages(self):
        print("BatchANEW")

        # cm
        self.list_total_seed_lengths_cm = []
        self.list_hypocotyl_seed_lengths_cm = []
        self.list_root_lengths_cm = []
        # Pixels
        self.list_total_seed_lengths_pixels = []
        self.list_hypocotyl_seed_lengths_pixels = []
        self.list_root_lengths_pixels = []

        for seedObj in self.seedObjList:
            # cm
            self.list_total_seed_lengths_cm.append(seedObj.total_length_cm)
            self.list_hypocotyl_seed_lengths_cm.append(seedObj.hyperCotyl_length_cm)
            self.list_root_lengths_cm.append(seedObj.radicle_length_cm)
            # Pixels
            self.list_total_seed_lengths_pixels.append(seedObj.total_length_pixels)
            self.list_hypocotyl_seed_lengths_pixels.append(seedObj.hyperCotyl_length_pixels)
            self.list_root_lengths_pixels.append(seedObj.radicle_length_pixels)

        # cm
        self.avg_total_length_cm = np.round(np.sum(self.list_total_seed_lengths_cm) /  len(self.seedObjList), 2)
        # Pixels
        self.avg_total_length_pixels = np.round(np.sum(self.list_total_seed_lengths_pixels) /  len(self.seedObjList), 2)
        # User given data
        self.avg_total_length_Settings = self.dict_settings['user_given_seedling_length']
        try:
            # cm
            self.avg_hypocotyl_length_cm = np.round(np.sum(self.list_hypocotyl_seed_lengths_cm) /  len(self.seedObjList),2)
            self.avg_root_length_cm = np.round(np.sum(self.list_root_lengths_cm) /  len(self.seedObjList), 2)
            # Pixels
            self.avg_hypocotyl_length_pixels = np.round(np.sum(self.list_hypocotyl_seed_lengths_pixels) /  len(self.seedObjList),2)
            self.avg_root_length_pixels = np.round(np.sum(self.list_root_lengths_pixels) /  len(self.seedObjList), 2)
        except Exception as e:
            print(traceback.format_exc())
    
    def calculate_std_deviation_and_other(self):
        self.std_deviation = np.round(np.std(self.list_total_seed_lengths_cm),2)
        self.germination_percent =  np.round(self.germinated_seed_count/ self.n_total_seeds_in_image * 100, 2)
            
    
    def calculate_uniformity_or_Uniformidade(self):
        abs_sum = np.sum([np.abs(l_seed - self.avg_total_length_pixels) for l_seed in self.list_total_seed_lengths_pixels])
        uni_ = (1 -  (abs_sum / (self.n_total_seeds_in_image * self.avg_total_length_pixels))) * 1000 - self.penalization 
        self.uniformity = int(max(0, uni_))
        #"avg_total_length_settings" ----> mudar para "avg_total_length", não é de settings, é o tamanho médio das plântulas na imagem.
        # Uniformidade mede com o Comp.médio das plantulas na imagem.
        # Crescimento que usa o fato 12.05.

    def calculate_growth_or_Crescimento(self):
        """ growth (or Crescimento) = avg of seed lengths(rad+hyp) / max length * 1000
        COMPRIMENTO MÉDIO DA PLÂNTULA INTEIRA / COMPRIMENTO MÉDIO (USUÁRIO) * 1000
        """
        ## wrong formula before       
        # self.growth = self.avg_total_length / max(self.list_total_seed_lengths) * 1000

        # self.ph_ = self.dict_settings['ph']
        # self.pr_ = self.dict_settings['pr']
        # factor_pixel_to_cm = self.dict_settings['factor_pixel_to_cm']

        # self.avg_hypocotyl_length_pixels = self.avg_hypocotyl_length_cm * factor_pixel_to_cm
        # self.avg_root_length_pixels = self.avg_root_length_cm * factor_pixel_to_cm

        # self.growth = min(self.avg_root_length_pixels* self.pr_ + self.avg_hypocotyl_length_pixels *self.ph_, 1000)
        self.growth = np.round((self.avg_total_length_cm/ self.avg_total_length_Settings) * 1000)
        
        # The lenghts are in pixels.
        # 12.05 is the user given lenght, wich correlates 99% to the Vigor-S results.
        
    def calculate_seed_vigor_index(self):

        """ Vigor = Pc * growth (or Crescimento) + Pu * Uniformity (or Uniformidade)"""
        self.Pc = self.dict_settings['weights_factor_growth_Pc']
        self.Pu = self.dict_settings['weights_factor_uniformity_Pu']
        self.seed_vigor_index = np.round(self.Pc * self.growth + self.Pu * self.uniformity)

    
