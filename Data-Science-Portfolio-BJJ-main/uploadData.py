import ast
from pymongo.mongo_client import MongoClient
import pandas as pd

uri = "mongodb+srv://<name>:<password>@mong1.5vptx5d.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Bjj_data']
collection = db['bjj_data']
# Open the CSV file and read the lines

data = pd.read_csv('data_transform_new.csv')
data.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

data_dict = data.to_dict("records")
collection.insert_many(data_dict)