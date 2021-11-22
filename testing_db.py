from pymongo import MongoClient

client = MongoClient(
    f'mongodb+srv://TeamNEMO:{PASSWORD}@ossproj.kyosv.mongodb.net/SquidGame?retryWrites=true&w=majority')
db = client.test
print(db)
