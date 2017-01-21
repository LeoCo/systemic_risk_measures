from getdata import get_banks_data
import pandas as pd
import time
import statsmodels.api as sm

def ses(bank, date_start, date_end):

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


if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    date_start = '2006-9-15'
    date_end = '2008-9-15'

    data_matrix = pd.DataFrame(columns=['Ticker', 'RSES', 'MES', 'LVR'])

    for b in banks:

        #Controllo se ci siano i prezzi delle azioni
        mask = (b.prices['Date'] >= date_start) & (b.prices['Date'] <= date_end)
        prices = b.prices.loc[mask]['PX_LAST']

        condition = not prices.dropna().empty

        if condition:

            rses = 0
            mes = 0
            lvr = 0

            #Calcolo RSES
            mask = (b.prices['Date'] >= date_start) & (b.prices['Date'] <= date_end)
            prices = b.prices.loc[mask]['PX_LAST']

            prices_first = prices.iloc[0]
            prices_last = prices.iloc[-1]

            rses = (prices_last - prices_first) / prices_first

            #Calcolo il mes
            mask = (b.yealds['Date'] >= date_start) & (b.yealds['Date'] <= date_end)
            yealds = b.yealds.loc[mask]

            percentile = yealds['Yeald'].quantile(q=0.05)

            yeald_percentile = yealds['Yeald'][yealds['Yeald'] <= percentile]

            yeald_percentile.reset_index(drop=True, inplace=True)

            mes = yeald_percentile.mean()

            #Calcolo il LVR medio
            mask = (b.datas['Date'] >= date_start) & (b.datas['Date'] <= date_end)
            leverage = b.datas.loc[mask]['FNCL_LVRG']

            leverage.reset_index(drop=True, inplace=True)

            lvr = leverage.mean()


            data_matrix = data_matrix.append({'Ticker': b.ticker,
                                                'RSES': rses,
                                                'MES': mes,
                                                'LVR': lvr}, ignore_index=True)


    #Effettuo la regressione per calcolare ses
    y = data_matrix['RSES']
    X = data_matrix[['MES', 'LVR']]

    model = sm.OLS(y, X)
    results = model.fit()

    #Parametri risultato regressione
    #print(results.summary())

    ses = pd.Series(results.predict(X),name='SES')

    #Aggiungo ses alla matrice dei dati
    data_matrix = pd.concat([data_matrix, ses], axis=1)

    print(data_matrix)

