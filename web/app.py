# coding: utf-8
from pprint import pprint
from datetime import datetime
from datetime import timedelta
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

@app.route('/all')
def all_bikes():
    return render_template('all.html')

@app.route('/api/bikes')
def get_bikes():
    d = datetime.now()
    d = d - timedelta(hours=3)
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

    locations = {}
    repeated = 0
    if request.args.get('count'):
        for obj in bikes.find(condition):
            if obj['distId'] not in locations:
                locations[obj['distId']] = 1
            else:
                locations[obj['distId']] += 1
        resp = jsonify(count=len(locations), repeated=sum(locations.values())-len(locations))
    else:
        for obj in bikes.find(condition).limit(30000):
            if obj['distId'] not in locations:
                locations[obj['distId']] = info = {}
                for k in ('biketype', 'distId', 'distY', 'distX', 'datetime'):
                    if k in obj:
                        info[k] = obj[k]
            else:
                repeated += 1

        print(len(locations), repeated)
        resp = jsonify(locations.values())

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
