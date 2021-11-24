import certifi
from pymongo import MongoClient

URI = "mongodb+srv://ossproj.32z9y.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(URI,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-174560122426641057.pem',
                     tlsCAFile=certifi.where()
                     )

db = client['OSSProj']
collection = db['testing']
print(collection.insert_one({"hello": "testing"}))
