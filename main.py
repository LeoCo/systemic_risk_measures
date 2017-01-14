from getdata import get_banks_data
import matplotlib.pyplot as plt

banks = get_banks_data()

for x in banks:

    #Stampa lista banche
    if True:
        print(x.name)
        print(x.ticker)
        print(x.datas.head())
        print(x.prices.head())

    #Fa il grafico del prezzo delle azioni
    if True:
        df = x.prices
        plt.plot(df['Date'], df['PX_LAST'])
        plt.title(x.name)
        plt.xlabel('Date')
        plt.ylabel('Prices')
        plt.show()




