import pandas as pd
import random
import bank
from getdata import get_banks_data


def granger_casualties(banks):
    banks_name = []

    #Creo la matrice delle correlazioni
    for x in banks:
        banks_name.append(x.ticker)

    corr_matrix = pd.DataFrame(index=banks_name, columns=banks_name)

    for x in corr_matrix.columns:
        for y in corr_matrix.index:

            bank_a = bank.find_ticker_in_list(x,banks)
            bank_b = bank.find_ticker_in_list(y,banks)

            corr_matrix.loc[x,y] = correlation_a_granger_caused_by_b(bank_a,bank_b)


    return corr_matrix

def correlation_a_granger_caused_by_b(a,b):

    influenced = 0



    return influenced

if __name__ == '__main__':

    banks = get_banks_data()

    granger_matrix = granger_casualties(banks)

    print(granger_matrix)