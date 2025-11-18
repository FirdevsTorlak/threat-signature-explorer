from __future__ import annotations

from typing import Iterable

from .models import DetectionResult


def format_result_text(result: DetectionResult) -> str:
    lines = [
        f"[EN] {result.description_en}",
        f"[DE] {result.description_de}",
    ]
    return "\n".join(lines)


def matrix_markdown(results: Iterable[DetectionResult]) -> str:
    results = list(results)
    if not results:
        return "No results available.\n"
    threat_code = results[0].threat_code
    threat_type = results[0].threat_type
    header = f"### Ship vs. threat matrix for `{threat_code}` ({threat_type})\n\n"
    header += "| Ship | Metric | Value |\n"
    header += "|------|--------|-------|\n"
    rows = [f"| {r.ship_name} | {r.metric_label} | {r.metric_value} |" for r in results]
    return header + "\n".join(rows) + "\n"
