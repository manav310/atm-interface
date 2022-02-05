import pandas as pd
import numpy as np

arr = np.zeros((10000, 4))
df = pd.DataFrame(arr, columns = ['Account Name', 'Card Number', 'PIN', 'Balance'])

df.to_csv('atm-interface/account_database.csv')