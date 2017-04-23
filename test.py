# coding: utf-8
from pprint import pprint
from datetime import datetime as dt
import json
from mobikeapi import API

import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.mobike
bikes = db.bikes1
saved_bikes = set()

def save_json(js):
    base = {'datetime': dt.now()}
    try:
        for obj in js['object']:
            if obj['distId'] not in saved_bikes:
                obj['location'] = point([obj['distX'], obj['distY']])
                obj.update(base)
                saved_bikes.add(obj['distId'])
                obj = bikes.insert_one(obj)
                print obj.inserted_id
    except Exception as e:
        print(e)

def process_response(js):
    if js and 'object' in js:
        save_json(js)

def point(loc):
    return {
        'type': "Point",
        'coordinates': loc,
    }

# 填入手机号
api = API('')
case = 1

if case == 0:
    print api.getridestate()
    #print api.nearby_bikes_info()
elif case == 1:
    for x in api.scan_region():
        process_response(x)
