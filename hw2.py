from hw2_modules import (DataLoader, EdaAnalyze)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
import time

dataload = DataLoader('./anxiety_attack_data/anxiety_attack_dataset_broken.csv', 'csv')
dataset = dataload.get_data()
aad = EdaAnalyze(dataset)
print('************************************')
print('Anxiety Attack dataset info')
print(aad.info())
print('************************************')
print('Anxiety Attack dataset header')
print(aad.head_list())
print('************************************')
print('Anxiety Attack dataset missing values')
print(aad.missing_value_report())
print('************************************')
print('Anxiety Attack dataset show selected distributions')
aad.show_select_distributions('Age', 'Gender', 'Sleep Hours', 'Physical Activity (hrs/week)')  # comment this if start script with text terminal
print('************************************')
print('Anxiety Attack dataset pie distribution')
aad.draw_pie_distribution('Occupation')   # comment this if start script with text terminal
print('************************************')
print('Anxiety Attack dataset filling missed values')
aad.filling_missing_values('mean', 'Therapy Sessions (per month)', True, './anxiety_attack_data/anxiety_attack_dataset_recovery.csv')
time.sleep(3)
dataload_recovery = DataLoader('./anxiety_attack_data/anxiety_attack_dataset_recovery.csv', 'csv')
dataset_recovery = dataload_recovery.get_data()
aad_recovery = EdaAnalyze(dataset_recovery)
print('************************************')
print('Anxiety Attack dataset with recovered values')
print(aad_recovery.missing_value_report())
