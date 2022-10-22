import pandas as pd

import random
import os
from datetime import timedelta, datetime


def get_flights_table():
    path = 'data/Рейсы, пассажиры.xlsx'
    if os.path.exists(path):
        excel_data = pd.read_excel(path)
    else:
        raise FileNotFoundError(f'Exception from file {__file__}: No such file or directory {path}.')

    excel_data['Дата'] = pd.to_datetime(excel_data['Дата'], infer_datetime_format=True)

    excel_data['Дата и время'] = excel_data.apply(lambda row: datetime.combine(row['Дата'], row['Плановое время']), axis=1)
    excel_data['Дата и время'] = excel_data['Дата и время'].map(lambda x: x + timedelta(minutes=random.randint(-20,45)))

    excel_data['Дата'] = excel_data['Дата и время'].dt.date
    excel_data['Плановое время'] = excel_data['Дата и время'].dt.time

    excel_data = excel_data.sort_values(by = 'Дата и время')
    
    return excel_data.drop(columns=['Дата и время']).to_excel("output.xlsx", index=False)
