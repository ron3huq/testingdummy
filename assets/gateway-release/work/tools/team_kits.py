"""Outfield kit choices from the current native registry, then ported data.

Never invent a third kit for every AI team. Most teams only have two outfield
kits; a nonexistent +2 ID lets the client fall back to a plain uniform. The
registry describes valid slots/palettes and does not assert texture licensing.
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

import ziru_data

STRIDE = 16384
CATALOG_FILE = Path(__file__).resolve().parents[2] / 'outputs/reference/efootxi-kit-catalog.json'


@functools.lru_cache(maxsize=1)
def catalog() -> dict:
    try:
        document = json.loads(CATALOG_FILE.read_text(encoding='utf8'))
    except (OSError, ValueError):
        return {}
    if not isinstance(document, dict) or document.get('schema') != 1:
        return {}
    teams = document.get('teams')
    return teams if isinstance(teams, dict) else {}


def _ids(team: int, records) -> list[int]:
    if not isinstance(records, list):
        return []
    result = []
    for record in records:
        if not isinstance(record, dict):
            continue
        slot, uid = record.get('slot'), record.get('id')
        if (type(slot) is int and 0 <= slot < 16 and type(uid) is int
                and uid == team * STRIDE + slot and uid > 0 and uid not in result):
            result.append(uid)
    return result


def uniform_ids(team: int) -> list[int]:
    """Existing outfield slots for this exact native team, in source order."""
    if type(team) is not int or team <= 0:
        return []
    current = _ids(team, catalog().get(str(team)))
    if current:
        return current
    # UniColor is not a complete registry of generic/unlicensed-team kits.
    # Those clubs can still have their pair in the ported match-team data.
    try:
        ported = _ids(team, (ziru_data.teams().get(str(team)) or {}).get('kits'))
    except ziru_data.NotPorted:
        ported = []
    if ported:
        return ported
    # Retain the existing compatibility pair when neither source has this team.
    # An absent palette entry is not proof the native client has no team assets.
    return [team * STRIDE, team * STRIDE + 1]
