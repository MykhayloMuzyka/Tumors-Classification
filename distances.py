from math import sqrt, fabs
from typing import Tuple, List

from numpy import array


def euclidean(obj1: List[float or int] or Tuple[float or int],
              obj2: List[float or int] or Tuple[float or int],
              weights: List[float or int] or Tuple[float or int]) -> float:
    """
    Counts distance between two objects with features obj1 and obj2 counted by euclidean formula
    :param weights: weights of features
    :param obj1: list of features of first object
    :param obj2: list of features of second object
    :return: distance between objects counted by euclidean formula
    """
    if len(obj1) != len(obj2):
        raise ValueError(f"Length of objects must be same. Got {len(obj1)} and {len(obj2)} instead.")
    return sqrt(sum(((array(obj1) - array(obj2)) * weights) ** 2))


def chebyshev(obj1: List[float or int] or Tuple[float or int],
              obj2: List[float or int] or Tuple[float or int]) -> float:
    """
    Counts distance between two objects with features obj1 and obj2 counted by chebyshev formula
    :param obj1: list of features of first object
    :param obj2: list of features of second object
    :return: distance between objects counted by chebyshev formula
    """
    if len(obj1) != len(obj2):
        raise ValueError(f"Length of objects must be same. Got {len(obj1)} and {len(obj2)} instead.")
    return max(map(lambda a, b: fabs(a - b), obj1, obj2))


def manhattan(obj1: List[float or int] or Tuple[float or int],
              obj2: List[float or int] or Tuple[float or int]) -> float:
    """
    Counts distance between two objects with features obj1 and obj2 counted by manhattan formula
    :param obj1: list of features of first object
    :param obj2: list of features of second object
    :return: distance between objects counted by manhattan formula
    """
    if len(obj1) != len(obj2):
        raise ValueError(f"Length of objects must be same. Got {len(obj1)} and {len(obj2)} instead.")
    return sum(map(lambda a, b: fabs(a - b), obj1, obj2))


def minkowski(obj1: List[float or int] or Tuple[float or int],
              obj2: List[float or int] or Tuple[float or int], p: float) -> float:
    """
    Counts distance between two objects with features obj1 and obj2 counted by minkowski formula
    :param obj1: list of features of first object
    :param obj2: list of features of second object
    :param p: parameter of minkowski formula. Show the power of difference between every feature of given objects and
              inversely proportional power of sum of these differences
    :return: distance between objects counted by minkowski formula
    """
    if len(obj1) != len(obj2):
        raise ValueError(f"Length of objects must be same. Got {len(obj1)} and {len(obj2)} instead.")
    if p <= 0:
        raise ValueError(f"p must be positive number. Got {p} instead.")
    return sum(map(lambda a, b: fabs(a - b) ** p, obj1, obj2)) ** (1 / p)
