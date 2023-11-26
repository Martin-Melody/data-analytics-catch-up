def convert_to_csv(input_filename, output_filename):
    # Read the data from the input file
    with open(input_filename, 'r') as infile:
        data = infile.read()

    # Convert to CSV format
    csv_data = data.replace(';', ',')

    # Write the converted data to the output file
    with open(output_filename, 'w') as outfile:
        outfile.write(csv_data)

# Specify input and output filenames
input_file = 'input.csv'
output_file = 'adcc_historical_data.csv'

# Perform the conversion
convert_to_csv(input_file, output_file)
print(f"Data converted and saved to {output_file}")
