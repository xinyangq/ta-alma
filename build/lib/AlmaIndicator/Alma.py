import math
import numpy as np
import pandas


# calculate single alma of each day
# prices, Series, close price of the stock
# window, int, window size
# offset, float, offset value
# sigma, int, sigma
# alma_single, float, the alma value of the single day
def _single_alma(prices, window, offset, sigma):
    # if data length is less than window, return None
    if len(prices) < 9:
        return None

    # get weights
    m = int(offset * (window - 1))
    s = window / sigma
    weights = np.array(range(window))
    temp = -((weights - m) ** 2) / (2 * (s ** 2))
    weights = [math.exp(item) for item in temp]
    weights = np.array(weights)

    # calculate alma
    weighted_sum = weights * prices  # weighted price
    alma_single = weighted_sum.sum() / weights.sum()  # weighted average price

    return alma_single


# calculate whole alma of the whole series
# prices, Series, close price of the stock
# window, int, window size
# offset, float, offset value
# sigma, int, sigma
# alma, series, alma average line
def get_alma(prices, window=9, offset=0.85, sigma=6):
    # calculate alma, series
    alma = prices.rolling(window=window).apply(_single_alma, args=(window, offset, sigma,))

    # replace inf and -inf with nan
    alma = alma.replace([np.inf, -np.inf], np.nan)

    return alma


if __name__ == '__main__':
    price = pandas.Series(list(range(19)))
    alma_line = get_alma(price, window=9, offset=0.85, sigma=6)
    i = 1
