# dataConcat.py. Concatenates CSV files in a folder, extracts seed and summary data, 
# and writes the consolidated results to an output CSV file.

import os
import glob
import pandas as pd

class dataConcat:
    def __init__(self, folder_path=None, output_filename="ProSeedling_data.csv"):
        """
        Initialize the DataConcat instance.
        
        Parameters:
            folder_path: Directory containing CSV files. If None, defaults to the script's directory.
            output_filename: Name of the output CSV file that will store the consolidated data.
        """
        # If no folder path is provided, use the directory of this script.
        if folder_path is None:
            folder_path = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = folder_path
        self.output_filename = output_filename
        # Create the full path for the output CSV file.
        self.output_csv = os.path.join(self.folder_path, self.output_filename)

    def process(self):
        """
        Process all CSV files in the folder, extract seed data and summary metrics,
        and write a consolidated CSV output.
        
        Returns:
            The number of CSV files processed (i.e. the number of rows in the output DataFrame).
        """
        print(f"Processando arquivos CSV no diretório: {self.folder_path}...")
        final_data = [] # List to hold dictionaries of processed data from each CSV file.

        # Loop through all CSV files in the specified folder.
        for file_path in glob.glob(os.path.join(self.folder_path, '*.csv')):
            # Skip the output CSV file if it already exists in the folder.
            if os.path.basename(file_path) == self.output_filename:
                continue

            # Get the base file name (without extension) to extract metadata.
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            # Skip files with too short a name.
            if len(base_name) < 2:
                continue
            # The last character represents the repetition number.
            repetition = base_name[-1]
            # The rest of the base name is considered the cultivar name.
            cultivar = base_name[:-1]

            # Try to read the CSV file while skipping the first row (e.g., header note).
            try:
                df = pd.read_csv(file_path, skiprows=1, delimiter=',', encoding='utf-8')
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

            # Strip any extra spaces from column names.
            df.columns = df.columns.str.strip()
            print(f"File: {file_path}")
            print("Columns found:", df.columns.tolist())

            # Define the required columns for seed data.
            seed_cols = ["Hypocotyl", "Root", "Total length", "Hypocotyl/root ratio"]
            # Identify any missing seed columns.
            missing_seed_cols = [col for col in seed_cols if col not in df.columns]
            if missing_seed_cols:
                print(f"Skipping file {file_path} because it is missing columns: {missing_seed_cols}")
                continue

            # Remove rows where any of the seed columns have NaN values.
            seedling_data = df.dropna(subset=seed_cols)
            if seedling_data.empty:
                print(f"Skipping file {file_path} because there is no seed data after dropping NAs.")
                continue

            # Calculate averages for the seed measurements.
            hyp_average = round(seedling_data['Hypocotyl'].mean(), 2)
            root_average = round(seedling_data['Root'].mean(), 2)
            length_average = round(seedling_data['Total length'].mean(), 2)
            hr_average = round(seedling_data['Hypocotyl/root ratio'].mean(), 2)

            # Define the required columns for summary metrics.
            summary_cols = [
                "Vigor Index", "Growth", "Uniformity", "Germination",
                "Standard deviation", "Normal Seedlings", "Abnormal Seedlings", "Non germinated seeds"
            ]
            # Identify any missing summary columns.
            missing_summary_cols = [col for col in summary_cols if col not in df.columns]
            if missing_summary_cols:
                print(f"Skipping file {file_path} because it is missing summary columns: {missing_summary_cols}")
                continue

            # Remove rows where summary columns have NaN values.
            summary_df = df.dropna(subset=summary_cols)
            if summary_df.empty:
                print(f"Skipping file {file_path} because no summary row was found.")
                continue

            # Extract the first valid summary row.
            summary_row = summary_df.iloc[0]
            vigor = summary_row["Vigor Index"]
            growth = summary_row["Growth"]
            uniformity = summary_row["Uniformity"]
            germination = summary_row["Germination"]
            # Remove '%' symbol from germination if present.
            if isinstance(germination, str) and '%' in germination:
                germination = germination.replace('%', '')
            try:
                germination = float(germination)
            except ValueError:
                print(f"Could not convert Germination value to float in file {file_path}. Skipping file.")
                continue

            stdev = summary_row["Standard deviation"]
            normal = summary_row["Normal Seedlings"]
            abnormal = summary_row["Abnormal Seedlings"]
            dead = summary_row["Non germinated seeds"]

            # Convert summary values to integers after rounding.
            try:
                vigor = int(round(float(vigor)))
                growth = int(round(float(growth)))
                uniformity = int(round(float(uniformity)))
                germination = int(round(germination))
                normal = int(round(float(normal)))
                abnormal = int(round(float(abnormal)))
                dead = int(round(float(dead)))
            except Exception as e:
                print(f"Conversion error in file {file_path}: {e}. Skipping file.")
                continue

            # Build a dictionary of the consolidated data for the current file.
            final_dict = {
                "Cultivar": cultivar,
                "Repetition": repetition,
                "HypAverage": hyp_average,
                "RootAverage": root_average,
                "LengthAverage": length_average,
                "H/RAverage": hr_average,
                "Vigor": vigor,
                "Growth": growth,
                "Uniformity": uniformity,
                "Germination": germination,
                "STDeviation": stdev,
                "Normal": normal,
                "Abnormal": abnormal,
                "Dead": dead
            }
            final_data.append(final_dict)

        # Create a DataFrame from the list of dictionaries, ensuring columns are in a specific order.
        final_df = pd.DataFrame(final_data, columns=[
            "Cultivar", "Repetition", "HypAverage", "RootAverage", "LengthAverage", "H/RAverage",
            "Vigor", "Growth", "Uniformity", "Germination", "STDeviation",
            "Normal", "Abnormal", "Dead"
        ])

        # Write the consolidated DataFrame to the output CSV file.
        try:
            with open(self.output_csv, 'w', newline='', encoding='utf-8') as out_f:
                # Write a separator line for Excel compatibility.
                out_f.write("SEP=,\n")
                final_df.to_csv(out_f, index=False)
            print(f"Done! Processed {len(final_df)} file(s) and wrote '{self.output_csv}'.")
        except Exception as e:
            print(f"Error writing the output CSV: {e}")
        
        # Return the number of processed CSV files (rows in the output DataFrame)
        return len(final_df)


if __name__ == "__main__":
    # When running this module as a script, create a dataConcat instance and process the files.
    dc = dataConcat()
    dc.process()
