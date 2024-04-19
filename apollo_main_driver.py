from input import state_expansion
from datetime import datetime, timedelta
from datetime import time as datetime_time
import os,csv

import pandas as pd

def combine_csv_files(file_paths, output_file):
    """
    Combine multiple CSV files into one.

    Args:
        file_paths (list): List of file paths to CSV files.
        output_file (str): File path for the combined CSV file.
    """
    # List to store DataFrames
    dfs = []

    # Load each CSV file into a DataFrame and append to dfs list
    for file_path in file_paths:
        dfs.append(pd.read_csv(file_path,encoding='utf-8'))

    # Concatenate DataFrames vertically (row-wise)
    combined_df = pd.concat(dfs, ignore_index=True)

    # Write combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False,encoding='utf-8')

    print("Combined CSV files successfully into", output_file)


def split_csv(input_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the input CSV file
    with open(input_file, 'r',encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read header row
        data = list(csv_reader)    # Read data rows

    # Calculate number of rows in each part
    total_rows = len(data)
    rows_per_part = total_rows // 3
    remainder = total_rows % 3

    # Iterate through each part and write to separate CSV files
    for i in range(3):
        start_index = i * rows_per_part
        end_index = start_index + rows_per_part
        if i < remainder:
            end_index += 1

        part_data = data[start_index:end_index]

        # Write part data to CSV file
        output_file = os.path.join(output_dir, f'input_{i+1}.csv')
        # output_file = os.path.join(output_dir, f'output_apollo_company_{i+1}.csv')

        with open(output_file, 'w', newline='',encoding='utf-8') as part_csv:
            csv_writer = csv.writer(part_csv)
            csv_writer.writerow(header)
            csv_writer.writerows(part_data)

    print("CSV file split into 3 equal parts successfully.")

if __name__ == "__main__":
    print("Splitting Input File to all bots")
    splited = False
    while True:
        current_time = datetime.now().time()
        if datetime_time(0, 2) <= current_time < datetime_time(0, 16):

            if splited==False:
                state_expansion.expand()
                #call split function here
                split_csv(os.getcwd()+r"/input/expanded_input.csv","bot_use_only")
                # split_csv(r"E:\PycharmProjects\apollo_zoom\output\output_apollo_company.csv","bot_use_only")

                splited = True
                print("Split Done")
        else:
            splited = False

