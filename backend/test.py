from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["smartdustbin"]
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
