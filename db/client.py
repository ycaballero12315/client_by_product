from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Mongo local
#db_client = MongoClient().local  # Assuming 'local' is the database name  
#  
# Mongo Atlas

load_dotenv()  
uri = os.getenv("DATABASE_URL") 
#uri = "mongodb+srv://yoevev:   

# Create a new db_client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'))
db = db_client.get_database("Cluster0")  # Replace with your database name
# Check if the connection was successful
if db:
    print("Connected to the database successfully")
# Send a ping to confirm a successful connection
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)