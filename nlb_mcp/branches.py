"""Branch code helpers using static C005 list."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

BRANCHES_PATH = Path(__file__).resolve().parent.parent / "resources" / "branches.json"

try:
    BRANCHES: List[Dict[str, str]] = json.loads(BRANCHES_PATH.read_text())
except Exception:
    BRANCHES = []


def find_branch(code: str) -> Dict[str, str] | None:
    code_lower = code.lower()
    for entry in BRANCHES:
        if entry.get("code", "").lower() == code_lower:
            return entry
    return None
