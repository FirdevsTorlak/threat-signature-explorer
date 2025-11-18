from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .config import SHIPS_CSV, RCS_CSV, ACOUSTIC_CSV, THREATS_CSV


@dataclass
class DataBundle:
    ships: pd.DataFrame
    rcs: pd.DataFrame
    acoustic: pd.DataFrame
    threats: pd.DataFrame


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def load_data() -> DataBundle:
    ships = _load_csv(SHIPS_CSV)
    rcs = _load_csv(RCS_CSV)
    acoustic = _load_csv(ACOUSTIC_CSV)
    threats = _load_csv(THREATS_CSV)
    return DataBundle(ships=ships, rcs=rcs, acoustic=acoustic, threats=threats)
