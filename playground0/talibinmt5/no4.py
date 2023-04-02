import talib
import MetaTrader5 as mt5
import matplotlib.pyplot as plt

# connect to MetaTrader5
mt5.initialize()

# get the EURUSD H1 historical data
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1
eurusd = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1000)

# calculate the RSI values using TA-Lib
rsi = talib.RSI(eurusd['close'], timeperiod=14)

# plot the RSI values on a chart
plt.plot(rsi)
plt.title("RSI Indicator")
plt.ylabel("RSI")
plt.xlabel("Time")
plt.show()

# disconnect from MetaTrader5
mt5.shutdown()