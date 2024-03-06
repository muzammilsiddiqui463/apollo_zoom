import csv
import os
def write_dicts_to_csv(list_of_dicts, filename):
    # Extract fieldnames from the first dictionary in the list
    fieldnames = list_of_dicts[0].keys()

    # Write the dictionaries to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in list_of_dicts:
            writer.writerow(row)

# Function to read CSV file and convert rows to list of dictionaries
def csv_to_dicts(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
def expand():
    # Paths to the input files
    input_path = os.getcwd()+"/input/input.csv"
    states_path = os.getcwd()+"/input/states.csv"

    # Read input and states data as list of dictionaries
    input_data = csv_to_dicts(input_path)
    states_data = csv_to_dicts(states_path)

    # Expand the input data with each state and city
    expanded_rows = []

    for row in input_data:
        for state_row in states_data:
            # Create a new row for each state and city, preserving the original data
            new_row = row.copy()
            new_row['Country'] = f"{state_row['City'].replace(' city','').strip()}, {state_row['State']}"
            expanded_rows.append(new_row)

    # Export the expanded data to a CSV file
    output_path = os.getcwd()+"/input/expanded_input.csv"
    write_dicts_to_csv(expanded_rows, output_path)
expand()