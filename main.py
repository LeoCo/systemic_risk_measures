from getdata import get_banks_data
import matplotlib.pyplot as plt
import statsmodels.api as sm
import bank

banks = get_banks_data()

for x in banks:

    #Stampa lista banche
    if False:
        print(x.name)
        print(x.ticker)
        print(x.datas.head())
        print(x.prices.head())
        print(x.yealds.head())

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

    #Regressione
    if False:

        y = x.prices['PX_LAST']

        X = list(range(0,len(x.prices['PX_LAST'])))
        X = sm.add_constant(X)

        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())

        predictions = results.predict(X)

        df = x.prices
        plt.plot(df['Date'], df['PX_LAST'], label="Sample")
        plt.plot(df['Date'], predictions, label="Prediction")
        plt.title(x.name)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Prices')
        plt.show()


#Testo il metodo di ricerca in lista
if True:

    x = bank.find_ticker_in_list('ACA:FP',banks)

    print(x.name)
