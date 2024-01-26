import os
import pandas as pd
import io
import re
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Now it needs to reduce the float point and make the graphs. Later on one big graph with subgraphs

output_filename = "ProSeedling Data"
problematic_files_detailed = []

def updated_process_file_v13(file_path):
    # Skip processing the output file
    if os.path.basename(file_path) == output_filename + '.csv':
        return None
    
    # Extract the base filename without its extension from the full file path.
    # This helps in extracting cultivar and repetition data later.
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    # Use regular expressions (regex) to match the expected filename pattern.
    # The pattern expects the filename to start with one or more letters followed by one or more numbers,
    # and then one single letter. For example, "X1A".
    match = re.match(r"([A-Za-z][0-9]+)([A-Za-z])", base_name)
    # Check if the filename does not match the expected pattern.
    if not match:
        # Add the problematic file to a list for tracking and return None to skip further processing.
        problematic_files_detailed.append((file_path, "Unexpected filename format"))
        return None
    
    # Extract the matched cultivar and repetition from the filename.
    cultivar, repetition = match.groups()
    # Use a try-except block to handle any unexpected errors during file processing.
    try:
        # Initialize lists to store lines related to seedling data and summary data.
        seedling_lines = []
        summary_lines = []
        
        # Open the provided file in read mode with a specific encoding to read its content.
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # Read all lines from the file.
            lines = f.readlines()
            # Define a starting point from where the data of interest begins in the file.
            data_start = 6
            # Flag to track when an empty line is found. This helps in segregating seedling and summary data.
            empty_line_found = False
            # Loop through each line starting from the defined starting point.
            for line in lines[data_start:]:
                # Check if the line is empty (or only contains whitespace).
                if not line.strip():
                    # If an empty line is found for the first time, set the flag and continue to the next iteration.
                    if not empty_line_found:
                        empty_line_found = True
                        continue
                    # If an empty line is found again, break out of the loop.
                    else:
                        break
                # If the empty line flag is set, it means we are in the summary section of the file.
                if empty_line_found:
                    summary_lines.append(line)
                # Otherwise, we are in the seedling data section of the file.
                else:
                    seedling_lines.append(line)

        # Define the column names for the seedling data manually.
        # These columns represent different metrics of the seedlings from the input file.
        seedling_columns = ['Seedling', 'hypocotyl', 'root', 'Total length', 'hypocotyl/root ratio']

        # Convert the seedling lines from the file into a DataFrame using pandas.
        # 'io.StringIO('\n'.join(seedling_lines))' creates a virtual text file in memory from the seedling lines.
        # 'sep=','' indicates that the data in these lines is comma-separated.
        seedling_data = pd.read_csv(io.StringIO('\n'.join(seedling_lines)), sep=',', names=seedling_columns)
        
        # Similarly, convert the summary lines from the file into another DataFrame.
        summary_data = pd.read_csv(io.StringIO('\n'.join(summary_lines)), sep=',')
        
        # Calculate the average value of the 'hypocotyl' column from the seedling data and round it to two decimal places.
        hyp_average = round(seedling_data['hypocotyl'].mean(), 2)

        # Calculate the average value of the 'root' column from the seedling data and round it to two decimal places.
        root_average = round(seedling_data['root'].mean(), 2)

        # Calculate the average value of the 'Total length' column from the seedling data and round it to two decimal places.
        length_average = round(seedling_data['Total length'].mean(), 2)

        # Calculate the average value of the 'hypocotyl/root ratio' column from the seedling data and round it to two decimal places.
        hr_average = round(seedling_data['hypocotyl/root ratio'].mean(), 2)
        
        # Extract the Germination value from the summary data.
        # Since it might contain a '%' symbol, we need to handle both cases (with or without the symbol).
        # The value is converted to a floating-point number for further calculations.
        germination_string = str(summary_data['Germination'].values[0])
        germination_value = float(germination_string.replace('%', '')) if '%' in germination_string else float(germination_string)
        

        # Construct the final dictionary
        final_dict = {
            "Cultivar": cultivar,
            "Repetition": repetition,
            "HypAverage": hyp_average,
            "RootAverage": root_average,
            "LengthAverage": length_average,
            "H/RAverage": hr_average,
            "Vigor": summary_data['Vigor Index'].values[0],
            "Growth": summary_data['Growth'].values[0],
            "Uniformity": summary_data['Uniformity'].values[0],
            "Germination": germination_value,
            "STDeviation": summary_data['Standard deviation'].values[0],
            "Normal": summary_data['Normal Seedlings'].values[0],
            "Abnormal": summary_data['Abnormal Seedlings'].values[0],
            "Dead": summary_data['Non germinated seeds'].values[0]
        }
    
        # Calculate STATS values
        final_dict["HypSTATS"] = (final_dict["HypAverage"] + 0.5) ** 0.5
        final_dict["RootSTATS"] = (final_dict["RootAverage"] + 0.5) ** 0.5
        final_dict["LenAvSTATS"] = (final_dict["LengthAverage"] + 0.5) ** 0.5
        final_dict["H/RSTATS"] = (final_dict["H/RAverage"] + 0.5) ** 0.5
        final_dict["GrowthSTATS"] = (float(final_dict["Growth"]) + 0.5) ** 0.5
        final_dict["UniformSTATS"] = (float(final_dict["Uniformity"]) + 0.5) ** 0.5
        final_dict["VigorSTATS"] = (float(final_dict["Vigor"]) + 0.5) ** 0.5
        final_dict["GerminSTATS"] = (final_dict["Germination"] / 100) ** 0.5
    
        return pd.DataFrame([final_dict])  # Return a DataFrame with a single row
    
    
    # Try to execute a block of code (above).
    # If any exception (error) occurs while executing that block of code, 
    # the code inside the 'except' block will be executed.
    except Exception as e:
        # Append a tuple to the 'problematic_files_detailed' list. 
        # The tuple contains the file path and the error message.
        problematic_files_detailed.append((file_path, str(e)))
        
        # Return None from the current function. This usually indicates that the function couldn't 
        # complete its intended task due to the encountered error.
        return None
    
    

