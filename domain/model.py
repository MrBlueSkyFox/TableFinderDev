from __future__ import annotations
# TODO
# 1) Create class to represent Table Coordinates
# 2) Create class to represent Table Structure coordinates
# 3) Create class to represent Table Structure
#                       with cells boxes in right order
# 4)Create class to represent Table Structure
#                       with cells boxes and text in right order


from dataclasses import dataclass


@dataclass
class TableBox:
    box: Cell
    confidence: float


@dataclass
class TableStructure:
    rows: list[Cell]
    columns: list[Cell]
    header: list[Cell]


@dataclass
class TableStructureOrdered:
    cells: list[list[Cell]]


@dataclass(frozen=True)
class Cell:
    x_min: float | int
    y_min: float | int
    x_max: float | int
    y_max: float | int


@dataclass(frozen=True)
class CellWithText(Cell):
    text: str
