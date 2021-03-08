import pandas as pd
import numpy as np

def clear_why(s):
    if '?' in s:
        s = s[:s.index('?')]
    return s

df = pd.read_csv('div_kings_2020.csv')

consumer_defensive = df[(df['Exchange'] == 'NYSE') & (df['Sector'] == 'Consumer defensive')]

print(consumer_defensive)