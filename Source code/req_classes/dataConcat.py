"""
dataConcat.py

Este arquivo faz parte do projeto ProSeedling.
Distribuído sob os termos da GNU General Public License.
"""

import glob
import os
import pandas as pd

# Nome do arquivo de saída (sem extensão)
output_filename = "combined_data"

def updated_process_file_v13(file_path):
    """
    Função auxiliar para processar cada arquivo CSV.
    Tenta ler o CSV, tratando o cabeçalho especial 'SEP=;' se presente.
    Retorna um DataFrame ou None em caso de erro.
    """
    try:
        with open(file_path, 'r') as f:
            # Verifica se a primeira linha contém a indicação do separador
            first_line = f.readline()
        # Se a primeira linha começar com 'SEP=', use skiprows para ignorá-la
        if first_line.startswith('SEP='):
            df = pd.read_csv(file_path, sep=';', skiprows=1, decimal=',')
        else:
            df = pd.read_csv(file_path, sep=';', decimal=',')
        return df
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")
        return None

class dataConcat:
    def __init__(self):
        pass

    def csv_concat(self, folder_path):
        """
        Procura todos os arquivos CSV na pasta informada, excluindo o arquivo de saída,
        processa cada um e concatena os dados em um único DataFrame.
        Em seguida, reordena as colunas, converte certas colunas para numérico e salva o CSV final.
        """
        # Busca todos os arquivos .csv na pasta especificada
        csv_file_paths = glob.glob(os.path.join(folder_path, '*.csv'))
        
        # Exclui o arquivo de saída, caso já exista na pasta
        csv_file_paths = [path for path in csv_file_paths 
                          if os.path.basename(path) != output_filename + '.csv']

        dfs = []
        # Processa cada arquivo CSV
        for file_path in csv_file_paths:
            processed_df = updated_process_file_v13(file_path)
            if processed_df is not None:
                dfs.append(processed_df)
        
        if dfs:
            final_df = pd.concat(dfs, ignore_index=True)
            
            # Reordena as colunas conforme a ordem desejada
            ordered_columns = ['Cultivar', 'Repetition', 'HypAverage', 'RootAverage', 'LengthAverage', 'H/RAverage',
                               'Vigor', 'Growth', 'Uniformity', 'Germination', 'STDeviation', 'Normal', 'Abnormal', 'Dead', 
                               'HypSTATS', 'RootSTATS', 'LenAvSTATS', 'H/RSTATS', 'GrowthSTATS', 'UniformSTATS', 'VigorSTATS', 'GerminSTATS']
            # Mantém apenas as colunas que estiverem disponíveis
            final_df = final_df[[col for col in ordered_columns if col in final_df.columns]]
            
            # Converte para numérico as colunas especificadas (caso seja possível)
            columns_to_enforce_numeric = ['HypSTATS', 'RootSTATS', 'LenAvSTATS', 'H/RSTATS', 
                                          'GrowthSTATS', 'UniformSTATS', 'VigorSTATS', 'GerminSTATS']
            for col in columns_to_enforce_numeric:
                if col in final_df.columns:
                    final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
            
            # Salva o DataFrame concatenado em um CSV
            combined_data_str = final_df.to_csv(sep=';', decimal=',', index=False)
            output_file_path = os.path.join(folder_path, output_filename + '.csv')
            with open(output_file_path, 'w', newline='') as file:
                file.write('SEP=;\n')
                file.write(combined_data_str)
        else:
            print("Nenhum arquivo foi processado com sucesso.")
            final_df = pd.DataFrame()  # Retorna um DataFrame vazio se não houver arquivos processados

        return final_df