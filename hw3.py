# Use dataset: https://www.kaggle.com/datasets/ruchikakumbhar/power-consumption-prediction-dataset This dataset is
# related to power consumption of three different distribution networks of Tetouan city which is located in north
# Morocco.

from hw2_modules import (DataLoader, EdaAnalyze)
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

data_load = DataLoader('./power_consumption_data/power_consumption.csv', 'csv')
dataset = data_load.get_data()  # load the data into a Pandas DataFrame
pcom = EdaAnalyze(dataset)
print('************************************')
print('power consumption dataset info')
print(pcom.info())
print('************************************')

con = sqlite3.connect('pcom.db')
cursor = con.cursor()
table_name = 'power_consumption'

key_create_db = False
key_convert_data = False

if key_create_db:
    # Create Table in DB
    request = f"""CREATE TABLE IF NOT EXISTS {table_name}
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                DateTime DATETIME, 
                Temperature REAL,
                Humidity REAL,
                Wind_Speed REAL,
                general_diffuse_flows REAL,
                diffuse_flows REAL,
                Zone_1 REAL,
                Zone_2 REAL,
                Zone_3 REAL                                                                                                
                )
            """
    cursor.execute(request)

if key_convert_data:
    # convert the DataFrame data to a sqlite table
    dataset.to_sql(table_name, con, if_exists='fail', index=True, index_label='id')

request_select = f'SELECT * FROM {table_name} WHERE `DateTime` < "01-01-2017 06:10" AND `Humidity` > 78'

date_select = cursor.execute(request_select).fetchall()
print(request_select)
for item in date_select:
    print(item)
print('************************************')

request_select = f'SELECT AVG(Humidity) FROM {table_name}'
date_select = cursor.execute(request_select).fetchone()
print(request_select, ': ', date_select[0])
request_select = f'SELECT AVG(Zone_1) FROM {table_name}'
date_select = cursor.execute(request_select).fetchone()
print(request_select, ': ', date_select[0])
print('************************************')

request_select = f'SELECT ROUND(SUM(Zone_2),2) FROM {table_name} WHERE `DateTime` > "12-01-2017 00:01" AND `Wind_Speed` < 0.071'
date_select = cursor.execute(request_select).fetchone()
print(request_select, ': ', date_select[0])
print('************************************')

request_select = f'SELECT COUNT(*) FROM {table_name} WHERE `DateTime` > "12-01-2017 00:01" AND `Wind_Speed` < 0.071'
date_select = cursor.execute(request_select).fetchone()
print(request_select, ': ', date_select[0])
print('************************************')

request_select = f'SELECT ROUND(Temperature,0), COUNT(*) FROM {table_name} GROUP BY ROUND(Temperature,0)'
date_select = cursor.execute(request_select).fetchall()
print(request_select)
for item in date_select:
    print(item)
print('************************************')

# read from DB to pandas DataFrame

request_select = f'SELECT * FROM {table_name}'
pcd_sql = pd.read_sql(request_select, con)

pcd_sql.info()
pcd_sql.head()

# Convert DataTime to datatime format
pcd_sql['DateTime'] = pd.to_datetime(pcd_sql['DateTime'], format='mixed', errors='coerce')


def parse_datetime(x):
    try:
        return pd.to_datetime(x)
    except:
        for fmt in ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']:
            try:
                return pd.to_datetime(x, format=fmt)
            except:
                continue
    return pd.NaT


pcd_sql['DateTime'] = pcd_sql['DateTime'].apply(parse_datetime)
pcd_sql.head()


# Visualisation

def zone(dataframe_obj: DataFrame, zone_name: str):
    plt.figure(figsize=(15, 8))

    daily_avg = dataframe_obj.resample('D', on='DateTime')[zone_name].mean()

    plt.plot(daily_avg.index, daily_avg.values, color='#2196F3', label='Daily Average', linewidth=1)

    rolling_avg = daily_avg.rolling(window=7).mean()
    plt.plot(rolling_avg.index, rolling_avg.values, color='#E91E63',
             label='7-day Rolling Average', linewidth=2)

    # Customize the plot
    plt.title(f'Power Consumption Over Time - {zone_name}', fontsize=12, pad=15)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Power Consumption', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    plt.show()


zone(pcd_sql, 'Zone_1')
zone(pcd_sql, 'Zone_2')
zone(pcd_sql, 'Zone_3')


