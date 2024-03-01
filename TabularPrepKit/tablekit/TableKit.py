import polars as pl
import numpy as np
from tablekit.core import *

class TableKit:
    def __init__(self, data: pl.DataFrame) -> None:
        self.data = data