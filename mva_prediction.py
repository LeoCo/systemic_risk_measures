from getdata import get_banks_data, get_states_variable
import statsmodels.api as sm
import pandas as pd
from covar import covar, portfolio_covar
from systemic_expected_shortfall import ses, portfolio_ses
import time
import matplotlib.pyplot as plt
from granger_casualities import granger_casualties
import numpy as np



start = time.clock()

# "If True:" Aggiorno il dataset
if False:

    #Carico il dataset delle banche
    banks = get_banks_data()
    print("Get data time: " + str(time.clock() - start))
    print()

    #Creo il dataframe dei delta MVA del portafoglio ovvero le y della regressione

    dates = [[2005,1],
             [2005,2],
             [2005,3],
             [2005,4],
             [2006,1],
             [2006,2],
             [2006,3],
             [2006,4],
             [2007,1],
             [2007,2],
             [2007,3],
             [2007,4],
             [2008,1],
             [2008,2],
             [2008,3],
             [2008,4],
             [2009,1],
             [2009,2],
             [2009,3],
             [2009,4],
             [2010,1],
             [2010,2],
             [2010,3],
             [2010,4],
             [2011,1],
             [2011,2],
             [2011,3],
             [2011,4],
             [2012,1],
             [2012,2],
             [2012,3],
             [2012,4]]

    portfolio_delta_mva = pd.DataFrame(columns=['Date','DELTA_MVA'])

    #Primo elemento
    year = dates[0][0]
    quarter = dates[0][1]

    for d in dates:

        year = d[0]
        quarter = d[1]

        total_mva = 0
        weighted_delta_mva = 0

        for b in banks:
            mask = (b.mva['Year'] == year) & (b.mva['Quarter'] == quarter)
            bank_mva = b.mva[mask]['MVA']
            bank_delta_mva = b.mva[mask]['DELTA_MVA']

            if ( len(bank_delta_mva) > 0 ):
                weighted_delta_mva += float(bank_mva * bank_delta_mva)
                total_mva += float(bank_mva)

        delta_mva = weighted_delta_mva / total_mva

        portfolio_delta_mva = portfolio_delta_mva.append({'Date': 'Q' + str(quarter) + '-' + str(year),
                                                        'DELTA_MVA': delta_mva}, ignore_index=True)

    print(portfolio_delta_mva)

    #Creo il dataframe delle x

    #Preparo il SES
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

    systemic_expected_shortfall = pd.DataFrame(columns=['Date', 'SES'])

    for d in dates:
        date_start = d[0]
        date_end = d[1]

        year_weight = d[2]
        quarter_weight = d[3]

        data_matrix = ses(banks, date_start, date_end)

        porfolio_ses = portfolio_ses(data_matrix, banks, 2008, 3)
        systemic_expected_shortfall = systemic_expected_shortfall.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                          'SES': porfolio_ses}, ignore_index=True)

    print(systemic_expected_shortfall)

    dataset = pd.merge(portfolio_delta_mva, systemic_expected_shortfall, on='Date')

    print(dataset)

    #Preparo il covar
    dates = [[2005, 4, 2007, 3],
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

    res = pd.DataFrame(columns=['Date','CovarUnc','Covar'])

    for d in dates:
        covar_unc_matrix, covar_matrix = covar(banks, d[0], d[1], d[2], d[3])

        res = res.append({'Date': 'Q' + str(d[3]) + '-' + str(d[2]),
                          'CovarUnc': portfolio_covar(covar_unc_matrix, banks, d[2], d[3]),
                          'Covar': portfolio_covar(covar_matrix, banks, d[2], d[3])}, ignore_index=True)

    print(res)

    dataset = pd.merge(dataset, res, on='Date')

    print(dataset)

    #Preparo le granger casualities
    dates = [['2007-07-03', '2007-10-02', 2007, 3],
             ['2007-10-03', '2007-12-30', 2007, 4],
             ['2008-01-01', '2008-04-03', 2008, 1],
             ['2008-04-03', '2008-07-02', 2008, 2],
             ['2008-07-03', '2008-10-02', 2008, 3],
             ['2008-10-03', '2008-12-30', 2008, 4],
             ['2009-01-01', '2009-04-03', 2009, 1],
             ['2009-04-03', '2009-07-02', 2009, 2],
             ['2009-07-04', '2009-10-03', 2009, 3],
             ['2009-10-03', '2009-12-30', 2009, 4],
             ['2010-01-01', '2010-04-03', 2010, 1],
             ['2010-04-03', '2010-07-02', 2010, 2],
             ['2010-07-03', '2010-10-02', 2010, 3],
             ['2010-10-03', '2010-12-30', 2010, 4],
             ['2011-01-01', '2011-04-03', 2011, 1],
             ['2011-04-03', '2011-07-02', 2011, 2],
             ['2011-07-03', '2011-10-03', 2011, 3],
             ['2011-10-03', '2011-12-30', 2011, 4],
             ['2012-01-01', '2012-04-03', 2012, 1],
             ['2012-07-03', '2012-10-02', 2012, 2],
             ['2012-07-03', '2012-10-02', 2012, 3],
             ['2012-10-03', '2012-12-30', 2012, 4]]

    average_connection = pd.DataFrame(columns=['Date', 'Average_Connection'])

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
                                                        'Average_Connection': float(granger_ranking.mean())},
                                                       ignore_index=True)


    dataset = pd.merge(dataset, average_connection, on='Date')

    print(average_connection)


    #Salvo in un file locale il dataset
    filename = 'dataset.csv'
    dataset.to_csv(filename, index=False)

    print("Loading time: " + str(time.clock() - start))
    print()


