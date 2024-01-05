from typing import Annotated
from dataclasses import dataclass


@dataclass
class ValueRange:
    min: float
    max: float


probability = Annotated[float, ValueRange(0.0, 1.0)]
