import statsmodels.tsa.stattools as st
import numpy as np


x = np.array([[1,5],
              [2,800],
              [4,10],
              [5,-12],
              [7,14]])

res = st.grangercausalitytests(x,1)

print(res)

print("")

print(res[1][0]['ssr_ftest'][1])
