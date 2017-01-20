from getdata import get_banks_data, get_states_variable
import pandas as pd
import numpy as np
import time
import statsmodels.api as sm

if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    print("Get data time: " + str(time.clock() - start))

    year_start = 2000
    year_end = 2015

    #Calcolo il portfolio system return
    portfolio_system_return = pd.DataFrame(columns=['Year','Quarter','PSR'])

    for year in range(year_start,year_end+1):
        for quarter in range(1,5):

            numerator = 0

            denominator = 0

            for bank in banks:

                mask = (bank.mva['Year'] == year) & (bank.mva['Quarter'] == quarter)

                delta_mva = 0
                mva = 0

                if bank.mva[mask].empty:
                    mva = 0
                    delta_mva = 0
                else:
                    mva = np.float64(bank.mva['MVA'][mask])
                    delta_mva = np.float64(bank.mva['DELTA_MVA'][mask])

                numerator += mva * delta_mva

                denominator += mva



            current_portfolio_system_return = numerator / denominator

            entry = pd.Series([year, quarter, current_portfolio_system_return], index=['Year','Quarter','PSR'])
            portfolio_system_return = portfolio_system_return.append(entry, ignore_index=True)

    print()
    print('Portfolio System Return')
    print()
    print(portfolio_system_return)
    print()

    # Calcolo i B di Xsys = a + B * X

    # Intervallo di anni
    year_from = 2010
    year_to = 2012

    # Preparo il vettore y
    mask = (portfolio_system_return['Year'] >= year_from) & (portfolio_system_return['Year'] <= year_to)
    y = portfolio_system_return['PSR'][mask]
    y.reset_index(drop=True, inplace=True)
    y.name = 'PSR'


    #Preparo la matrice X
    X = pd.DataFrame()

    for b in banks:
        mask = (b.mva['Year'] >= year_from) & (b.mva['Year'] <= year_to)
        s = b.mva.loc[mask,'DELTA_MVA']
        s.reset_index(drop=True, inplace=True)
        s.name = b.ticker
        X.reset_index(drop=True, inplace=True)
        X = pd.concat([X, s],axis=1)


    # Eseguo la quantile regression per ogni banca

    delta_covar_unconditional = pd.DataFrame(columns=['Ticker', 'Beta', 'VAR_0.01', 'VAR_0.5'])

    for b in banks:

        x = X[b.ticker]

        if not x.isnull().values.sum():
            x = sm.add_constant(x)

            model = sm.QuantReg(y,x)

            res = model.fit(q=0.01)

            #print(res.summary())

            delta_covar_unconditional = delta_covar_unconditional.append({'Ticker':b.ticker, 'Beta':res.params[b.ticker],
                                                        'VAR_0.01':X[b.ticker].quantile(q=0.01),
                                                        'VAR_0.5':X[b.ticker].quantile(q=0.5)}, ignore_index=True)

    #Calcolo il delta covar unconditional
    delta_covar_unconditional['DELTA_COVAR_UNC'] = delta_covar_unconditional['Beta'] * (delta_covar_unconditional['VAR_0.01'] - delta_covar_unconditional['VAR_0.5'])

    print()
    print('Delta Covar Unconditional')
    print('From first quarter of ' + str(year_from) + " to last quarter of " + str(year_to))
    print()
    print(delta_covar_unconditional)


    writer = pd.ExcelWriter('Output/covar.xlsx')
    sheet_name = "CovarUnc_" + str(year_from) + "_to_" + str(year_to)
    delta_covar_unconditional.to_excel(writer, sheet_name)

    #Carico le variabili di stato
    states_variables = get_states_variable()

    #Preparo la parte delle X con le variabili di sistema e la chiamo X2
    start_index = states_variables[(states_variables['Year'] == year_from) & (states_variables['Quarter'] == 1)].index[0]
    start_index -= 1
    quarters = ((year_to + 1) - year_from) * 4
    end_index = start_index + quarters
    X2 = states_variables.iloc[start_index:end_index]
    X2 = X2[['V2X Index','SX5E Index','Spr_Liq_St','Incl_curv_rend','var_t-bill_3M']]
    X2.reset_index(drop=True, inplace=True)

    print(X2)

    covar_matrix = pd.DataFrame(columns=['Ticker','Covar'])

    #Eseguo la regressione OLS per ogni banca
    for b in banks:

        #Preparo gli input per la regressione OLS, le y non cambiano

        #Preparo le X
        X1 = X[b.ticker]

        X1_X2 = pd.concat([X1,X2],axis=1)
        X1_X2 = sm.add_constant(X1_X2)

        #Eseguo la regressione
        model = sm.OLS(y, X1_X2)
        results = model.fit()

        #Preparo X1 e X2 Predict
        X1_pred = pd.Series(X[b.ticker].quantile(q=0.01),name=b.ticker)

        X2_pred = X2.iloc[-1]

        X2_pred = pd.DataFrame(X2_pred).transpose()

        X2_pred.reset_index(drop=True, inplace=True)

        X1_X2_pred = pd.concat([X1_pred, X2_pred], axis=1,ignore_index=True)

        X1_X2_pred = sm.add_constant(X1_X2_pred)

        #Calcolo il covar
        covar = results.predict(X1_X2_pred)

        #Memorizzo il covar
        covar_matrix = covar_matrix.append({'Ticker': b.ticker, 'Covar': covar[0]}, ignore_index=True)



    print(covar_matrix)

    sheet_name = "Covar_" + str(year_from) + "_to_" + str(year_to)
    covar_matrix.to_excel(writer, sheet_name)


    writer.save()

    run_time = time.clock() - start

    print("Execution time: " + str(run_time))

