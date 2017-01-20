from getdata import get_banks_data, get_states_variable
import matplotlib.pyplot as plt
import statsmodels.api as sm
import bank
import pandas as pd
from covar import covar, portfolio_covar

banks = get_banks_data()

for x in banks:

    #Stampa lista banche
    if False:
        print(x.name)
        print(x.ticker)
        print(x.datas.head())
        print(x.prices.head())
        print(x.yealds.head())
        print(type(x.yealds.iloc[0,0]))

    #Fa il grafico del prezzo delle azioni
    if False:
        df = x.prices
        plt.plot(df['Date'], df['PX_LAST'])
        plt.title(x.name)
        plt.xlabel('Date')
        plt.ylabel('Prices')
        plt.show()

    #Fa il grafico dei rendimenti
    if False:
        df = x.yealds
        plt.plot(df['Date'], df['Yeald'])
        plt.title(x.name)
        plt.xlabel('Date')
        plt.ylabel('Prices')
        plt.show()

    #Regressione prezzi
    if False:

        y = x.prices['PX_LAST']

        X = list(range(0,len(x.prices['PX_LAST'])))
        X = sm.add_constant(X)

        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        print()
        print('P values:')
        print(results.pvalues)

        predictions = results.predict(X)

        df = x.prices
        plt.plot(df['Date'], df['PX_LAST'], label="Sample")
        plt.plot(df['Date'], predictions, label="Prediction")
        plt.title(x.name)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Prices')
        plt.show()

    #Regressione Rendimenti
    if False:
        y = x.yealds['Yeald']

        X = list(range(0, len(x.yealds['Yeald'])))
        X = sm.add_constant(X)

        print(y)
        print(X[0])

        print(type(y))
        print(type(X[0]))

        model = sm.OLS(y.astype(float), X.astype(float))
        results = model.fit()
        print(results.summary())
        print()
        print('P values:')
        print(results.pvalues)

        predictions = results.predict(X)

        df = x.yealds
        plt.plot(df['Date'], df['Yeald'], label="Sample")
        plt.plot(df['Date'], predictions, label="Prediction")
        plt.title(x.name)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Yeald')
        plt.show()


#Testo il metodo di ricerca in lista
if False:

    x = bank.find_ticker_in_list('ACA:FP',banks)

    print(x.name)
    yealds = x.yealds
    print(yealds['Date'])

#Testo il metodo get_states_variable()
if False:

    df = get_states_variable()

    print(df.head())

if True:
    dates = [[2008,1,2010,4],
             [2008,2,2011,1],
             [2008,3,2011,2],
             [2008,4,2011,3],
             [2009,1,2011,4],
             [2009,2,2012,1],
             [2009,3,2012,2],
             [2009,4,2012,3],
             [2010,1,2012,4],
             [2010,2,2013,1],]

    banks = get_banks_data()

    porfolio_covar_unc = []
    porfolio_covar = []

    res = pd.DataFrame(columns=['Date','CovarUnc','Covar'])

    for d in dates:
        covar_unc_matrix, covar_matrix = covar(banks, d[0], d[1], d[2], d[3])

        #porfolio_covar_unc.append(portfolio_covar(covar_unc_matrix, banks, d[2], d[3]))
        #porfolio_covar.append(portfolio_covar(covar_matrix, banks, d[2], d[3]))

        res = res.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                          'CovarUnc': portfolio_covar(covar_unc_matrix, banks, d[2], d[3]),
                          'Covar': portfolio_covar(covar_matrix, banks, d[2], d[3])}, ignore_index=True)

    #print(porfolio_covar_unc)
    #print(porfolio_covar)

    print(res)

    plt.plot(res['CovarUnc'], label="Covar Unc")
    plt.plot(res['Covar'], label="Covar")
    plt.title('Portfolio Covar Trend')
    plt.xticks(list(range(0,len(res))), res['Date'])
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Covar')
    plt.show()


