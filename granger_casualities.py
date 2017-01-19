import pandas as pd
import bank
import statsmodels.tsa.stattools as st
from getdata import get_banks_data
import time


def granger_casualties(banks, full_period=True, date_start="", date_end=""):
    banks_name = []

    #Creo la matrice delle correlazioni
    for x in banks:
        banks_name.append(x.ticker)

    corr_matrix = pd.DataFrame(index=banks_name, columns=banks_name)

    for x in corr_matrix.index:
        for y in corr_matrix.columns:

            bank_a = bank.find_ticker_in_list(x,banks)
            bank_b = bank.find_ticker_in_list(y,banks)

            corr_matrix.loc[x,y] = correlation_a_granger_caused_by_b(bank_a,bank_b,full_period=full_period, date_start=date_start, date_end=date_end)


    return corr_matrix

def correlation_a_granger_caused_by_b(a, b, full_period=True, date_start="", date_end="",p_value=0.01):

    influenced = 0

    yealds1 = a.yealds

    yealds2 = b.yealds

    yeald_inner_join = pd.merge(yealds1, yealds2, on='Date', how='inner')

    if full_period == False:
        #Filtro solo le date che mi servono
        mask = (yeald_inner_join['Date'] >= date_start) & (yeald_inner_join['Date'] <= date_end)
        yeald_inner_join = yeald_inner_join.loc[mask]
        #Se non ci sono sovrapposizioni di date ritorna zero ovvero che non sono correlate
        if yeald_inner_join.empty:
            return 0


    x = yeald_inner_join[['Yeald_x','Yeald_y']]

    granger_result = st.grangercausalitytests(x, 1,verbose=False)

    granger_pvalue = granger_result[1][0]['ssr_ftest'][1]

    if granger_pvalue <= p_value:
        influenced = 1

    return influenced

if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    print("Get data time: " + str(time.clock() - start))

    #Calcolo i rendimenti
    #for x in banks:
    #    x.yealds = bank.compute_yealds(x)


    #print("Get data time: " + str(time.clock() - start))

    writer = pd.ExcelWriter('Output/granger_casualties_test.xlsx')

    print('Granger Matrix of the 2008 crysis')
    date_start = '2006-9-15'
    date_end = '2008-9-15'
    granger_matrix = granger_casualties(banks, full_period=False, date_start=date_start, date_end=date_end)
    print(granger_matrix)
    print()
    sheet_title = str(date_start) + "_" + str(date_end)
    granger_matrix.to_excel(writer, sheet_title)

    print('Granger Matrix of the 2012 crysis')
    date_start = '2010-6-30'
    date_end = '2012-6-30'
    granger_matrix = granger_casualties(banks, full_period=False, date_start=date_start, date_end=date_end)
    print(granger_matrix)
    print()
    sheet_title = str(date_start) + "_" + str(date_end)
    granger_matrix.to_excel(writer, sheet_title)

    print('Granger Matrix of the full available time period')
    granger_matrix = granger_casualties(banks)
    print(granger_matrix)
    print()
    sheet_title = "Full Period"
    granger_matrix.to_excel(writer, sheet_title)

    writer.save()

    run_time = time.clock() - start

    print("Execution time: " + str(run_time))
