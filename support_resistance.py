import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt


symbol = 'EURUSD=X'

START_DATE = dt.datetime(2020,1,1) 
END_DATE = dt.datetime.today()

df = web.DataReader(symbol, 'yahoo', START_DATE, END_DATE)

pivots = []

dates = []

periods = 20

counter = 0

lastPivot = -1

Range = [0] * periods
dateRange = [0] * periods

for i in df.index:
    currMax = max(Range, default=0)
    value = round(df['High'][i],4)
    
    Range = Range[1:periods]
    print(Range)
    Range.append(value)
    dateRange = dateRange[1:periods]
    dateRange.append(i)
    
    # Range[len(Range) - 1] = value
    # dateRange[len(dateRange) - 1] = i
    
    if currMax == max(Range, default=0):
        counter += 1
    else:
        counter = 0
    
    if counter == 10:
        lastPivot = currMax
        dateloc = Range.index(lastPivot)
        lastDate = dateRange[dateloc]
        pivots.append(lastPivot)
        dates.append(lastDate)
        print("today is {} and lastDate is {}".format(str(i),str(lastDate)))

print()

# print(str(pivots))
# print(str(dates))

for index in range(len(pivots)):
    print(str(pivots[index]) + " : " + str(dates[index]))


df['High'].plot(label='High')