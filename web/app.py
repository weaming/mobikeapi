# coding: utf-8
from pprint import pprint
from datetime import datetime as dt
import json

from flask import Flask, redirect, request, jsonify, render_template
import pymongo
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.mobike
bikes = db.bikes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bikes')
def get_bikes():
    locations = []
    d = dt(2017, 4, 22, 20, 30)
    condition = {'datetime': {'$gt': d}}
    xx = request.args.get('lng')
    yy = request.args.get('lat')
    if xx and yy:
        xx = float(xx)
        yy = float(yy)
        offsetX = 0.02
        offsetY = 0.02
        condition.update({
            'distX': {'$gt': xx-offsetX, '$lt': xx+offsetX},
            'distY': {'$gt': yy-offsetY, '$lt': yy+offsetY},
        })
    distIDs = set()
    for obj in bikes.find(condition).limit(10000):
        if obj['distId'] not in distIDs:
            distIDs.add(obj['distId'])

            info = {}
            locations.append(info)
            for k in ('biketype', 'distId', 'distY', 'distX', 'datetime'):
                if k in obj:
                    info[k] = obj[k]

    resp = jsonify(locations)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
