from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ThreatType = Literal["radar", "sonar"]


@dataclass
class Ship:
    id: int
    name: str
    ship_class: str


@dataclass
class RadarThreat:
    code: str
    name: str
    band: str
    base_rcs_dbsm: float
    base_range_km: float
    max_range_km: float


@dataclass
class SonarThreat:
    code: str
    name: str
    band: str
    noise_floor_db: float
    detection_snr_db: float


@dataclass
class DetectionResult:
    ship_name: str
    threat_code: str
    threat_name: str
    threat_type: ThreatType
    metric_value: float | str
    metric_label: str
    description_en: str
    description_de: str
