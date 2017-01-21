from getdata import get_banks_data
import pandas as pd
import time
import statsmodels.api as sm
from bank import find_ticker_in_list

def ses(banks, date_start, date_end):

    data_matrix = pd.DataFrame(columns=['Ticker', 'RSES', 'MES', 'LVR'])

    for b in banks:

        # Controllo se ci siano i prezzi delle azioni
        mask = (b.prices['Date'] >= date_start) & (b.prices['Date'] <= date_end)
        prices = b.prices.loc[mask]['PX_LAST']

        condition = not prices.dropna().empty

        if condition:
            rses = 0
            mes = 0
            lvr = 0

            # Calcolo RSES
            mask = (b.prices['Date'] >= date_start) & (b.prices['Date'] <= date_end)
            prices = b.prices.loc[mask]['PX_LAST']

            prices_first = prices.iloc[0]
            prices_last = prices.iloc[-1]

            rses = (prices_last - prices_first) / prices_first

            # Calcolo il mes
            mask = (b.yealds['Date'] >= date_start) & (b.yealds['Date'] <= date_end)
            yealds = b.yealds.loc[mask]

            percentile = yealds['Yeald'].quantile(q=0.05)

            yeald_percentile = yealds['Yeald'][yealds['Yeald'] <= percentile]

            yeald_percentile.reset_index(drop=True, inplace=True)

            mes = yeald_percentile.mean()

            # Calcolo il LVR medio
            mask = (b.datas['Date'] >= date_start) & (b.datas['Date'] <= date_end)
            leverage = b.datas.loc[mask]['FNCL_LVRG']

            leverage.reset_index(drop=True, inplace=True)

            lvr = leverage.mean()

            data_matrix = data_matrix.append({'Ticker': b.ticker,
                                              'RSES': rses,
                                              'MES': mes,
                                              'LVR': lvr}, ignore_index=True)

    # Effettuo la regressione per calcolare ses
    y = data_matrix['RSES']
    X = data_matrix[['MES', 'LVR']]

    model = sm.OLS(y, X)
    results = model.fit()

    # Parametri risultato regressione
    # print(results.summary())

    ses = pd.Series(results.predict(X), name='SES')

    # Aggiungo ses alla matrice dei dati
    data_matrix = pd.concat([data_matrix, ses], axis=1)

    return data_matrix

def portfolio_ses(datamatrix, banks, year, quarter):

    port_ses = 0

    dm = datamatrix.copy()

    dm['Weighted'] = 0

    mva_sum = 0

    for ticker in dm['Ticker']:
        bank = find_ticker_in_list(ticker, banks)
        mask = (bank.mva['Year'] == year) & (bank.mva['Quarter'] == quarter)

        mva = float(bank.mva[mask]['MVA'])

        mva_sum += mva

        dm.loc[dm['Ticker'] == ticker, 'Weighted'] = mva * dm.loc[dm['Ticker'] == ticker, 'SES']

    port_ses = dm['Weighted'].sum() / mva_sum


    return port_ses


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    date_start = '2006-09-15'
    date_end = '2008-09-15'

    year_weight = 2008
    quarter_weight = 3

    data_matrix = ses(banks, date_start, date_end)

    port_ses = portfolio_ses(data_matrix, banks, year_weight, quarter_weight)

    print()
    print('Systemic Expected Shortfall')
    print('Portfolio ses: ' + str(port_ses))
    print()
    print(data_matrix)

    writer = pd.ExcelWriter('Output/systemic_expected_shortfall.xlsx')
    sheet_name = "SES_" + date_start + '_to_' + date_end
    data_matrix.to_excel(writer, sheet_name)
    writer.save()

    run_time = time.clock() - start

    print("Execution time: " + str(run_time))