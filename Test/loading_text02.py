import os
import pandas as pd
from bank import Bank

print(os.listdir('./Data'))

banca = Bank("nome", "AAA")

print(banca.ticker)

list_of_banks = []

for x in os.listdir('./Data'):

    #Evito di importare cartelle di sistema
    if x[0] != '.':

        #Creo un nuovo oggetto banca
        bank = Bank(x)

        #Carico il nome ed il ticker
        filename = 'Data/' + x + '/name.txt'
        with open(filename) as f:
            name_ticker = f.read().splitlines()

        #Aggiungo nome e ticker
        bank.name = name_ticker[0]
        bank.ticker = name_ticker[1]

        #Aggiungo il file datas.csv
        filename = 'Data/' + x + '/datas.csv'
        bank.datas = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0])

        # Aggiungo il file prices.csv
        filename = 'Data/' + x + '/prices.csv'
        bank.prices = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0])

        #Aggiungo l'oggetto banca alla lista di banche
        list_of_banks.append(bank)

print(list_of_banks)

for x in list_of_banks:
    print(x.name)
    print(x.ticker)
    print(x.prices.head())
