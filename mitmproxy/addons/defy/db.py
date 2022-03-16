import os
from pymongo import MongoClient


MONGO_URL = os.getenv("MONGO_MITM_URI", "mongodb://root:rootpassword@host.docker.internal:27017")

dbclient = MongoClient(MONGO_URL)

