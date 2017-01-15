import os
import pandas as pd
from bank import Bank, compute_yealds

def get_banks_data():
    list_of_banks = []

    #Creo un covertitore di date
    dateparser = lambda x: pd.datetime.strptime(x, '%d/%m/%y')

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

            # Aggiungo il file datas.csv
            filename = 'Data/' + x + '/datas.csv'
            bank.datas = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0],date_parser=dateparser)

            # Aggiungo il file prices.csv
            filename = 'Data/' + x + '/prices.csv'
            bank.prices = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0],date_parser=dateparser)

            # Creo la lista dei rendimenti
            bank.yealds = compute_yealds(bank)

            #Aggiungo l'oggetto banca alla lista di banche
            list_of_banks.append(bank)

    return list_of_banks
