import pandas as pd
from math import ceil
from random import randint

from normalize import normalize


class Data:
    def __init__(self, initial_data, target):
        self.initial_data = initial_data
        self.target = target

    @property
    def min_vals(self) -> dict:
        res = {}
        for column in self.initial_data.columns:
            if column != 'id':
                res[column] = min(self.initial_data[column].tolist())
        return res

    @property
    def max_vals(self) -> dict:
        res = {}
        for column in self.initial_data.columns:
            if column != 'id':
                res[column] = max(self.initial_data[column].tolist())
        return res

    @property
    def normalized_data(self) -> pd.DataFrame:
        df_dict = dict()
        for column in self.initial_data.columns:
            if column not in ['id', self.target]:
                df_dict[column] = normalize(features=self.initial_data[column].tolist(), from_val=-1, to_val=1)
        df_dict[self.target] = self.initial_data[self.target].tolist()
        return pd.DataFrame.from_dict(df_dict)

    def normalize(self, features):
        if len(features) != len(self.initial_data.columns) - 1:
            raise ValueError(
                f'features list must have same length as count of columns in initial dataset without id and target.'
                f' Got {len(features)} and {len(self.initial_data.columns)} instead.')
        res = []
        for column, feature in zip(
                [feature for feature in list(self.initial_data.columns) if feature not in ['id', self.target]],
                features):
            feature -= self.min_vals[column]
            res.append(feature / (self.max_vals[column] - self.min_vals[column]) * 2 - 1)
        return res

    def train_test_split(self, test_set_size: float):
        df = self.normalized_data
        indexes = list(self.normalized_data.index)
        if not 0 <= test_set_size <= 1:
            raise ValueError(f'Size of test split must be in range (0, 1). Got {test_set_size} instead.')

        test_set_size_in_rows = ceil(len(df) * test_set_size)
        test_set, real_classes = list(), list()
        for _ in range(test_set_size_in_rows):
            idx = randint(0, len(indexes)-1)
            feature_list = list()
            for column in df.columns:
                if column != self.target:
                    feature_list.append(df.loc[indexes[idx], column])
            test_set.append(tuple(feature_list))
            real_classes.append(df.loc[indexes[idx], self.target])
            del indexes[idx]

        train_set = dict()
        for idx in indexes:
            feature_list = list()
            for column in df.columns:
                if column != self.target:
                    feature_list.append(df.loc[idx, column])
            train_set[tuple(feature_list)] = df.loc[idx, self.target]

        return train_set, tuple(test_set), tuple(real_classes)

