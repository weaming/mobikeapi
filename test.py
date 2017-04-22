# coding: utf-8
from mobikeapi import API
from pprint import pprint
from datetime import datetime as dt

import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.mobike
bikes = db.bikes

def save_json(js):
    js.update(datetime = dt.now())
    obj = bikes.insert_one(js)
    print obj.inserted_id

def process_response(js):
    if js:
        save_json(js)

api = API('')
test = 0

if test:
    print api.getridestate()
    #print api.nearby_bikes_info()
else:
    for x in api.scan_region():
        process_response(x)
