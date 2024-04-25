import json
import csv

def json_to_csv(json_file, csv_file, delimiter=','):
    """Converts JSON data with arrays to CSV, preserving dimensional integrity.

    Args:
        json_file (str): Path to the JSON input file.
        csv_file (str): Path to the output CSV file.
        delimiter (str, optional): Delimiter to use in the CSV file (default: ',').
    """

    with open(json_file, 'r') as json_data, open(csv_file, 'w', newline='') as csvfile:
        json_data = json.load(json_data)

        # Handle edge case: empty JSON array
        if not json_data:
            return

        # Calculate dimensions (y rows) from the length of the outer array
        y_rows = len(json_data)

        # Determine column count (x) from the length of the first inner array
        # (assuming consistent array lengths)
        try:
            x_columns = len(json_data[0])
        except IndexError:  # Handle case of empty inner arrays
            x_columns = 0

        writer = csv.writer(csvfile, delimiter=delimiter)

        # Create headers as "Column1", "Column2", etc.
        headers = [f'Column{i+1}' for i in range(x_columns)]
        writer.writerow(headers)

        for row in json_data:
            # Ensure consistent row length (x columns) by padding with empty values
            row.extend([''] * (x_columns - len(row)))
            writer.writerow(row)

# Example usage:
json_file = 'surf_f/Air-force.json'
csv_file = 'converted_data.csv'

json_to_csv(json_file, csv_file)
