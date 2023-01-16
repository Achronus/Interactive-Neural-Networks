from __future__ import annotations
from dataclasses import dataclass

import pandas as pd
import numpy as np

from app.data import ids
from app.data.generate import DataSchema


@dataclass
class DataSource:
    """A data class for retrieving information from a given pandas DataFrame."""
    _data: pd.DataFrame

    def filter(self, x: list[str], y: list[str], labels: list[str]) -> DataSource:
        filtered_data = self._data.query(f"{ids.X_COL_NAME} in {x} and {ids.Y_COL_NAME} in {y} and {ids.LABEL_COL_NAME} in {labels}")
        return DataSource(filtered_data)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_x(self) -> list[str]:
        return self._data[DataSchema.X_AXIS].tolist()

    @property
    def all_y(self) -> list[str]:
        return self._data[DataSchema.Y_AXIS].tolist()

    @property
    def all_labels(self) -> list[str]:
        return self._data[DataSchema.LABELS].tolist()

    @property
    def unique_labels(self) -> list[str]:
        return sorted(set(self.all_labels))

    @property
    def x_and_y(self) -> np.array:
        return self._data[[DataSchema.X_AXIS, DataSchema.Y_AXIS]].to_numpy()
