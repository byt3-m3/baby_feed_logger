from flask import Flask, jsonify, render_template, request, url_for, redirect, Response
import re
import os
import sys
import mongoengine
import datetime
import time
import bson
import json
from marshmallow import Schema, fields
import requests

app = Flask(__name__)

JSON_RESPONSE_HEADERS = {'content-type': 'application/json; charset=utf-8'}


def connect_mongoengine():
    mongoengine.connect("milk_log_dev", host="192.168.1.182", port=27017)


class Log(mongoengine.Document):
    timeStamp = mongoengine.StringField()
    milkUsed = mongoengine.StringField()


class LogNew(mongoengine.Document):
    milkUsed = mongoengine.StringField()
    timeStr = mongoengine.StringField()
    dateStr = mongoengine.StringField()
    timeStamp = mongoengine.DateTimeField(default=datetime.datetime.now())
    todayStamp = mongoengine.DateTimeField(default=datetime.date.today())


@app.route("/")
def baby_formula_log():
    results = LogNew.objects()
    dict_logs = []
    total = 0

    for log in results:
        data = json.loads(log.to_json())

        dict_logs.append(data)

        if data['milkUsed']:
            total += int(data['milkUsed'])

    return render_template("index.j2", logs=dict_logs, total=total)


@app.route("/log", methods=['POST', 'GET'])
def log_milk():
    timeStamp = datetime.datetime.now()

    date = timeStamp.strftime("%d-%m")
    time = timeStamp.strftime("%H:%M")

    form_data = request.form

    log_new = {
        "milkUsed": form_data.get("milk_amount"),
        "dateStr": date,
        "timeStr": time
    }

    res = LogNew.from_json(json.dumps(log_new))

    res.save()

    return redirect('/')


@app.route("/delete_log", methods=['POST'])
def delete_log():
    data = request.json
    _id = data['id']

    result = LogNew.objects(id=_id).first()
    result.delete()

    return jsonify({"status": True})


@app.route("/api/v1/logs", methods=['POST'])
def post_logs():
    data = request.json
    REQ_DATE = data.get("date")
    REQ_TIME = data.get("time")
    REQ_FED = data.get("fed")

    HOUR = int(REQ_TIME[:2])
    MIN = int(REQ_TIME[3:])

    YEAR = int(REQ_DATE[:4])
    DAY = int(REQ_DATE[5:7])
    MONTH = int(REQ_DATE[8:10])

    log = LogNew.objects(id=data.get("id")).first()

    date_obj = datetime.datetime(YEAR, MONTH, DAY)

    time_obj = datetime.time(HOUR, MIN)

    datetime_obj = datetime.datetime.combine(date_obj, time_obj)

    log.timeStamp = datetime_obj
    log.dateStr = f"{REQ_DATE[5:7]}-{REQ_DATE[8:10]}"
    log.milkUsed = REQ_FED
    log.timeStr = REQ_TIME

    log.save()

    return jsonify({})


@app.route("/api/v1/log/<_id>", methods=['GET'])
def get_log(_id):
    b_id = bson.objectid.ObjectId(_id)
    resp = {}
    try:
        results = LogNew.objects(id=b_id).first()

        resp['log'] = json.loads(results.to_json())
        return jsonify(resp)
    except Exception:
        return jsonify(resp)


@app.route("/api/v1/logs", methods=['GET'])
def get_logs():
    resp = {}

    results = LogNew.objects()

    dict_logs = []
    total = 0

    for log in results:
        data = json.loads(log.to_json())

        dict_logs.append(data)
        total += int(data['milkUsed'])

    resp['total'] = total
    resp['results'] = dict_logs

    return jsonify(resp)


@app.route("/api/v1/feed/estimate", methods=['GET'])
def calculate_next_feed():
    delta = datetime.timedelta(hours=2)

    resp = {}

    res = LogNew.objects().order_by('-timeStamp').first()

    dif = res.timeStamp + delta

    resp['estimated_feeding_time'] = dif.strftime('%H:%M')

    return jsonify(resp)
