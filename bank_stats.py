from getdata import get_banks_data
import pandas as pd
from pandas import ExcelWriter

banks = get_banks_data()

stats = pd.DataFrame(columns=('Ticker',
                              'Leverage Mean',
                              'Leverage STD',
                              'Market Cap Mean',
                              'Market Cap STD',
                              'MVA Mean',
                              'MVA Std',
                              'Delta MVA Mean',
                              'Delta MVA Std'))

for i in range(len(banks)):

    datas = banks[i].datas

    datas['Quarter'] = datas['Date'].dt.quarter

    datas['Year'] = datas['Date'].dt.year

    mva = datas.groupby(['Year', 'Quarter'], as_index=False).mean()

    mva['MVA'] = mva['FNCL_LVRG'] * mva['HISTORICAL_MARKET_CAP']

    previous_mva = mva.loc[0, 'MVA']

    for x in range(1, len(mva)):
        current_mva = mva.loc[x, 'MVA']

        mva.loc[x, 'DELTA_MVA'] = (current_mva - previous_mva) / previous_mva

        previous_mva = current_mva

    mva = mva.loc[1:, :]

    stats.loc[i] = [banks[i].ticker,
                    mva["FNCL_LVRG"].mean(),
                    mva["FNCL_LVRG"].std(),
                    mva["HISTORICAL_MARKET_CAP"].mean(),
                    mva["HISTORICAL_MARKET_CAP"].std(),
                    mva["MVA"].mean(),
                    mva["MVA"].std(),
                    mva["DELTA_MVA"].mean(),
                    mva["DELTA_MVA"].std()]

print(stats)

writer = ExcelWriter('Bank_Stats.xlsx')
stats.to_excel(writer,'Sheet1')
writer.save()