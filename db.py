from pymongo import MongoClient

URI = "mongodb+srv://ossproj.32z9y.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(URI,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-174560122426641057.pem')
db = client['testDB']
collection = db['testCol']
print(collection)
# doc_count = collection.count_documents({})
# print(doc_count)
