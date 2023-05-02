# Data Analysis in NumPy and Pandas

## axis=0 or axis=1

- axis=0 : row
- axis=1 : column

## NaN

- isnull()
- dropna(subset=[], axis=0): remove rows with NaN
- dropna(axis=1): remove columns with NaN
- dropna(axis=1, thresh=300): remove columns with more than 300 NaN
- fillna(): df['age'].fillna(mean_age, inplace=True)

For Time Series data, we can replace NaN with previous or next data assuming that neighbor data have similarity.

- df['col'].fillna(method='ffill'): replace NaN with previous value
- df['col'].fillna(method='bfill'): replace NaN with next value

## DataFrame Index

- DataFrame.set_index('col', inplace=True)
- DataFrame.sort_index(inplace=True, ascending=False)
- DataFrame.reset_index(inplace=True)

## DataFrame Filtering

### Boolean Indexing
```python
filter_bool = (df['cylinders'] == 4)
df.loc[filter_bool, ]

filter_bool_2 = (df['cylinders'] == 4) & (df['horsepower'] >= 100)
df.loc[filter_bool_2, ['cylinders', 'horsepower', 'name']]
```

### isin()

```python
filter_isin = df['name'].isin(['ford maverick', 'ford mustang', 'chevrolet impala'])
df.loc[filter_isin, ]
```

## Create a New Column

```python
import numpy as np
num = pd.Series([-2,-1,1,2])
np.where(num >= 0, 'pos', 'neg') # ['neg', 'neg', 'pos', 'pos']

```

## Data Concatenation

- concat()
- merge()
- join()