#Carico il dataset
filename = 'dataset.csv'
dataset = pd.read_csv(filename)
print(dataset)

#Regressione quadratica?
quadratic_reg = True

#Regressione

#Divido i dati in training set e test set
split_number = 15

y_train = dataset[['DELTA_MVA']].iloc[:split_number]

X_train = dataset[['SES','CovarUnc','Covar','Average_Connection']].iloc[:split_number]

if quadratic_reg == True:
    X_train['SES_sq'] = np.square(X_train['SES'])
    X_train['CovarUnc_sq'] = np.square(X_train['CovarUnc'])
    X_train['Covar_sq'] = np.square(X_train['Covar'])
    X_train['Average_Connection_sq'] = np.square(X_train['Average_Connection'])

X_train = sm.add_constant(X_train)

print(y_train)

print(X_train)

y_test = dataset[['DELTA_MVA']].iloc[split_number:]

X_test = dataset[['SES','CovarUnc','Covar','Average_Connection']].iloc[split_number:]

if quadratic_reg == True:
    X_test['SES_sq'] = np.square(X_test['SES'])
    X_test['CovarUnc_sq'] = np.square(X_test['CovarUnc'])
    X_test['Covar_sq'] = np.square(X_test['Covar'])
    X_test['Average_Connection_sq'] = np.square(X_test['Average_Connection'])

X_test = sm.add_constant(X_test)

print(y_test)

#Effettuo la regressione sul training set
model = sm.OLS(y_train.astype(float), X_train.astype(float))
results = model.fit()

print(results.summary())

#Predico usando il test set
pred_matrix = dataset[['Date']].iloc[split_number:].reset_index(drop=True)

predictions = results.predict(X_test)

pred_matrix.loc[:,'Pred_DELTA_MVA'] = pd.Series(predictions, index=pred_matrix.index)

print(pred_matrix)

#Disegno il grafico

plt.plot(dataset['DELTA_MVA'], label="Delta MVA")
plt.plot(list(range(split_number, len(dataset))),pred_matrix['Pred_DELTA_MVA'], label="Pred Delta MVA",color='r')
plt.title('Delta MVA Prediction')
plt.xticks(list(range(0, len(dataset))), dataset['Date'], rotation='vertical')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Delta MVA')
plt.show()

print("Execution time: " + str(time.clock() - start))
print()
