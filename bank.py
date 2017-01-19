import pandas as pd


class Bank(object):

    def __init__(self, name='', ticker='', datas=pd.DataFrame(),prices=pd.DataFrame()):
        self.name = name
        self.ticker = ticker
        self.datas = datas
        self.prices = prices

def compute_yealds(bank):


    # Creo un df per i rendimenti

    dates = bank.prices['Date'][1:]
    columns = ['Date', 'Yeald']
    yealds = pd.DataFrame(dates, columns=columns)


    # Calcolo i rendimenti

    price_yesterday = bank.prices['PX_LAST'][0]

    price_today = 0

    for i in range(0, len(yealds)):
        price_today = bank.prices['PX_LAST'][i + 1]

        yeald = (price_today - price_yesterday) / price_yesterday

        yealds.loc[i + 1, 'Yeald'] = yeald

        price_yesterday = price_today


    return yealds

def compute_mva(bank):

    datas = bank.datas

    datas['Quarter'] = datas['Date'].dt.quarter

    datas['Year'] = datas['Date'].dt.year

    mva = datas.groupby(['Year', 'Quarter'], as_index=False).mean()

    mva['MVA'] = mva['FNCL_LVRG'] * mva['HISTORICAL_MARKET_CAP']

    mva = mva[['Year', 'Quarter', 'MVA']]

    previous_mva = mva.loc[0, 'MVA']

    for x in range(1, len(mva)):
        current_mva = mva.loc[x, 'MVA']

        mva.loc[x, 'DELTA_MVA'] = (current_mva - previous_mva) / previous_mva

        previous_mva = current_mva

    mva = mva.loc[1:, :]

    return mva

def find_ticker_in_list(bank_ticker, list_of_banks):
    for x in list_of_banks:
        if x.ticker == bank_ticker:
            return x

def find_name_in_list(bank_name, list_of_banks):
    for x in list_of_banks:
        if x.name == bank_name:
            return x