from pandas import DataFrame, Series


def target_action(prices: Series, price_increase_ratio: float):
    price_decrease_ratio = 1.0 - (price_increase_ratio - 1.0)

    price_0 = prices.iloc[0]
    increase_price = price_0 * price_increase_ratio
    decrease_price = price_0 * price_decrease_ratio

    for i in range(1, prices.shape[0]):
        price_i = prices.iloc[i]
        if price_i >= increase_price:
            return 1
        elif price_i <= decrease_price:
            return -1

    return 0


def calculate_target_actions(prices: Series, window: int, price_increase_ratio: float):
    return (
        prices.shift(-window)
        .rolling(window + 1)
        .apply(target_action, args=(price_increase_ratio,))
    )


def calculate_and_set_target_actions_feature(
    features: DataFrame, window: int, price_increase_ratio: float
):
    features["target_actions"] = calculate_target_actions(
        features["close_price"], window, price_increase_ratio
    )
