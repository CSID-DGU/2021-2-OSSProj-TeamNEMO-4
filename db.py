import certifi
from pymongo import MongoClient

from Games.game_settings import *

try:
    URI = "mongodb+srv://ossproj.32z9y.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(URI,
                         tls=True,
                         tlsCertificateKeyFile='X509-cert-174560122426641057.pem',
                         tlsCAFile=certifi.where()
                         )

    db = client['OSSProj']
    print("Success to connect DB")
except:
    print("DB 연결 오류")


def record_score(mode, new_record, old_record):
    if mode == SELECT:
        collection = db[SELECT]
        return
    elif mode == INFINITE:
        collection = db[INFINITE]
        collection.delete_one(old_record)
        collection.insert_one(new_record)
        return
    elif mode == BEST_RECORD:
        collection = db[BEST_RECORD]
        return


def get_score(mode, *game):
    scores = None
    if mode == SELECT:
        collection = db[SELECT]
        scores = collection.find()
        # game 에 따라 분류 한 번 해야함.
    elif mode == (INFINITE or BEST_RECORD):
        collection = db[INFINITE]
        scores = collection.find().sort("score")
    return scores
