from __future__ import annotations

import pandas as pd

from ..models import RadarThreat, SonarThreat


def _select_rcs_for_ship(rcs_df: pd.DataFrame, ship_id: int) -> float:
    sub = rcs_df[rcs_df["ship_id"] == ship_id]
    if sub.empty:
        raise ValueError(f"No RCS data for ship_id={ship_id}")
    return float(sub["rcs_dbsm"].max())


def _select_acoustic_for_ship(acoustic_df: pd.DataFrame, ship_id: int, band_label: str = "125 Hz") -> float:
    sub = acoustic_df[(acoustic_df["ship_id"] == ship_id) & (acoustic_df["band_label"] == band_label)]
    if not sub.empty:
        return float(sub["level_db"].iloc[0])
    sub_all = acoustic_df[acoustic_df["ship_id"] == ship_id]
    if sub_all.empty:
        raise ValueError(f"No acoustic data for ship_id={ship_id}")
    return float(sub_all["level_db"].mean())


def evaluate_radar_detection(rcs_dbsm: float, threat: RadarThreat) -> float:
    delta_db = rcs_dbsm - threat.base_rcs_dbsm
    scale = 10.0 ** (delta_db / 40.0)
    est_range = threat.base_range_km * scale
    est_range = max(0.0, min(est_range, threat.max_range_km))
    return float(est_range)


def evaluate_sonar_detection(acoustic_level_db: float, threat: SonarThreat) -> str:
    relative = acoustic_level_db - threat.noise_floor_db
    if relative < threat.detection_snr_db:
        return "low"
    elif relative < threat.detection_snr_db + 10.0:
        return "medium"
    else:
        return "high"


def result_texts_for_radar(ship_name: str, threat: RadarThreat, det_range_km: float) -> tuple[str, str]:
    txt_en = (
        f"Estimated radar detection range for {ship_name} with threat "
        f"'{threat.code}' is about {det_range_km:.1f} km "
        f"(max {threat.max_range_km:.1f} km, synthetic RCS-based estimate)."
    )
    txt_de = (
        f"Geschätzte Radar-Erfassungsreichweite für {ship_name} mit Bedrohung "
        f"'{threat.code}' beträgt ca. {det_range_km:.1f} km "
        f"(Maximalreichweite {threat.max_range_km:.1f} km, "
        f"basierend auf synthetischen RCS-Daten)."
    )
    return txt_en, txt_de


def result_texts_for_sonar(ship_name: str, threat: SonarThreat, category: str) -> tuple[str, str]:
    if category == "low":
        en = (
            f"Estimated detection probability for {ship_name} with sonar threat "
            f"'{threat.code}' is LOW (signal close to or below noise floor)."
        )
        de = (
            f"Die geschätzte Entdeckungswahrscheinlichkeit für {ship_name} mit "
            f"Sonar-Bedrohung '{threat.code}' ist NIEDRIG "
            f"(Signal liegt nahe am oder unter dem Geräuschpegel)."
        )
    elif category == "medium":
        en = (
            f"Estimated detection probability for {ship_name} with sonar threat "
            f"'{threat.code}' is MEDIUM (moderate margin above noise floor)."
        )
        de = (
            f"Die geschätzte Entdeckungswahrscheinlichkeit für {ship_name} mit "
            f"Sonar-Bedrohung '{threat.code}' ist MITTEL "
            f"(moderater Abstand über dem Geräuschpegel)."
        )
    else:
        en = (
            f"Estimated detection probability for {ship_name} with sonar threat "
            f"'{threat.code}' is HIGH (signal clearly above noise floor)."
        )
        de = (
            f"Die geschätzte Entdeckungswahrscheinlichkeit für {ship_name} mit "
            f"Sonar-Bedrohung '{threat.code}' ist HOCH "
            f"(Signal deutlich über dem Geräuschpegel)."
        )
    return en, de
