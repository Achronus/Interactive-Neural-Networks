import random
from functools import reduce, partial
from typing import Callable

import pandas as pd
import numpy as np

from app.data import ids

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    X_AXIS = 'x'
    Y_AXIS = 'y'
    LABELS = 'label'


def create_sample_data(n_points: int, seed: int = 362, threshold: int = 11) -> pd.DataFrame:
    """
    Generate a set of random sample data.

    :param n_points: (int) total number of sample data
    :param seed: (int) number for random seed
    :param threshold: (int) maximum value of sample data (exclusive, divided by 10)
    """
    random.seed(seed)
    all_points = [(a/10, b/10) for a in range(threshold) for b in range(threshold)]
    sample = sorted(random.sample(all_points, n_points))

    return pd.DataFrame(sample, columns=[DataSchema.X_AXIS, DataSchema.Y_AXIS])


def create_labels(df: pd.DataFrame, n_positive: int) -> pd.DataFrame:
    """
    Create an array of labels and set them to a unique column in the given DataFrame.
    Returns the updated DataFrame.

    :param df: (pd.DataFrame) a DataFrame of sample data
    :param n_positive: (int) number of positive labels
    """
    positive_labels = np.array([ids.LABEL_ONE for _ in range(n_positive)], dtype=str)
    negative_labels = np.array([ids.LABEL_TWO for _ in range(df.shape[0] - n_positive)], dtype=str)
    labels = np.concatenate((positive_labels, negative_labels))

    df[DataSchema.LABELS] = labels
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    """Creates a lambda function that applies a set of functions in sequential order."""
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def set_data(n_points: int, n_positive: int, seed: int = 362, threshold: int = 11) -> pd.DataFrame:
    """Create data and iterate it through the preprocessor pipeline."""
    data = create_sample_data(n_points, seed, threshold)

    preprocessor = compose(
        partial(create_labels, n_positive=n_positive)
    )
    return preprocessor(data)
