# Threat vs. Signature Explorer

A small, self-contained Python toolkit to explore how **synthetic ship signatures**
(RCS and acoustic levels) interact with **simplified radar and sonar threat models**.

The goal is *not* to model real systems, but to show in a transparent way how
assumptions about threat performance can be linked to a signature database and
turned into **detection range estimates** and **qualitative risk assessments**.

The project is designed as a compact, professional example for:

- working with **relational-style tabular data** (CSV + pandas),
- basic **radar / sonar detection modelling** on synthetic data,
- generating **CLI-based reports** (CSV / Markdown),
- creating simple **visualisations** with matplotlib.

> All data and models in this repository are **fully synthetic** and serve
> demonstration and training purposes only.

## 1. Project structure

```text
threat-signature-explorer/
  README.md
  requirements.txt
  .gitignore
  .vscode/
    settings.json
    launch.json
  data/
    ships.csv
    rcs_signatures.csv
    acoustic_signatures.csv
    threats.csv
  src/
    threatsig/
      __init__.py
      config.py
      data.py
      models.py
      reporting.py
      cli.py
      analysis/
        __init__.py
        detection.py
  docs/
    figures/
      (created by export_figures.py)
  export_figures.py
```

## 2. Installation

Create and activate a virtual environment (recommended).

On Linux/macOS (bash):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Quickstart

```bash
cd threat-signature-explorer
```

List ships and threats:

```bash
python -m threatsig.cli list-ships
python -m threatsig.cli list-threats
```

Evaluate a ship vs. radar:

```bash
python -m threatsig.cli evaluate Alpha radar_basic
```

Evaluate a ship vs. sonar:

```bash
python -m threatsig.cli evaluate Alpha sonar_basic
```

Create a Markdown matrix:

```bash
python -m threatsig.cli matrix radar_basic
```

## 4. Example figures

```bash
python export_figures.py
```

This will create `docs/figures/radar_detection_radar_basic.png` with bilingual
labels (English / German).

## 5. Short German summary

Dieses Projekt demonstriert, wie sich **synthetische Schiffssignaturen**
(RCS und akustische Pegel) mit einfachen **Radar- und Sonar-Bedrohungs-
modellen** verknüpfen lassen, um daraus geschätzte **Erfassungsreichweiten**
und qualitative Einschätzungen der Entdeckungswahrscheinlichkeit abzuleiten.
