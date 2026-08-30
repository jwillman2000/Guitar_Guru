import pytest

from app.engine.picking_technique import (
    DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES,
    generate_alternate_picking_drill,
    generate_economy_picking_drill,
    generate_hybrid_picking_drill,
    generate_string_skipping_drill,
    generate_sweep_picking_drill,
    generate_tremolo_drill,
)


def test_alternate_picking_strictly_alternates() -> None:
    drill = generate_alternate_picking_drill(key="G", scale="major", start_string=6, start_fret=3, num_strings=6)
    directions = [n["pickDirection"] for n in drill.notes]
    assert directions == ["down", "up"] * (len(directions) // 2)


def test_economy_picking_matches_current_convention() -> None:
    """Tests the CURRENT convention (DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_
    DECREASES), not an independently-verified-correct one — if that constant
    is flipped after musical-accuracy review, this test's expectations must
    be updated alongside it, not left silently passing.
    """
    assert DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES is True
    drill = generate_economy_picking_drill(key="G", scale="major", start_string=6, start_fret=3, num_strings=2)
    directions = [n["position"]["string"] for n in drill.notes], [n["pickDirection"] for n in drill.notes]
    strings, picks = directions
    # Within string 6 (first 3 notes): strict alternation starting down.
    assert picks[0:3] == ["down", "up", "down"]
    # Transition to string 5 (string number decreases) repeats the last stroke.
    assert strings[2] == 6 and strings[3] == 5
    assert picks[3] == picks[2]


def test_tremolo_repeats_single_note_alternating() -> None:
    drill = generate_tremolo_drill(key="E", scale="minor_pentatonic", string=1, fret=0, repeat_count=6)
    assert len(drill.notes) == 6
    assert all(n["pitch"] == "E4" for n in drill.notes)
    assert [n["pickDirection"] for n in drill.notes] == ["down", "up"] * 3


def test_tremolo_rejects_non_diatonic_fret() -> None:
    with pytest.raises(ValueError):
        generate_tremolo_drill(key="C", scale="major", string=1, fret=6, repeat_count=4)  # F#, not in C major


def test_string_skipping_produces_expected_string_pattern() -> None:
    drill = generate_string_skipping_drill(
        key="C", scale="major", start_string=6, start_fret=0, num_strings=3, skip=2
    )
    strings = [n["position"]["string"] for n in drill.notes]
    assert strings == [6, 4, 2]


def test_string_skipping_rejects_skip_of_one() -> None:
    with pytest.raises(ValueError):
        generate_string_skipping_drill(key="C", scale="major", skip=1)


def test_string_skipping_rejects_out_of_range_pattern() -> None:
    with pytest.raises(ValueError):
        generate_string_skipping_drill(key="C", scale="major", start_string=4, num_strings=3, skip=2)  # -> [4,2,0]


def test_sweep_picking_ascending_then_descending_reverses_direction() -> None:
    drill = generate_sweep_picking_drill(key="A", chord_type="minor_triad", start_string=5, start_fret=0, num_strings=4)
    assert len(drill.notes) == 8  # 4 ascending + 4 descending
    ascending, descending = drill.notes[:4], drill.notes[4:]
    ascending_directions = {n["pickDirection"] for n in ascending}
    descending_directions = {n["pickDirection"] for n in descending}
    assert len(ascending_directions) == 1
    assert len(descending_directions) == 1
    assert ascending_directions != descending_directions
    # Descending half retraces the same positions in reverse order.
    assert [n["position"] for n in descending] == [n["position"] for n in reversed(ascending)]


def test_sweep_picking_rejects_unsupported_chord_type() -> None:
    with pytest.raises(ValueError):
        generate_sweep_picking_drill(key="A", chord_type="dominant7")


def test_hybrid_picking_splits_pick_and_finger_by_string_half() -> None:
    drill = generate_hybrid_picking_drill(key="G", scale="major", start_string=6, start_fret=3, num_strings=6)
    methods = [n["pluckMethod"] for n in drill.notes]
    assert methods == ["pick", "pick", "pick", "finger", "finger", "finger"]


def test_generators_reject_unsupported_key() -> None:
    with pytest.raises(ValueError):
        generate_alternate_picking_drill(key="C#")
    with pytest.raises(ValueError):
        generate_sweep_picking_drill(key="C#")
