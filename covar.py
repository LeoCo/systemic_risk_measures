from getdata import get_banks_data
import pandas as pd
import numpy as np
import time


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    print("Get data time: " + str(time.clock() - start))

    year_start = 2000
    year_end = 2015


    portfolio_system_return = pd.DataFrame(columns=['Year','Quarter','PSR'])

    for year in range(year_start,year_end+1):
        for quarter in range(1,5):

            numerator = 0

            denominator = 0

            for bank in banks:

                mask = (bank.mva['Year'] == year) & (bank.mva['Quarter'] == quarter)

                delta_mva = 0
                mva = 0

                if bank.mva[mask].empty:
                    mva = 0
                    delta_mva = 0
                else:
                    mva = np.float64(bank.mva['MVA'][mask])
                    delta_mva = np.float64(bank.mva['DELTA_MVA'][mask])

                numerator += mva * delta_mva

                denominator += mva



            current_portfolio_system_return = numerator / denominator

            entry = pd.Series([year, quarter, current_portfolio_system_return], index=['Year','Quarter','PSR'])
            portfolio_system_return = portfolio_system_return.append(entry, ignore_index=True)

    print(portfolio_system_return)

    # Calcolo i B di Xsys = a + B * X

    # Preparo il vettore y e la matrice X
    year_from = 2010
    year_to = 2012

    mask = (portfolio_system_return['Year'] >= year_from) & (portfolio_system_return['Year'] <= year_to)
    y = portfolio_system_return['PSR'][mask]
    y.reset_index(drop=True, inplace=True)
    y.name = 'PSR'

    X = pd.DataFrame()

    for b in banks:
        mask = (b.mva['Year'] >= year_from) & (b.mva['Year'] <= year_to)
        s = b.mva.loc[mask,'DELTA_MVA']
        s.reset_index(drop=True, inplace=True)
        s.name = b.ticker
        X.reset_index(drop=True, inplace=True)
        X = pd.concat([X, s],axis=1)

    print(y)
    print(X)

    # Eseguo la quantile regression



    run_time = time.clock() - start

    print("Execution time: " + str(run_time))

