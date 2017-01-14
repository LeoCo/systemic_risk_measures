import pandas as pd
import numpy as np

df = pd.read_csv('Data/ACA/datas.csv', sep=';', decimal=',', parse_dates=[0])

print(df.head())

print(type(df.Date[1]))

print(type(df.FNCL_LVRG[1]))

df2 = pd.read_csv('Data/ACA/prices.csv', sep=';', decimal=',', parse_dates=[0])

print(df2.head())

with open('Data/ACA/name.txt') as f:
    data = f.read().splitlines()

print(data)