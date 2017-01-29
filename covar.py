from getdata import get_banks_data, get_states_variable
import pandas as pd
import numpy as np
import time
import statsmodels.api as sm
from bank import find_ticker_in_list

def portfolio_system_return(banks, year_start=2000,year_end=2015):

    portfolio_system_return = pd.DataFrame(columns=['Year', 'Quarter', 'PSR'])

    for year in range(year_start, year_end + 1):
        for quarter in range(1, 5):

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

            entry = pd.Series([year, quarter, current_portfolio_system_return], index=['Year', 'Quarter', 'PSR'])
            portfolio_system_return = portfolio_system_return.append(entry, ignore_index=True)

    return portfolio_system_return

def covar(banks, year_from, quarter_from, year_to, quarter_to):

    #Calcolo il portfolio system return
    psr = portfolio_system_return(banks,year_start=2000,year_end=2015)

    # Calcolo i B di Xsys = a + B * X

    # Preparo il vettore y filtrando i quarti
    mask = (psr['Year'] == year_from) & (psr['Quarter'] == quarter_from)
    start_index = psr[mask].index[0]
    mask = (psr['Year'] == year_to) & (psr['Quarter'] == quarter_to)
    end_index = psr[mask].index[0]
    y = psr['PSR'].iloc[start_index:end_index+1]
    y.reset_index(drop=True, inplace=True)
    y.name = 'PSR'

    # Preparo la matrice X
    X = pd.DataFrame()

    for b in banks:
        mask = (b.mva['Year'] == year_from) & (b.mva['Quarter'] == quarter_from)
        if any(mask == True):
            start_index = b.mva[mask].index[0]
            mask = (b.mva['Year'] == year_to) & (b.mva['Quarter'] == quarter_to)
            if any(mask == True):
                end_index = b.mva[mask].index[0]
                s = b.mva['DELTA_MVA'].iloc[start_index:end_index+1]
                s.reset_index(drop=True, inplace=True)
                s.name = b.ticker
                X.reset_index(drop=True, inplace=True)
                X = pd.concat([X, s], axis=1)

    # Eseguo la quantile regression per ogni banca

    covar_unc_matrix = pd.DataFrame(columns=['Ticker', 'Beta', 'COVAR', 'VAR_0.01', 'VAR_0.5'])

    for ticker in X.columns.values:

        x = X[ticker]

        if not x.isnull().values.sum():
            x = sm.add_constant(x)

            model = sm.QuantReg(y, x)

            res = model.fit(q=0.01)

            x_pred = [1, X[ticker].quantile(q=0.01)]

            # Calcolo il covar
            covar = np.float(res.predict(x_pred))

            covar_unc_matrix = covar_unc_matrix.append(
                {'Ticker': ticker, 'Beta': res.params[ticker],
                 'COVAR': covar,
                 'VAR_0.01': X[ticker].quantile(q=0.01),
                 'VAR_0.5': X[ticker].quantile(q=0.5)}, ignore_index=True)


    # Calcolo il delta covar unconditional
    covar_unc_matrix['DELTA_COVAR_UNC'] = covar_unc_matrix['Beta'] * (
    covar_unc_matrix['VAR_0.01'] - covar_unc_matrix['VAR_0.5'])

    # Carico le variabili di stato
    states_variables = get_states_variable()

    # Preparo la parte delle X con le variabili di sistema e la chiamo X2
    mask = (states_variables['Year'] == year_from) & (states_variables['Quarter'] == quarter_from)
    start_index = states_variables[mask].index[0]
    mask = (states_variables['Year'] == year_to) & (states_variables['Quarter'] == quarter_to)
    end_index = states_variables[mask].index[0]
    start_index -= 1
    X2 = states_variables.iloc[start_index:end_index]
    X2 = X2[['V2X Index', 'SX7P Index', 'Spr_Liq_St', 'Incl_curv_rend', 'var_t-bill_3M','credit_spread']]
    X2.reset_index(drop=True, inplace=True)

    # Inizializzo la matrice covar
    covar_matrix = pd.DataFrame(columns=['Ticker', 'Beta', 'COVAR', 'VAR_0.01', 'VAR_0.5', 'DELTA_COVAR'])

    # Eseguo la regressione OLS per ogni banca
    for ticker in X.columns.values:

        X1 = X[ticker]

        if not X1.isnull().values.sum():
            # Preparo gli input per la regressione OLS, le y non cambiano

            # Preparo le X

            X1_X2 = pd.concat([X1, X2], axis=1)
            X1_X2 = sm.add_constant(X1_X2)

            # Eseguo la regressione
            model = sm.OLS(y, X1_X2)
            results = model.fit()

            # Preparo X1 e X2 Predict
            X1_pred = pd.Series(X[ticker].quantile(q=0.01), name=b.ticker)

            X2_pred = X2.iloc[-1]

            X2_pred = pd.DataFrame(X2_pred).transpose()

            X2_pred.reset_index(drop=True, inplace=True)

            X1_X2_pred = pd.concat([X1_pred, X2_pred], axis=1, ignore_index=True)

            X1_X2_pred = sm.add_constant(X1_X2_pred)

            # Calcolo il covar
            covar = results.predict(X1_X2_pred)

            # Memorizzo il covar
            covar_matrix = covar_matrix.append({'Ticker': ticker, 'COVAR': covar[0],
                                                'Beta': results.params[ticker],
                                                'VAR_0.01': X[ticker].quantile(q=0.01),
                                                'VAR_0.5': X[ticker].quantile(q=0.5)}, ignore_index=True)

    covar_matrix['DELTA_COVAR'] = covar_matrix['Beta'] * (covar_matrix['VAR_0.01'] - covar_matrix['VAR_0.5'])

    return covar_unc_matrix, covar_matrix

