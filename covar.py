from getdata import get_banks_data
import pandas as pd
import numpy as np
import time


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    print("Get data time: " + str(time.clock() - start))

    year_start = 1997
    quarter_start = 1

    year_end = 2015
    quarter_end = 5

    portfolio_system_return = pd.DataFrame(columns=['Year','Quarter','PSR'])

    for year in range(year_start,year_end):
        for quarter in range(quarter_start,quarter_end):

            numerator = 0

            denominator = 0

            for bank in banks:

                mask = (bank.mva['Year'] == year) & (bank.mva['Quarter'] == quarter)

                #print("Bank name: " + bank.name)
                #print(bank.mva.head())
                #print(bank.mva['MVA'][mask])
                #print(bank.mva[mask].empty)
                #print('ok')

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


    run_time = time.clock() - start

    print("Execution time: " + str(run_time))

