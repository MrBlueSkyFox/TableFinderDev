from typing import Union

from pydantic import BaseModel


class Cell(BaseModel):
    x_min: Union[float, int]
    y_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]


class CellWithText(Cell):
    text: str


class TableBox(BaseModel):
    confidence: float
    box: Cell


class TableStructureOrderedWithText(BaseModel):
    cells: list[list[CellWithText]]
