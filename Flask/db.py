
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()
mongo_uri = os.getenv('MONGO_URI')

# Create a new client and connect to the server
client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.test
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)