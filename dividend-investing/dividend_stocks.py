import pandas as pd
import numpy as np
import email_sender as email
from qtrade import Questrade

watchlist = [('MO', 45), ('SBUX', 100)]

qt = Questrade()
data = qt.get_historical_data('MO')

print(data)
#for stock in watchlist:
