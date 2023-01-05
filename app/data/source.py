from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.data.generate import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(self, x: list[str], y: list[str], labels: list[str]) -> DataSource:
        filtered_data = self._data.query(f"x in {x} and y in {y} and label in {labels}")
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
