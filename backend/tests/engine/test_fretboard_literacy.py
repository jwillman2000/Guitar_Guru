import random

import pytest

from app.engine.fretboard_literacy import generate_drill


def test_generate_drill_returns_requested_count() -> None:
    drill = generate_drill(key="G", count=5, rng=random.Random(0))
    assert len(drill.notes) == 5


def test_generate_drill_positions_within_range() -> None:
    drill = generate_drill(
        key="C",
        string_range=(2, 4),
        fret_range=(3, 7),
        count=6,
        rng=random.Random(1),
    )
    for note in drill.notes:
        position = note["position"]
        assert 2 <= position["string"] <= 4
        assert 3 <= position["fret"] <= 7


def test_generate_drill_positions_are_unique() -> None:
    drill = generate_drill(key="A", string_range=(1, 2), fret_range=(0, 4), count=10, rng=random.Random(2))
    positions = [(n["position"]["string"], n["position"]["fret"]) for n in drill.notes]
    assert len(positions) == len(set(positions))


def test_generate_drill_rejects_unsupported_key() -> None:
    with pytest.raises(ValueError):
        generate_drill(key="C#", count=1)


def test_generate_drill_rejects_count_exceeding_available_positions() -> None:
    with pytest.raises(ValueError):
        generate_drill(key="C", string_range=(1, 1), fret_range=(0, 0), count=2)


def test_generate_drill_rejects_out_of_bounds_ranges() -> None:
    with pytest.raises(ValueError):
        generate_drill(key="C", string_range=(0, 6), count=1)
    with pytest.raises(ValueError):
        generate_drill(key="C", fret_range=(0, 20), count=1)
