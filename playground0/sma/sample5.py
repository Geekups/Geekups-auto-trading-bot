import MetaTrader5 as mt5
import ta_lib
import datetime

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize failed")
    mt5.shutdown()

# get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H4
utc_from = datetime(2020, 1, 10)
rates = mt5.copy_rates_from_pos(symbol, timeframe, mt5.datetime_to_timestamp(utc_from), 10)

# calculate moving average using TA-lib
close = [rate[4] for rate in rates]
ma = talib.SMA(close, timeperiod=5)

# print moving average values
print(ma)
input("jjjjj")
# shut down connection to MetaTrader 5 terminal
mt5.shutdown()
