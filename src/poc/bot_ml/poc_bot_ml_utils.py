def will_values_increase_or_decrease(values, increase_ratio):
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
