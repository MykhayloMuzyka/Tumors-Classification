from typing import List, Tuple


def normalize(features: List[float | int] or Tuple[float | int], from_val: float, to_val: float) \
        -> List[float | int]:
    """
    Normalize feature list in range from from_val to to_val
    :param features: list of features
    :param from_val: minimal value in normalized list
    :param to_val: maximal value in normalized list
    :return: normalized list
    """
    if from_val >= to_val:
        raise ValueError(f"from_val must by less than to_val. Got {from_val} and {to_val} instead.")
    if len(features) == 0:
        return list()
    dif = to_val - from_val
    max_val = max(features)
    min_val = min(features)
    obj = [i - min_val for i in features]
    res = list()
    for feature in obj:
        # print(max_val, min_val)
        res.append(feature / (max_val - min_val) * dif + from_val)
    return res



