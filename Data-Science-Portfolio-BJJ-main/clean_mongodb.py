import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import ast

# Define MongoDB connection
uri = "mongodb+srv://<name>:<password>@mong1.5vptx5d.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Bjj_data']
collection = db['bjj_data']

# Define the URL
url = "https://www.bjjheroes.com/a-z-bjj-fighters-list"

# Make a request to the website
response = requests.get(url)

# Create a Beautiful Soup object
soup = BeautifulSoup(response.text, "html.parser")

# Find the table
table = soup.find("tbody", {"class":"row-hover"})

# Create a list to store dictionaries (each dictionary represents a row in the table)
data_list = []

# Iterate over each row in the table
for row in table.find_all("tr"):
    # Find all the td elements in the row
    tds = row.find_all("td")

    # Extract the text from each td element
    data = [td.get_text(strip=True) for td in tds]
    data_str = '|'.join(data)

    # Find the first anchor tag in the row
    anchor = row.find("a")

    # Extract the href attribute value
    href = anchor["href"]

    href_response = requests.get("https://www.bjjheroes.com"+href)
    href_soup = BeautifulSoup(href_response.text, "html.parser")
    href_table = href_soup.find("tbody")

    if href_table:
        for href_row in href_table.find_all("tr"):
            href_tds = href_row.find_all("td")
            href_data = [td.get_text(strip=True) for td in href_tds]
            href_data_str = '|'.join(href_data)

            # Create a dictionary for this row and add it to the list
            data_list.append({"First Name": href, "Last Name": data_str, "Nickname": href_data_str})

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data_list)

# Perform the cleaning steps here (e.g., splitting columns, removing rows, etc.)
df[['First Name','Last Name','Nickname','Team']] = df['Name'].str.split("|", expand=True)

# Split the 'Sub' column into 'Id', 'Opponent', 'W/L', 'Method', 'Competition', 'Weight', 'Stage', and 'Year'
df[['Id', 'Opponent', 'W/L', 'Method', 'Competition', 'Weight', 'Stage', 'Year']] = df['Sub'].str.split("|", expand=True)

# Define the function to remove repeated substrings in 'Opponent'
def remove_repeated_substrings(s):
    if pd.isna(s):
        return s
    substrings = set()
    new_string = ''
    
    for char in s:
        new_string += char
        if new_string in substrings:
            new_string = ''
        else:
            substrings.add(new_string)
    
    return new_string

# Apply the function to the 'Opponent' column
df['Opponent'] = df['Opponent'].apply(remove_repeated_substrings)

# Remove rows where 'W/L' is not 'W', 'L', or 'D'
df = df[df['W/L'].isin(['W', 'L', 'D'])]

# Remove rows where 'Weight', 'Stage', or 'Year' is missing
df = df.dropna(subset=['Weight', 'Stage', 'Year'])

# Convert the cleaned DataFrame to a list of dictionaries
data_dict = df.to_dict("records")

# Insert the list of dictionaries into the MongoDB collection
collection.insert_many(data_dict)
