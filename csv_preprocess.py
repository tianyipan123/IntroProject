import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import util

raw = pd.read_csv("interval_data.csv")
raw["time"] = pd.to_datetime(raw["time"])
time_range = raw["time"].unique()
symbol = raw["trade_symbol"].unique()
types = ["open_mid_price", "close_mid_price", "high_price", "low_price",
         "volume", "vwap", "adjustment", "type"]
data_dict = {}
#%%
start_time = time.time()
for info_type in types:
    type_data = pd.DataFrame(raw[["trade_symbol", "time", info_type]])
    result = []
    for ticker in symbol:
        ticker_data = type_data[type_data["trade_symbol"] == ticker]
        series = ticker_data[["time", info_type]]
        series.set_index("time", inplace=True)
        series.set_axis([ticker], axis=1, inplace=True)
        result.append(series)
    output = pd.concat(result, axis=1)
    data_dict[info_type] = output

end_time = time.time()
print("total time spend on data processing is " + str(end_time - start_time))
#%%
start_time = time.time()
close_mid = data_dict["close_mid_price"]
signal_result = []
for ticker in symbol:
    series = close_mid[ticker]
    signal = util.go_up(series)
    signal.set_axis([ticker], axis=1, inplace=True)
    signal.set_index(time_range, inplace=True)
    signal_result.append(signal)
go_up_signals = pd.concat(signal_result, axis=1)
end_time = time.time()
print("total time spend on go up signal is " + str(end_time - start_time))
print(np.count_nonzero(go_up_signals))
#%%
profits = []
for ticker in symbol:
    profits.append(util.count_profit(close_mid[ticker], go_up_signals[ticker]))
profits = pd.Series(profits, index=symbol, name="profit")
profits = profits.multiply(100)

plt.figure()
plt.hist(profits, bins=20)
plt.show()
