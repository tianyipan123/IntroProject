import pandas as pd
import numpy as np
import math
from typing import Union


def go_up(ds: pd.Series) -> pd.DataFrame:
    """Return a 1-D dataframe containing buying and selling signal.
    Here does not consider short-sell.
    """
    ds = ds.copy()
    mean = ds.ewm(com = 10, min_periods=5).mean()
    pct_change = pd.Series(mean).pct_change()

    # 1 for buy, 0 for hold, -1 for sell
    signal = []
    current = 0
    for pct in pct_change:
        if math.isnan(pct):
            if current == 1:
                signal[-1] = 0
                signal.append(0)
                current = 0
            else:
                signal.append(0)
            continue
        if current == 1:
            if pct > -0.1:
                signal.append(0)
            else:
                signal.append(-1)
                current = 0
        elif current == 0:
            if signal[-1] == -1 and pct > 0.03:
                signal.append(1)
                current = 1
            elif signal[-1] == 0 and pct > 0.01:
                signal.append(1)
                current = 1
            else:
                signal.append(0)
    return pd.DataFrame(signal)


def count_profit(price: pd.Series, signal: pd.Series) -> Union[float, None]:
    """Return the percentage profit.
    """
    duration = len(price)
    if duration != len(signal):
        print("price not match with signal!!")
        return None
    start_price = -1
    history = []
    close = False
    money_add = []
    nonzero_signal = np.nonzero(signal.to_numpy())[0]
    if len(nonzero_signal) > 0:
        first_price = price[nonzero_signal[0]]
    else:
        return 0
    for i in range(duration):
        current = signal[i]
        if current == 1:
            start_price = price[i]
            history.append(start_price)
            close = False
        elif current == -1:
            money_add.append(price[i] - start_price)
            close = True
        if i == duration - 1:
            if not close:
                money_add.append(price[price.last_valid_index()] - start_price)
    return sum(money_add) / first_price
