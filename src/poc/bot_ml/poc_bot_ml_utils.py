from pandas import Series


def will_values_increase_or_decrease(values: Series, increase_ratio: float):
    decrease_ratio = 1.0 - (increase_ratio - 1.0)

    value_0 = values.iloc[0]
    increase_value = value_0 * increase_ratio
    decrease_value = value_0 * decrease_ratio

    for i in range(1, values.shape[0]):
        value_i = values.iloc[i]
        if value_i >= increase_value:
            return 1
        elif value_i <= decrease_value:
            return -1

    return 0


def calculate_target_actions(prices: Series, window: int, price_increase_ratio: float):
    return (
        prices.shift(-window)
        .rolling(window + 1)
        .apply(will_values_increase_or_decrease, args=(price_increase_ratio,))
    )
