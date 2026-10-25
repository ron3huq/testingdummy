"""Native base overall rating in canonical 147-parameter / GK..CF position order.

Recovered from original ARM64 0x82b5784 (wrapper 0x82b5bb0), table 0xcd7170.
The generic parameter names were independently read from the enum registration
0x75eac8c: e.g. 26 CONSCIOUS_DEFENSE, 40 STAMINA. Flat rating-model ordinals
are a separate enum and must never index an owned card's wire parameters.
This neutral rating excludes manager/conditional booster effects by default;
an explicit common stat-boost mapping can be supplied for both candidates.
"""
from __future__ import annotations

PARAMETERS = (47, 14, 18, 17, 19, 21, 22, 20, 27, 28, 23, 15, 24, 25,
              37, 34, 38, 35, 36, 39, 16, 32, 29, 30, 31, 40, 33, 26)
SOURCE_SHA256 = '2cea0c85344d7d7f295aea1c2353621f02db78dbccd888a0a21a0508ac330659'
WEIGHTS_SHA256 = '34d08a4df83cc1a8f224f3545df64c5f7f90c8db5d384c553d68e1b4548f4d76'
WEIGHTS = (
    (186, 136, 49, 49, 61, 37, 12, 12, 37, 49, 49, 62, 99),
    (0, 14, 61, 61, 61, 98, 98, 98, 171, 159, 159, 173, 210),
    (13, 27, 86, 86, 122, 171, 171, 171, 196, 159, 159, 210, 123),
    (0, 14, 61, 61, 37, 98, 110, 122, 122, 159, 159, 123, 62),
    (0, 0, 37, 37, 24, 49, 73, 61, 73, 86, 86, 86, 37),
    (27, 41, 61, 61, 122, 208, 135, 135, 196, 73, 73, 99, 37),
    (40, 68, 147, 147, 122, 159, 196, 196, 159, 98, 98, 74, 12),
    (0, 27, 24, 24, 37, 73, 86, 86, 184, 159, 159, 284, 358),
    (0, 14, 24, 24, 12, 12, 24, 24, 12, 12, 12, 12, 12),
    (0, 14, 24, 24, 12, 12, 24, 24, 12, 12, 12, 12, 12),
    (0, 55, 24, 24, 61, 24, 12, 12, 24, 24, 24, 25, 62),
    (13, 286, 147, 147, 220, 86, 49, 49, 24, 12, 12, 0, 0),
    (0, 191, 86, 86, 122, 86, 24, 24, 24, 12, 12, 12, 12),
    (0, 82, 37, 37, 98, 37, 12, 12, 12, 12, 12, 12, 12),
    (53, 27, 24, 24, 49, 73, 24, 24, 73, 61, 61, 99, 123),
    (13, 136, 220, 220, 61, 61, 196, 196, 98, 220, 220, 86, 99),
    (40, 150, 184, 184, 61, 86, 159, 159, 86, 159, 159, 99, 123),
    (80, 204, 98, 98, 122, 49, 24, 24, 24, 37, 37, 37, 86),
    (0, 0, 24, 24, 12, 24, 61, 61, 24, 73, 73, 74, 86),
    (133, 109, 37, 37, 37, 12, 12, 12, 12, 24, 24, 37, 62),
    (279, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (173, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (173, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 68, 196, 196, 196, 196, 147, 147, 86, 49, 49, 49, 37),
    (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
    (0, 14, 24, 24, 24, 24, 24, 24, 24, 24, 24, 12, 12),
)


def rating(parameters, position=None, *, boosts=None, allow_high=True):
    """Rate one 147-field snapshot without modifying it.

    A deterministic, neutral comparison uses identical position and effects
    for every allocation candidate. No guessed base_overall metadata is used.
    """
    if len(parameters) != 147:
        raise ValueError('overall requires canonical 147-field parameters')
    position = parameters[0] if position is None else position
    if type(position) is not int or not 0 <= position <= 12:
        raise ValueError('invalid overall position')
    values = [parameters[i] for i in PARAMETERS]
    if any(type(value) is not int for value in values):
        raise ValueError('invalid overall attributes')
    if boosts:
        values = [value + boosts.get(index, 0) for value, index in zip(values, PARAMETERS)]
    values[0] -= 111
    values[26] = (59 * values[26]) // 3 + 40
    score = sum(row[position] * max(15, min(95, value - 25))
                for row, value in zip(WEIGHTS, values))
    result = max(40, (score + 500) // 1000)
    return result if allow_high else min(110, result)
