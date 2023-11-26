import csv

def get_year_range(filename):
    # List to store all the years from the dataset
    years = []

    # Open the CSV file and read its content
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            years.append(int(row['year']))

    # Find the min and max year
    min_year = min(years)
    max_year = max(years)

    return min_year, max_year

# Get the year range from the CSV file
filename = 'adcc_historical_data.csv'
min_year, max_year = get_year_range(filename)

print(f"The data ranges from {min_year} to {max_year}.")
