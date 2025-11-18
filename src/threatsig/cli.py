from __future__ import annotations

import argparse
from typing import List

import pandas as pd
from pandas import Series

from .data import load_data
from .models import Ship, RadarThreat, SonarThreat, DetectionResult
from .analysis.detection import (
    _select_rcs_for_ship,
    _select_acoustic_for_ship,
    evaluate_radar_detection,
    evaluate_sonar_detection,
    result_texts_for_radar,
    result_texts_for_sonar,
)
from .reporting import format_result_text, matrix_markdown


def _ship_from_row(row: Series) -> Ship:
    """
    Convert a pandas Series row from ships.csv into a Ship dataclass.
    Using .at[] helps the type checker to understand that we are accessing
    scalar values instead of sub-Series.
    """
    id_val = row.at["id"]
    name_val = row.at["name"]
    class_val = row.at["class"]
    return Ship(
        id=int(id_val),
        name=str(name_val),
        ship_class=str(class_val),
    )


def _radar_from_row(row: Series) -> RadarThreat:
    """
    Convert a threats.csv row into a RadarThreat dataclass.
    """
    code = row.at["code"]
    name = row.at["name"]
    band = row.at["band"]
    base_rcs = row.at["base_rcs_dbsm"]
    base_range = row.at["base_range_km"]
    max_range = row.at["max_range_km"]

    return RadarThreat(
        code=str(code),
        name=str(name),
        band=str(band),
        base_rcs_dbsm=float(base_rcs),
        base_range_km=float(base_range),
        max_range_km=float(max_range),
    )


def _sonar_from_row(row: Series) -> SonarThreat:
    """
    Convert a threats.csv row into a SonarThreat dataclass.
    """
    code = row.at["code"]
    name = row.at["name"]
    band = row.at["band"]
    noise_floor = row.at["noise_floor_db"]
    det_snr = row.at["detection_snr_db"]

    return SonarThreat(
        code=str(code),
        name=str(name),
        band=str(band),
        noise_floor_db=float(noise_floor),
        detection_snr_db=float(det_snr),
    )


def cmd_list_ships(args: argparse.Namespace) -> None:
    data = load_data()
    print("Available ships:\n")
    for _, row in data.ships.iterrows():
        ship = _ship_from_row(row)
        print(f"- {ship.name} ({ship.ship_class}) [id={ship.id}]")


def cmd_list_threats(args: argparse.Namespace) -> None:
    data = load_data()
    print("Available threats:\n")
    for _, row in data.threats.iterrows():
        print(f"- {row['code']} ({row['type']}), {row['name']} [{row['band']}]")


def _find_ship_by_name(name: str) -> Ship:
    data = load_data()
    sub = data.ships[data.ships["name"].str.lower() == name.lower()]
    if sub.empty:
        raise SystemExit(f"Unknown ship name: {name}")
    return _ship_from_row(sub.iloc[0])


def _find_threat_by_code(code: str):
    data = load_data()
    sub = data.threats[data.threats["code"].str.lower() == code.lower()]
    if sub.empty:
        raise SystemExit(f"Unknown threat code: {code}")
    row = sub.iloc[0]
    ttype = str(row["type"]).lower()
    if ttype == "radar":
        return _radar_from_row(row), "radar"
    elif ttype == "sonar":
        return _sonar_from_row(row), "sonar"
    else:
        raise SystemExit(f"Unsupported threat type: {ttype}")


def _evaluate_single(ship: Ship, threat_code: str) -> DetectionResult:
    data = load_data()
    threat, ttype = _find_threat_by_code(threat_code)

    if ttype == "radar":
        assert isinstance(threat, RadarThreat)
        rcs_dbsm = _select_rcs_for_ship(data.rcs, ship.id)
        det_range = evaluate_radar_detection(rcs_dbsm, threat)
        en, de = result_texts_for_radar(ship.name, threat, det_range)
        return DetectionResult(
            ship_name=ship.name,
            threat_code=threat.code,
            threat_name=threat.name,
            threat_type="radar",
            metric_value=round(det_range, 1),
            metric_label="Detection range [km] / Erfassungsreichweite [km]",
            description_en=en,
            description_de=de,
        )
    else:
        assert isinstance(threat, SonarThreat)
        acoustic_db = _select_acoustic_for_ship(data.acoustic, ship.id)
        category = evaluate_sonar_detection(acoustic_db, threat)
        en, de = result_texts_for_sonar(ship.name, threat, category)
        label_map = {"low": "low / niedrig", "medium": "medium / mittel", "high": "high / hoch"}
        metric_value = label_map.get(category, category)
        return DetectionResult(
            ship_name=ship.name,
            threat_code=threat.code,
            threat_name=threat.name,
            threat_type="sonar",
            metric_value=metric_value,
            metric_label="Detection probability / Entdeckungswahrscheinlichkeit",
            description_en=en,
            description_de=de,
        )


def cmd_evaluate(args: argparse.Namespace) -> None:
    ship = _find_ship_by_name(args.ship_name)
    result = _evaluate_single(ship, args.threat_code)
    print(format_result_text(result))


def cmd_matrix(args: argparse.Namespace) -> None:
    data = load_data()
    results: List[DetectionResult] = []
    for _, row in data.ships.iterrows():
        ship = _ship_from_row(row)
        res = _evaluate_single(ship, args.threat_code)
        results.append(res)
    md = matrix_markdown(results)
    print(md)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="threatsig",
        description="Threat vs. Signature Explorer (synthetic data demo)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_ls = subparsers.add_parser("list-ships", help="List all available ships.")
    p_ls.set_defaults(func=cmd_list_ships)

    p_lt = subparsers.add_parser("list-threats", help="List all available threats.")
    p_lt.set_defaults(func=cmd_list_threats)

    p_eval = subparsers.add_parser(
        "evaluate",
        help="Evaluate a single ship against a given threat.",
    )
    p_eval.add_argument("ship_name", help="Name of the ship, e.g. 'Alpha'.")
    p_eval.add_argument("threat_code", help="Threat code, e.g. 'radar_basic'.")
    p_eval.set_defaults(func=cmd_evaluate)

    p_matrix = subparsers.add_parser(
        "matrix",
        help="Create a Markdown matrix for all ships vs. one threat.",
    )
    p_matrix.add_argument("threat_code", help="Threat code, e.g. 'radar_basic'.")
    p_matrix.set_defaults(func=cmd_matrix)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()