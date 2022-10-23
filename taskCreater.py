from cgi import print_form
from csv import excel
from numpy import int64
import pandas as pd
import requests

import random
import os
from datetime import timedelta, datetime

port = 3332

__excel_data : pd.DataFrame

def get_next_flight(data):
    global __excel_data
    timestamp = int(data.get('model-time'))
    next_flight = __excel_data.where(__excel_data['Дата и время'] <= timestamp + 3600) 
    next_flight = next_flight.dropna()
    idx = next_flight.index
    __excel_data = __excel_data.drop(index=idx)
    #requests.get("http://localhost:%d/ready-for-event?service_id=%s" % (port, __excel_data.to_dict('recodrs'))) допилить
    return 200

def init(path):
    global __excel_data
    if os.path.exists(path):
        __excel_data = pd.read_excel(path)
    else:
        raise FileNotFoundError(f'Exception from file {__file__}: No such file or directory {path}.')

    __excel_data['Дата и время']
    __excel_data['Дата и время'] = (pd.to_numeric(__excel_data['Дата и время'].values) / 10 ** 9).astype(int64)

