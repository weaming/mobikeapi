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
    for obj in bikes.find():
        info = {}
        locations.append(info)
        for k in ('type', 'distId', 'distY', 'distX'):
            if k in obj:
                info[k] = obj[k]

    resp = jsonify(locations)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
