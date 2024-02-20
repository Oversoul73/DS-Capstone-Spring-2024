from pymongo import MongoClient

client = MongoClient("mongodb+srv://hm2np:capstone2024@cluster0.0ahrvhs.mongodb.net/?retryWrites=true&w=majority")

db = client.test

collection_name = db["test1"]
