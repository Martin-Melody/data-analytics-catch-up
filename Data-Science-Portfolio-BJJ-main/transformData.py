import pandas as pd
import re

# Re-load the new data
data_new = pd.read_csv("data_new_sep.csv")

# Correct the column names
data_new.columns = ['Link', 'Name', 'Sub', 'Unused1', 'Unused2']

# Split the 'Name' column
data_new['First Name'] = data_new['Name'].apply(lambda x: x.split('|')[0] if '|' in x else x.split()[0])
data_new['Last Name'] = data_new['Name'].apply(lambda x: x.split('|')[1] if '|' in x else x.split()[1])
data_new['Nickname'] = data_new['Name'].apply(lambda x: x.split('|')[2] if '|' in x and len(x.split('|')) > 2 else x.split()[2] if len(x.split()) > 2 else None)
data_new['Team'] = data_new['Name'].apply(lambda x: x.split('|')[3] if '|' in x and len(x.split('|')) > 3 else ' '.join(x.split()[3:]) if len(x.split()) > 3 else None)

# Split the 'Sub' column into 'Id', 'Opponent', 'W/L', 'Method', 'Competition', 'Weight', 'Stage', and 'Year'
data_new[['Id', 'Opponent', 'W/L', 'Method', 'Competition', 'Weight', 'Stage', 'Year']] = data_new['Sub'].str.split("|", expand=True)

# Drop the original 'Name' and 'Sub' columns
data_new = data_new.drop(columns=['Name', 'Sub', 'Unused1', 'Unused2'])

# Display the processed data
data_new.head()

# Function to check for repeated substrings in a string
def remove_repeated_substrings(s):
    if pd.isna(s):
        return s
    else:
        # Find all substrings
        substrings = [s[i: j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
        
        # Sort substrings by length in descending order
        substrings.sort(key=len, reverse=True)
        
        # Check each substring
        for substring in substrings:
            # If the substring is repeated and is not a single character
            if s.count(substring) > 1 and len(substring) > 1:
                # Replace all instances of the repeated substring with a single instance
                s = s.replace(substring, substring, 1)
        return s

# Apply the function to the 'Opponent' column
data_new['Opponent'] = data_new['Opponent'].apply(remove_repeated_substrings)

# Remove list brackets from 'First Name'
data_new['First Name'] = data_new['First Name'].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").replace(",", ""))

# Display the processed data
data_new.head()

# Function to check for repeated substrings in a string
def remove_repeated_substrings(s):
    if pd.isna(s):
        return s
    else:
        # Find all substrings
        substrings = [s[i: j] for i in range(len(s)) for j in range(i + 2, len(s) + 1)]
        
        # Sort substrings by length in descending order
        substrings.sort(key=len, reverse=True)
        
        # Check each substring
        for substring in substrings:
            # If the substring is repeated and is not a single character
            if s.count(substring) > 1 and len(substring) > 1:
                # Replace all instances of the repeated substring with a single instance
                s = s.replace(substring*2, substring)
        return s

# Apply the function to the 'Opponent' column
data_new['Opponent'] = data_new['Opponent'].apply(remove_repeated_substrings)

# Remove unwanted characters from 'First Name'
data_new['First Name'] = data_new['First Name'].apply(lambda x: x.replace("'", "").replace(",", "").strip())

# Display the processed data
data_new.head()

# Remove unwanted characters from 'First Name' and 'Last Name'
data_new['First Name'] = data_new['First Name'].str.strip(" '[],")
data_new['Last Name'] = data_new['Last Name'].str.strip(" '[],")

# Function to check for repeated names in a string
def remove_repeated_names(s):
    if pd.isna(s):
        return s
    else:
        words = s.split()
        half = len(words) // 2
        if words[:half] == words[half:2*half] and len(words[:half]) > 0:
            return ' '.join(words[:half])
        else:
            return s

# Apply the function to the 'Opponent' column
data_new['Opponent'] = data_new['Opponent'].apply(remove_repeated_names)

# Display the processed data
data_new.head()

# Remove unwanted characters from 'First Name', 'Last Name', 'Nickname', and 'Team'
data_new['First Name'] = data_new['First Name'].str.strip(" '[],")
data_new['Last Name'] = data_new['Last Name'].str.strip(" '[],")
data_new['Nickname'] = data_new['Nickname'].str.strip(" '[],")
data_new['Team'] = data_new['Team'].str.strip(" '[],")

# Display the processed data
data_new.head()

# Get the top 10 teams with the most entries
top_teams = data_new['Team'].value_counts().index[:10]

# Filter the data to include only the top 10 teams
data_top_teams = data_new[data_new['Team'].isin(top_teams)]

# Combine 'First Name' and 'Last Name' to create a 'Full Name' column
data_new['Full Name'] = data_new['First Name'] + ' ' + data_new['Last Name']

# Get the top 10 individuals with the most entries
top_individuals = data_new['Full Name'].value_counts().index[:10]

# Filter the data to include only the top 10 individuals
data_top_individuals = data_new[data_new['Full Name'].isin(top_individuals)]


# Fill NaN values in 'Year' with '0' and convert to integer
data_new['Year'] = data_new['Year'].fillna('0').astype(int)

# Create a count plot for the 'W/L' column
