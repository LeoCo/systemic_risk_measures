from getdata import get_banks_data
import pandas as pd
import time


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    bank = banks[0]

    print(bank.mva)

    print("Get data time: " + str(time.clock() - start))

    year_start = 2006
    quarter_start = 0

    year_end = 2009
    quarter_end = 4

    portfolio_system_return = pd.DataFrame(columns=['Year','Quarter','PSR'])

    for year in range(year_start,year_end):
        for quarter in range(quarter_start,quarter_end):


            entry = pd.Series([2001, 1, 50])
            #portfolio_system_return.append([2001, 1, 50])

    print(portfolio_system_return)



    run_time = time.clock() - start

    print("Execution time: " + str(run_time))