import os
import pandas as pd
from bank import Bank, compute_yealds, compute_mva

def get_banks_data():
    list_of_banks = []

    #Creo un covertitore di date
    dateparser1 = lambda x: pd.datetime.strptime(x, '%d/%m/%y')
    dateparser2 = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

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
            bank.datas = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0], date_parser=dateparser1)

            # Aggiungo il file prices.csv
            filename = 'Data/' + x + '/prices.csv'
            bank.prices = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0], date_parser=dateparser1)

            #Creo la lista dei rendimenti se non esiste e la carico
            #altrimenti carico direttamente i rendimenti
            filename = 'Data/' + x + '/yealds.csv'
            if os.path.exists(filename):
                bank.yealds = pd.read_csv(filename, parse_dates=[0], date_parser=dateparser2) #carica il file
            else:
                bank.yealds = compute_yealds(bank)
                bank.yealds.to_csv(filename,index=False)

            #Creo MVA
            #Se esiste lo carico
            filename = 'Data/' + x + '/mva.csv'
            if os.path.exists(filename):
                bank.mva = pd.read_csv(filename)  # carica il file
            else:
                bank.mva = compute_mva(bank)
                bank.mva.to_csv(filename, index=False)



            #Aggiungo l'oggetto banca alla lista di banche
            list_of_banks.append(bank)

    return list_of_banks

def get_states_variable():

    #Creo un covertitore di date
    dateparser1 = lambda x: pd.datetime.strptime(x, '%d/%m/%y')

    filename = 'statesvariables.csv'
    states_variable = pd.read_csv(filename, sep=';', decimal=',', parse_dates=[0], date_parser=dateparser1)

    return states_variable