def portfolio_covar(covar_matrix, banks, year, quarter):

    covar = covar_matrix.copy()

    covar['Weighted'] = 0

    mva_sum = 0

    for ticker in covar['Ticker']:
        bank = find_ticker_in_list(ticker,banks)
        mask = (bank.mva['Year'] == year ) & ( bank.mva['Quarter'] == quarter)

        mva = float(bank.mva[mask]['MVA'])

        mva_sum += mva

        covar.loc[covar['Ticker'] == ticker, 'Weighted'] = mva * covar.loc[covar['Ticker'] == ticker, 'COVAR']

    portfolio_covar = covar['Weighted'].sum() / mva_sum

    return portfolio_covar

if __name__ == '__main__':

    start = time.clock()

    banks = get_banks_data()

    print("Get data time: " + str(time.clock() - start))

    # Intervallo in quarters
    quarter_from = 1
    year_from = 2009

    quarter_to = 4
    year_to = 2011

    covar_unc_matrix, covar_matrix = covar(banks, year_from, quarter_from, year_to,quarter_to)

    print()
    print('Delta Covar Unconditional')
    print('Portfolio Covar: ' + str(portfolio_covar(covar_unc_matrix, banks, year_from,quarter_to)))
    print('From quarter ' + str(quarter_from) +' of ' + str(year_from) + ' to quarter ' + str(quarter_to) +' of ' + str(year_to))
    print()
    print(covar_unc_matrix)


    writer = pd.ExcelWriter('Output/covar.xlsx')
    sheet_name = "CovarUnc_Q" + str(quarter_from) + '-' + str(year_from) + "_to_Q" + str(quarter_to) + "-" + str(year_to)
    covar_unc_matrix.to_excel(writer, sheet_name)


    print()
    print('Delta Covar')
    print('Portfolio Covar: ' + str(portfolio_covar(covar_matrix, banks, year_from,quarter_to)))
    print('From quarter ' + str(quarter_from) +' of ' + str(year_from) + ' to quarter ' + str(quarter_to) +' of ' + str(year_to))
    print()
    print(covar_matrix)

    sheet_name = "Covar_Q" + str(quarter_from) + '-' + str(year_from) + "_to_Q" + str(quarter_to) + "-" + str(year_to)
    covar_matrix.to_excel(writer, sheet_name)

    writer.save()

    run_time = time.clock() - start

    print("Execution time: " + str(run_time))

