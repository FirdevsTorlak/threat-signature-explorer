from __future__ import annotations
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = BASE_DIR / "data"

SHIPS_CSV: Path = DATA_DIR / "ships.csv"
RCS_CSV: Path = DATA_DIR / "rcs_signatures.csv"
ACOUSTIC_CSV: Path = DATA_DIR / "acoustic_signatures.csv"
THREATS_CSV: Path = DATA_DIR / "threats.csv"
