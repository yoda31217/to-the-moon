def to_json(dictionary: dict):
    key_value_strs = [f'"{key}": {value}' for (key, value) in dictionary.items()]
    key_values_str = "\n    ".join(key_value_strs)
    return f"{{\n    {key_values_str}\n}}"
