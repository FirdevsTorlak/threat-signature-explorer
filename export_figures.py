from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from threatsig.data import load_data  # type: ignore
from threatsig.cli import _evaluate_single, _ship_from_row  # type: ignore
from threatsig.config import BASE_DIR  # type: ignore


def export_radar_detection_bar(threat_code: str = "radar_basic") -> Path:
    data = load_data()
    results = []
    for _, row in data.ships.iterrows():
        ship = _ship_from_row(row)
        res = _evaluate_single(ship, threat_code)
        if res.threat_type == "radar":
            results.append(res)

    if not results:
        raise RuntimeError(f"No radar results for threat '{threat_code}'.")

    ships = [r.ship_name for r in results]
    ranges = [float(r.metric_value) for r in results]

    fig, ax = plt.subplots()
    ax.bar(ships, ranges)
    ax.set_xlabel("Ship / Schiff")
    ax.set_ylabel("Range [km] / Reichweite [km]")
    ax.set_title("Radar detection range / Radar-Erfassungsreichweite")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()

    figures_dir = BASE_DIR / "docs" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    out_path = figures_dir / f"radar_detection_{threat_code}.png"
    fig.savefig(str(out_path), dpi=300, bbox_inches="tight")  # 👈 burada str(...)
    plt.close(fig)

    print(f"Saved radar detection figure to: {out_path}")
    return out_path


def main() -> None:
    export_radar_detection_bar("radar_basic")


if __name__ == "__main__":
    main()