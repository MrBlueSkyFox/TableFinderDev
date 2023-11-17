from dataclasses import dataclass


@dataclass
class FoundedTableObjects:
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    pos: int  # 1 col 2 rows
