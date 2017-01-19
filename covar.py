from getdata import get_banks_data
import pandas as pd
import time


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    bank = banks[0]

    print(bank.mva)

    print("Get data time: " + str(time.clock() - start))

    run_time = time.clock() - start

    print("Execution time: " + str(run_time))