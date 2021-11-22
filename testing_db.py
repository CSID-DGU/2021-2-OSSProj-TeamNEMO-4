from pymongo import MongoClient

client = MongoClient(
    f'mongodb+srv://TeamNEMO:oo1735oo1735@ossproj.kyosv.mongodb.net/SquidGame?retryWrites=true&w=majority')
db = client.test
print(db)
