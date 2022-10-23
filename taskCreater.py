from cgi import print_form
from csv import excel
import json
from numpy import int64
import pandas as pd
import requests

import random
import os
from datetime import timedelta, datetime

port = 8888

__excel_data : pd.DataFrame

def phonk(row):
    timestamp = row['Дата и время']
    typeS = row['AD (A-прилет, D-вылет)']
    parking = row['Номер места стоянки']
    gate = row['Номер гейта']
    passangers = row['Количество пассажиров']
    
    requests.get("http://localhost:{}/getTask?time={}&typeS={}&parking={}&gate={}&pass={}".format(port ,timestamp, typeS, parking, gate, passangers)) 

def get_next_flight(data):
    global __excel_data
    timestamp = int(data.get('model-time'))
    next_flight = __excel_data.where(__excel_data['Дата и время'] <= timestamp + 3600) 
    next_flight = next_flight.dropna()
    idx = next_flight.index
    __excel_data = __excel_data.drop(index=idx)
    js = next_flight.to_json(orient='records')
    parsed = json.loads(js)
    next_flight.apply(phonk, axis=1)
    return 200

def init(path):
    global __excel_data
    if os.path.exists(path):
        __excel_data = pd.read_excel(path)
    else:
        raise FileNotFoundError(f'Exception from file {__file__}: No such file or directory {path}.')

    __excel_data['Дата и время']
    __excel_data['Дата и время'] = (pd.to_numeric(__excel_data['Дата и время'].values) / 10 ** 9).astype(int64)
    __excel_data['Дата и время'] = __excel_data[__excel_data['AD (A-прилет, D-вылет)'] == 'D']['Дата и время'] - 1800

