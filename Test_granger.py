import pandas as pd
import bank
from getdata import get_banks_data

if __name__ == '__main__':

    banks = get_banks_data()

    yealds1 = bank.find_ticker_in_list('ACA:FP',banks).yealds

    yealds2 = bank.find_ticker_in_list('AKTAV:FH',banks).yealds

    yeald_inner_join = pd.merge(yealds1, yealds2, on='Date', how='inner')

    print(yeald_inner_join[['Yeald_x','Yeald_y']])