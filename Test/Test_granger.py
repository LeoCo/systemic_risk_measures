import pandas as pd
import bank
from getdata import get_banks_data

if __name__ == '__main__':

    banks = get_banks_data()

    yealds1 = bank.find_ticker_in_list('ACA:FP',banks).yealds

    yealds2 = bank.find_ticker_in_list('AKTAV:FH',banks).yealds

    yeald_inner_join = pd.merge(yealds1, yealds2, on='Date', how='inner')

    print(yeald_inner_join[['Yeald_x','Yeald_y']])

    print(yeald_inner_join.head())
    print(yeald_inner_join.tail())

    date_start = "2010-1-10"
    date_end = "2011-1-1"

    mask = (yeald_inner_join['Date'] > date_start) & (yeald_inner_join['Date'] <= date_end)
    yeald_inner_join = yeald_inner_join.loc[mask]

    print(yeald_inner_join.head())