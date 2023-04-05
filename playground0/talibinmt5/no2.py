import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
# Init MT5 
mt5.initialize()


# Get the EURUSD M1 data
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M1
start_time = pd.Timestamp("2022-01-01")
end_time = dt.datetime.now()

rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(rates)
df["time"] = pd.to_datetime(df["time"], unit="s")
df.set_index("time", inplace=True)

# Calculate the moving average using Matplotlib
ma = df["close"].rolling(window=20).mean()

# Plot the data and the moving average
plt.plot(df["close"], label="Close")
# plt.plot(xama, label="MA")
plt.legend()
plt.show()

# Shutdown MT5 connection
mt5.shutdown()