def process_all_files_dynamically():
    # Get a list of all .csv file paths in the script's directory
    csv_file_paths = glob.glob('*.csv')
    
    # Exclude the output file from the list of files to process
    csv_file_paths = [path for path in csv_file_paths if os.path.basename(path) != output_filename + '.csv']
    
    # Create an empty list named 'dfs' that will store DataFrames created from each CSV file.
    dfs = []
    
    # Iterate through each file path in the 'csv_file_paths' list.
    for file_path in csv_file_paths:
        # Process the current CSV file using the 'updated_process_file_v13' function.
        # The function reads the data, processes it, and returns a DataFrame.
        processed_df = updated_process_file_v13(file_path)
        
        # Check if the DataFrame returned from the function is not None (i.e., the file was successfully processed).
        if processed_df is not None:
            
            # If successfully processed, append the resulting DataFrame to the 'dfs' list.
            dfs.append(processed_df)
    
    # Check if any dataframe exists before concatenating and rearranging columns
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        
        # Rearrange columns
        ordered_columns = ['Cultivar', 'Repetition', 'HypAverage', 'RootAverage', 'LengthAverage', 'H/RAverage',
                           'Vigor', 'Growth', 'Uniformity', 'Germination', 'STDeviation', 'Normal', 'Abnormal', 'Dead', 
                           'HypSTATS', 'RootSTATS', 'LenAvSTATS', 'H/RSTATS', 'GrowthSTATS', 'UniformSTATS', 'VigorSTATS', 'GerminSTATS']
        
        final_df = final_df[ordered_columns]
        
        # Enforce numeric data type
        columns_to_enforce_numeric = ['HypSTATS', 'RootSTATS', 'LenAvSTATS', 'H/RSTATS', 'GrowthSTATS', 'UniformSTATS', 'VigorSTATS', 'GerminSTATS']

        # Iterate through each column name provided in the 'columns_to_enforce_numeric' list.
        for col in columns_to_enforce_numeric:
            # Convert the column in the 'final_df' DataFrame to numeric type.
            # If there are any errors or invalid values during the conversion, replace them with NaN (due to the 'coerce' parameter).
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce')

        # Convert DataFrame to string with European number formatting
        combined_data_str = final_df.to_csv(sep=';', decimal=',', index=False)

        # Save the result to a CSV file in the same directory as the script
        output_file_path = os.path.join('.', output_filename + '.csv')
        with open(output_file_path, 'w', newline='') as file:
            file.write('SEP=;\n')
            file.write(combined_data_str)
    else:
        print("No files were successfully processed.")


    return final_df

# You can call the function to start processing when the script is run
final_df = process_all_files_dynamically()

def plot_cultivar_data(final_df):
    """
    Plots a series of bar graphs for the given DataFrame.

    Args:
    final_df (DataFrame): A pandas DataFrame containing the cultivar data.
    """
    # Check if the DataFrame is empty or not
    if final_df.empty:
        print("The DataFrame is empty. No data to plot.")
        return

    # Creating a figure with 6 subplots (one for each variable)
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    fig.suptitle('Cultivar Data Analysis')

    # Plotting each variable in a subplot
    sns.barplot(x='Cultivar', y='HypAverage', data=final_df, ax=axes[0, 0], errorbar='sd')
    axes[0, 0].set_title('HypAverage')

    sns.barplot(x='Cultivar', y='RootAverage', data=final_df, ax=axes[0, 1], errorbar='sd')
    axes[0, 1].set_title('RootAverage')

    sns.barplot(x='Cultivar', y='LengthAverage', data=final_df, ax=axes[0, 2], errorbar='sd')
    axes[0, 2].set_title('LengthAverage')

    sns.barplot(x='Cultivar', y='Vigor', data=final_df, ax=axes[1, 0], errorbar='sd')
    axes[1, 0].set_title('Vigor')

    sns.barplot(x='Cultivar', y='Growth', data=final_df, ax=axes[1, 1], errorbar='sd')
    axes[1, 1].set_title('Growth')

    sns.barplot(x='Cultivar', y='Uniformity', data=final_df, ax=axes[1, 2], errorbar='sd')
    axes[1, 2].set_title('Uniformity')

    # Adjusting layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    # Save the plot
    plt.savefig('Visual_data', dpi=600)

    # Show the plot
    plt.show()

plot_cultivar_data(final_df)