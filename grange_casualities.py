import pandas as pd
import random
from getdata import get_banks_data


def grange_casualties(banks):
    banks_name = []

    #Creo la matrice delle correlazioni
    for x in banks:
        banks_name.append(x.ticker)

    corr_matrix = pd.DataFrame(index=banks_name, columns=banks_name)

    for x in corr_matrix.columns:
        for y in corr_matrix.index:
            corr_matrix.loc[x,y] = correlation_a_to_b(x,y)


    return corr_matrix

def correlation_a_to_b(a,b):
    #mock

    return random.randint(0,1)

if __name__ == '__main__':

    banks = get_banks_data()

    grange_matrix = grange_casualties(banks)

    print(grange_matrix)