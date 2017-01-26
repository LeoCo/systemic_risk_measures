from getdata import get_banks_data, get_states_variable
import matplotlib.pyplot as plt
import statsmodels.api as sm
import bank
import pandas as pd
from covar import covar, portfolio_covar
from systemic_expected_shortfall import ses, portfolio_ses
from granger_casualities import granger_casualties

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

#Plotto il grafico andamentale del portfolio covar
if False:
    dates = [[2005, 3, 2007, 2],
             [2005, 4, 2007, 3],
             [2006, 1, 2007, 4],
             [2006, 2, 2008, 1],
             [2006, 3, 2008, 2],
             [2006, 4, 2008, 3],
             [2007, 1, 2008, 4],
             [2007, 2, 2009, 1],
             [2007, 3, 2009, 2],
             [2007, 4, 2009, 3],
             [2008, 1, 2009, 4],
             [2008, 2, 2010, 1],
             [2008, 3, 2010, 2],
             [2008, 4, 2010, 3],
             [2009, 1, 2010, 4],
             [2009, 2, 2011, 1],
             [2009, 3, 2011, 2],
             [2009, 4, 2011, 3],
             [2010, 1, 2011, 4],
             [2010, 2, 2012, 1],
             [2010, 3, 2012, 2],
             [2010, 4, 2012, 3],
             [2011, 1, 2012, 4]]

    banks = get_banks_data()

    res = pd.DataFrame(columns=['Date','CovarUnc','Covar'])

    for d in dates:
        covar_unc_matrix, covar_matrix = covar(banks, d[0], d[1], d[2], d[3])

        res = res.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                          'CovarUnc': portfolio_covar(covar_unc_matrix, banks, d[2], d[3]),
                          'Covar': portfolio_covar(covar_matrix, banks, d[2], d[3])}, ignore_index=True)

    print(res)

    plt.plot(res['CovarUnc'], label="Covar Unc")
    plt.plot(res['Covar'], label="Covar")
    plt.title('Portfolio Covar Trend')
    plt.xticks(list(range(0,len(res))), res['Date'], rotation='vertical')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Covar')
    plt.show()


#Plotto il grafico andamentale del portfolio systemic expected shortfall
if False:
    dates = [['2005-01-01','2005-04-03',2005,1],
             ['2005-04-03','2005-07-02',2005,2],
             ['2005-07-04','2005-10-03',2005,3],
             ['2005-10-03','2005-12-30',2005,4],
             ['2006-01-01','2006-04-03',2006,1],
             ['2006-04-03','2006-07-02',2006,2],
             ['2006-07-03','2006-10-02',2006,3],
             ['2006-10-03','2006-12-30',2006,4],
             ['2007-01-01','2007-04-03',2007,1],
             ['2007-04-03','2007-07-02',2007,2],
             ['2007-07-03','2007-10-02',2007,3],
             ['2007-10-03','2007-12-30',2007,4],
             ['2008-01-01','2008-04-03',2008,1],
             ['2008-04-03','2008-07-02',2008,2],
             ['2008-07-03','2008-10-02',2008,3],
             ['2008-10-03','2008-12-30',2008,4],
             ['2009-01-01','2009-04-03',2009,1],
             ['2009-04-03','2009-07-02',2009,2],
             ['2009-07-04','2009-10-03',2009,3],
             ['2009-10-03','2009-12-30',2009,4],
             ['2010-01-01','2010-04-03',2010,1],
             ['2010-04-03','2010-07-02',2010,2],
             ['2010-07-03','2010-10-02',2010,3],
             ['2010-10-03','2010-12-30',2010,4],
             ['2011-01-01','2011-04-03',2011,1],
             ['2011-04-03','2011-07-02',2011,2],
             ['2011-07-03','2011-10-02',2011,3],
             ['2011-10-03','2011-12-30',2011,4],
             ['2012-01-01','2012-04-03',2012,1],
             ['2012-04-03','2012-07-02',2012,2],
             ['2012-07-03','2012-10-02',2012,3],
             ['2012-10-03','2012-12-30',2012,4]]

    banks = get_banks_data()


    res = pd.DataFrame(columns=['Date','SES'])

    for d in dates:
        date_start = d[0]
        date_end = d[1]

        year_weight = d[2]
        quarter_weight = d[3]

        data_matrix = ses(banks, date_start, date_end)

        porfolio_ses = portfolio_ses(data_matrix, banks, 2008, 3)
        res = res.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                          'SES': porfolio_ses}, ignore_index=True)

    print(res)

    plt.plot(res['SES'], label="SES")
    plt.title('Portfolio SES Trend')
    plt.xticks(list(range(0,len(res))), res['Date'], rotation='vertical')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('SES')
    plt.show()

#Plotto il grafico andamentale delle granger casualities
if True:

    dates = [['2007-07-03','2007-10-02',2007,3],
             ['2007-10-03','2007-12-30',2007,4],
             ['2008-01-01','2008-04-03',2008,1],
             ['2008-04-03','2008-07-02',2008,2],
             ['2008-07-03','2008-10-02',2008,3],
             ['2008-10-03','2008-12-30',2008,4],
             ['2009-01-01','2009-04-03',2009,1],
             ['2009-04-03','2009-07-02',2009,2],
             ['2009-07-04','2009-10-03',2009,3],
             ['2009-10-03','2009-12-30',2009,4],
             ['2010-01-01','2010-04-03',2010,1],
             ['2010-04-03','2010-07-02',2010,2],
             ['2010-07-03','2010-10-02',2010,3],
             ['2010-10-03','2010-12-30',2010,4],
             ['2011-01-01','2011-04-03',2011,1],
             ['2011-04-03','2011-07-02',2011,2],
             ['2011-07-03','2011-10-03',2011,3],
             ['2011-10-03','2011-12-30',2011,4],
             ['2012-01-01','2012-04-03',2012,1],
             ['2012-07-03','2012-10-02',2012,2],
             ['2012-07-03','2012-10-02',2012,3],
             ['2012-10-03','2012-12-30',2012,4]]

    average_connection = pd.DataFrame(columns=['Date','Average_Connection'])

    for d in dates:
        date_start = d[0]
        date_end = d[1]

        year_weight = d[2]
        quarter_weight = d[3]

        print(date_end)

        granger_matrix = granger_casualties(banks, full_period=False, date_start=date_start, date_end=date_end)

        granger_ranking = pd.DataFrame(granger_matrix.sum(axis=1), index=granger_matrix.index,
                                       columns=['Number of Connections'])

        average_connection = average_connection.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                                                        'Average_Connection': float(granger_ranking.mean())}, ignore_index=True)

    print(average_connection)

    plt.plot(average_connection['Average_Connection'], label="Average_Connection")
    plt.title('Average Connection Trend')
    plt.xticks(list(range(0,len(average_connection))), average_connection['Date'], rotation='vertical')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Average_Connection')
    plt.show()
