import os
from pymongo import MongoClient


# MONGO_URL = os.getenv("MONGO_MITM_URI", "mongodb://root:rootpassword@host.docker.internal:27017")
MONGO_URL = os.getenv("MONGO_MITM_URI", "mongodb://host.docker.internal:27017")

dbclient = MongoClient(MONGO_URL)

def get_map_local():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["map_local"].find()

    for temporary_mapping in temporary_mapping_data:
        # ctx.log.info(temporary_mapping)
        if temporary_mapping["enabled"] and temporary_mapping["rule"]:
            temporary_mapping["rule"] = temporary_mapping["rule"] + "|" + temporary_mapping["file_path"]
            # remove path from temporary_mapping
            new_list.append(temporary_mapping)

    return new_list


def get_map_remote():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["map_remote"].find()

    for temporary_mapping in temporary_mapping_data:
        if temporary_mapping["enabled"] and temporary_mapping["rule"]:
            new_list.append(temporary_mapping)

    return new_list


def get_url_redirect():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["url_redirect"].find()

    for temporary_mapping in temporary_mapping_data:
        if temporary_mapping["enabled"] and temporary_mapping["rule"]:
            new_list.append(temporary_mapping)

    return new_list

def get_rewrite():
    new_list=[]
    temporary_mapping_data = dbclient["mitm"]["rewrite"].find()

    for temporary_mapping in temporary_mapping_data:
        if temporary_mapping["enabled"] and temporary_mapping["location"]:
            new_list.append(temporary_mapping)

    return new_list