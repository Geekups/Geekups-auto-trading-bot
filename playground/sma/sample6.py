import MetaTrader5 as mt5
import talib

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# set the symbol and timeframe
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M1

# get the OHLC data from MT5
ohlcv = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)

# extract the close prices from the OHLC data
close = [x[1] for x in ohlcv]

# calculate the moving average using TA-Lib
ma = talib.SMA(close, timeperiod=20)

# print the moving average values
print(ma)

# shut down the connection to MetaTrader 5 terminal
mt5.shutdown()