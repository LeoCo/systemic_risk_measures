import pandas as pd
from getdata import get_banks_data


def grange_casualties(banks):
    banks_name = []

    for x in banks:
        banks_name.append(x.ticker)

    df = pd.DataFrame(index=banks_name, columns=banks_name)

    #Calcola i rendimenti(yealds) per tutte le banche
    for x in banks:
        print(x.yealds)


    return df

if __name__ == '__main__':

    banks = get_banks_data()

    grange_matrix = grange_casualties(banks)

    print(grange_matrix)