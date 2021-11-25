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
    print("recording new score...")
    collection = db[mode]
    collection.delete_one(old_record)
    collection.insert_one(new_record)


def get_score(mode, game=None):
    scores = None
    print(mode, "get score from DB...")
    if mode == SELECT:
        collection = db[mode]
        scores = collection.find({"game": game}).sort("score", -1)
    elif mode == INFINITE or mode == BEST_RECORD:
        collection = db[mode]
        scores = collection.find().sort("score", -1)  # 내림차순 정렬
    return scores
