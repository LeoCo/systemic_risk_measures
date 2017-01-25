from getdata import get_banks_data, get_states_variable
import statsmodels.api as sm
import bank
import pandas as pd
from covar import covar, portfolio_covar
from systemic_expected_shortfall import ses, portfolio_ses
import numpy as np


#Carico il dataset delle banche
banks = get_banks_data()


#Creo la lista dei delta MVA del portafoglio

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