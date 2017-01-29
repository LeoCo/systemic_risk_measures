import statsmodels.api as sm
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score

start = time.clock()

def mva_prediction_score(dataset,split_number,quadratic_reg=False):

    y_train = dataset[['DELTA_MVA']].iloc[:split_number]

    X_train = dataset[['SES', 'CovarUnc', 'Covar', 'Average_Connection']].iloc[:split_number]

    if quadratic_reg == True:
        X_train['SES_sq'] = np.square(X_train['SES'])
        X_train['CovarUnc_sq'] = np.square(X_train['CovarUnc'])
        X_train['Covar_sq'] = np.square(X_train['Covar'])
        X_train['Average_Connection_sq'] = np.square(X_train['Average_Connection'])

    X_train = sm.add_constant(X_train)

    y_test = dataset[['DELTA_MVA']].iloc[split_number:]

    X_test = dataset[['SES', 'CovarUnc', 'Covar', 'Average_Connection']].iloc[split_number:]

    if quadratic_reg == True:
        X_test['SES_sq'] = np.square(X_test['SES'])
        X_test['CovarUnc_sq'] = np.square(X_test['CovarUnc'])
        X_test['Covar_sq'] = np.square(X_test['Covar'])
        X_test['Average_Connection_sq'] = np.square(X_test['Average_Connection'])

    X_test = sm.add_constant(X_test)

    # Effettuo la regressione sul training set
    model = sm.OLS(y_train.astype(float), X_train.astype(float))
    results = model.fit()

    # Predico usando il test set
    pred_matrix = dataset[['Date']].iloc[split_number:].reset_index(drop=True)

    predictions = results.predict(X_test)

    pred_matrix.loc[:, 'Pred_DELTA_MVA'] = pd.Series(predictions, index=pred_matrix.index)

    score = r2_score(y_test, predictions)

    return score



#Carico il dataset
filename = 'dataset.csv'
dataset = pd.read_csv(filename)
print(dataset)

results = pd.DataFrame(columns=['SplitNumber','Linear','Quadratic'])

min_sample = 12
max_sample = 18


for i in range(min_sample,max_sample):
    results = results.append({'SplitNumber': i,
                    'Linear': mva_prediction_score(dataset,split_number=i),
                    'Quadratic': mva_prediction_score(dataset, split_number=i,quadratic_reg=True)},
                                                       ignore_index=True)

print(results)

plt.plot(results['Linear'], label="Linear")
plt.plot(results['Quadratic'], label="Quadratic", color='r')
plt.title('MVA Prediction Analisys')
plt.xticks(list(range(0, max_sample-min_sample)), list(range(min_sample,max_sample)))
plt.legend()
plt.xlabel('Training set size')
plt.ylabel('R^2 Score')
plt.show()


