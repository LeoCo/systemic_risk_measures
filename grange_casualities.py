import pandas as pd
from getdata import get_banks_data


def compute_yealds(bank):

    #Creao un df per i rendimenti
    dates = bank.prices['Date'][1:]
    columns = ['Date','Yeald']
    yealds = pd.DataFrame(dates, columns=columns)
    #yealds['Yeald'] = 0

    #Calcolo i rendimenti

    price_yesterday = bank.prices['PX_LAST'][0]

    price_today = 0

    for i in range(0,len(yealds)):
        price_today = bank.prices['PX_LAST'][i + 1]

        yeald = (price_today - price_yesterday)/price_yesterday

        yealds.loc[i+1,'Yeald'] = yeald

        price_yesterday = price_today


    return yealds


def grange_casualties(banks):
    banks_name = []

    for x in banks:
        banks_name.append(x.ticker)

    df = pd.DataFrame(index=banks_name, columns=banks_name)

    #Calcola i rendimenti(yealds) per tutte le banche
    for x in banks:
        x.yealds = compute_yealds(x)
        print(x.yealds)


    return df

if __name__ == '__main__':

    banks = get_banks_data()

    grange_matrix = grange_casualties(banks)

    print(grange_matrix)