def zone_compare(dataframe_obj: DataFrame):
    plt.figure(figsize=(15, 8))

    daily_avg1 = dataframe_obj.resample('D', on='DateTime')['Zone_1'].mean()
    daily_avg2 = dataframe_obj.resample('D', on='DateTime')['Zone_2'].mean()
    daily_avg3 = dataframe_obj.resample('D', on='DateTime')['Zone_3'].mean()

    # plt.plot(daily_avg.index, daily_avg.values, color='#2196F3', label='Daily Average', linewidth=1)

    rolling_avg1 = daily_avg1.rolling(window=7).mean()
    plt.plot(rolling_avg1.index, rolling_avg1.values, color='#2196F3',
             label='7-day Rolling Average Zone 1', linewidth=2)
    rolling_avg2 = daily_avg2.rolling(window=7).mean()
    plt.plot(rolling_avg2.index, rolling_avg2.values, color='#E9FF63',
             label='7-day Rolling Average Zone 2', linewidth=2)
    rolling_avg3 = daily_avg3.rolling(window=7).mean()
    plt.plot(rolling_avg3.index, rolling_avg3.values, color='#E91EFF',
             label='7-day Rolling Average Zone 3', linewidth=2)

    # Customize the plot
    plt.title('Power Consumption Over Time - 3 Zones', fontsize=12, pad=15)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Power Consumption', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    plt.show()


zone_compare(pcd_sql)


# Temperature vs Power Consumption

def temp(dataframe_obj: DataFrame):
    plt.figure(figsize=(20, 6))

    # Zone 1
    plt.subplot(1, 3, 1)
    plt.hexbin(dataframe_obj['Temperature'], dataframe_obj['Zone_1'],
               gridsize=30, cmap='YlOrRd',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Temperature')
    plt.ylabel('Zone 1')
    plt.title(f'Temperature vs Power Consumption\nZone 1')

    # Zone 2
    plt.subplot(1, 3, 2)
    plt.hexbin(dataframe_obj['Temperature'], dataframe_obj['Zone_2'],
               gridsize=30, cmap='YlOrRd',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Temperature')
    plt.ylabel('Zone 2')
    plt.title(f'Temperature vs Power Consumption\nZone 2')

    # Zone 3
    plt.subplot(1, 3, 3)
    plt.hexbin(dataframe_obj['Temperature'], dataframe_obj['Zone_3'],
               gridsize=30, cmap='YlOrRd',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Temperature')
    plt.ylabel('Zone 3')
    plt.title(f'Temperature vs Power Consumption\nZone 3')

    plt.tight_layout()
    plt.show()


temp(pcd_sql)


# Humidity vs Power Consumption

def humid(dataframe_obj: DataFrame):
    plt.figure(figsize=(20, 6))

    # Zone 1
    plt.subplot(1, 3, 1)
    plt.hexbin(dataframe_obj['Humidity'], dataframe_obj['Zone_1'],
               gridsize=30, cmap='Spectral',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Humidity')
    plt.ylabel('Zone 1')
    plt.title(f'Humidity vs Power Consumption\nZone 1')

    # Zone 2
    plt.subplot(1, 3, 2)
    plt.hexbin(dataframe_obj['Humidity'], dataframe_obj['Zone_2'],
               gridsize=30, cmap='Spectral',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Humidity')
    plt.ylabel('Zone 2')
    plt.title(f'Humidity vs Power Consumption\nZone 2')

    # Zone 3
    plt.subplot(1, 3, 3)
    plt.hexbin(dataframe_obj['Humidity'], dataframe_obj['Zone_3'],
               gridsize=30, cmap='Spectral',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Humidity')
    plt.ylabel('Zone 3')
    plt.title(f'Humidity vs Power Consumption\nZone 3')

    plt.tight_layout()
    plt.show()


humid(pcd_sql)


# Wind Speed vs Power Consumption

def wind(dataframe_obj: DataFrame):
    plt.figure(figsize=(20, 6))

    # Zone 1
    plt.subplot(1, 3, 1)
    plt.hexbin(dataframe_obj['Wind_Speed'], dataframe_obj['Zone_1'],
               gridsize=30, cmap='coolwarm',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Wind Speed')
    plt.ylabel('Zone 1')
    plt.title(f'Humidity vs Power Consumption\nZone 1')

    # Zone 2
    plt.subplot(1, 3, 2)
    plt.hexbin(dataframe_obj['Wind_Speed'], dataframe_obj['Zone_2'],
               gridsize=30, cmap='coolwarm',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Wind Speed')
    plt.ylabel('Zone 2')
    plt.title(f'Wind Speed vs Power Consumption\nZone 2')

    # Zone 3
    plt.subplot(1, 3, 3)
    plt.hexbin(dataframe_obj['Wind_Speed'], dataframe_obj['Zone_3'],
               gridsize=30, cmap='coolwarm',
               mincnt=1)
    plt.colorbar(label='Count')
    plt.xlabel('Wind Speed')
    plt.ylabel('Zone 3')
    plt.title(f'Wind Speed vs Power Consumption\nZone 3')

    plt.tight_layout()
    plt.show()


wind(pcd_sql)


# Correlation Heatmap

def correlation_heatmap(dataframe_obj: DataFrame):
    plt.figure(figsize=(10, 8))
    correlation_vars = ['Temperature', 'Humidity', 'Wind_Speed',
                        'Zone_1', 'Zone_2', 'Zone_3']
    correlation_matrix = dataframe_obj[correlation_vars].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()


correlation_heatmap(pcd_sql)
