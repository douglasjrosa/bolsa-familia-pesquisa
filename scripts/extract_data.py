#!/usr/bin/env python3
"""Build a validated master snapshot note for reproducibility."""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "2024_master.csv")
sources = json.loads((ROOT / "data" / "sources_registry.json").read_text())
print(f"metrics={len(df)} sources={len(sources['sources'])}")
key = [
    "bf_cost_annual",
    "interest_consolidated_bc",
    "tax_expenditures_dirbi_total",
    "amendments_committed",
    "military_expenses_system",
]
for k in key:
    v = float(df.loc[df.metric == k, "value"].iloc[0])
    print(f"{k}: R$ {v/1e9:.2f} bi")
