import numpy as np
import pandas as pd
import json

## Converts a JSON file to a pandas dataframe

def convert_i(text):
	if str == '[]':
		return np.nan
	else:
		lst = json.loads(text)
		return [(item[0], item[1]) for item in lst]
def convert_dt(text):
	lst = json.loads(text)
	return lst[0], lst[1]
def read(path):
	df = pd.read_table(path, header=None, names=['dt', 'i'])
	df['points'] = df['i'].apply(convert_i)
	df['date'], df['time'] = zip(*df['dt'].map(convert_dt))
	return df.drop(['dt', 'i'], axis = 1)