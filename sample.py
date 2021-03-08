import financial_data_helper_func as hf
import pandas as pd


b = hf.get_daily_price_data('AMZN', '1970-01-01', '2020-12-13')

print(b.head())

a = hf.get_price_and_return_data('AMZN', '1970-01-01', '2020-12-25')

cagr_a = hf.calculate_cagr(a)

print(cagr_a)

mdd_a = hf.calculate_mdd(a)

print(mdd_a)

print(hf.calculate_vol(a))

print(hf.calculate_ex_post_sharpe(a))