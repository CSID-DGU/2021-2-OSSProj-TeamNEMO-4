import certifi
from pymongo import MongoClient

from Games.game_settings import *

URI = "mongodb+srv://ossproj.32z9y.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(URI,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-174560122426641057.pem',
                     tlsCAFile=certifi.where()
                     )
print(123)
db = client['OSSProj']
collection = db['testing']


def record_score(mode, object):
    if mode == SELECT:
        collection = db[SELECT]
        return
    elif mode == INFINITE:
        collection = db[INFINITE]
        return
    elif mode == BEST_RECORD:
        collection = db[BEST_RECORD]
        return
