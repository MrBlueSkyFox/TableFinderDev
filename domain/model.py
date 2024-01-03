from __future__ import annotations
# TODO
# 1) Create class to represent Table Coordinates
# 2) Create class to represent Table Structure coordinates
# 3) Create class to represent Table Structure
#                       with cells boxes in right order
# 4)Create class to represent Table Structure
#                       with cells boxes and text in right order


from dataclasses import dataclass, field


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
class TableProperty:
    number_of_columns: int = field(init=False)
    number_of_rows: int = field(init=False)


@dataclass
class TableStructureOrdered(TableProperty):
    cells: list[list[Cell]]

    @property
    def number_of_columns(self) -> int:
        return len(self.cells[0])

    @property
    def number_of_rows(self) -> int:
        return len(self.cells)


class TableStructureOrderedWithText(TableStructureOrdered):
    cells: list[list[CellWithText]]


@dataclass(frozen=True)
class Cell:
    x_min: float | int
    y_min: float | int
    x_max: float | int
    y_max: float | int


@dataclass(frozen=True)
class CellWithText(Cell):
    text: str
