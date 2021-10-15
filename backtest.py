import numpy as np
from oandaTrader import OandaTrader
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID

oanda = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)

# OHLCV(open, high, Low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = oanda.get_ohlc('BTC_USD', 1000, 'D')

# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['High'] - df['Low']) * 0.5

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['Open'] + df['range'].shift(1)

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['High'] > df['target'],
                     df['Close'] / df['target'],
                     1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD 계산
print("MDD(%): ", df['dd'].max())

print(df)

#엑셀로 출력
# df.to_excel("dd.xlsx")