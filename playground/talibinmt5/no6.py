import MetaTrader5 as mt5
import talib
import numpy as np 

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# copy the last 14 close prices of a currency pair
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M15, 0, 14)
rates_dfs = np.array(rates)
# close_prices = [rates_df[4] for rates_df in rates_dfs]
close_prices = []
# for rate in rates.as:
#     close_prices.append(rate)
# calculate the RSI using TA-Lib
rsi = talib.RSI(close_prices, timeperiod=14)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()