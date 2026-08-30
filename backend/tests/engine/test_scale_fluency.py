import pytest

from app.engine.scale_fluency import generate_scale_pattern
from app.engine.theory import fret_to_midi


def test_g_major_three_nps_golden_pattern() -> None:
    """Hand-verified reference pattern: G major, 3nps, starting string 6 fret 3.

    See the Module 2 plan for the full derivation. Any change to the
    ascending-pitch-slicing algorithm that breaks this indicates a musical
    correctness regression, not just a refactor.
    """
    drill = generate_scale_pattern(key="G", scale="major", start_string=6, start_fret=3, num_strings=6)

    expected = [
        (6, 3, "G2"), (6, 5, "A2"), (6, 7, "B2"),
        (5, 3, "C3"), (5, 5, "D3"), (5, 7, "E3"),
        (4, 4, "F#3"), (4, 5, "G3"), (4, 7, "A3"),
        (3, 4, "B3"), (3, 5, "C4"), (3, 7, "D4"),
        (2, 5, "E4"), (2, 7, "F#4"), (2, 8, "G4"),
        (1, 5, "A4"), (1, 7, "B4"), (1, 8, "C5"),
    ]
    actual = [(n["position"]["string"], n["position"]["fret"], n["pitch"]) for n in drill.notes]
    assert actual == expected


def test_a_minor_pentatonic_box_one_golden_pattern() -> None:
    """Hand-verified reference pattern: A minor pentatonic, box 1, starting
    string 6 fret 5 — the textbook "5-8/5-7/5-7/5-7/5-8/5-8" shape every
    guitarist knows. Confirms 2-notes-per-string reproduces standard
    pentatonic box fingerings, not just an arbitrary subset of notes.
    """
    drill = generate_scale_pattern(key="A", scale="minor_pentatonic", start_string=6, start_fret=5, num_strings=6)

    expected = [
        (6, 5, "A2"), (6, 8, "C3"),
        (5, 5, "D3"), (5, 7, "E3"),
        (4, 5, "G3"), (4, 7, "A3"),
        (3, 5, "C4"), (3, 7, "D4"),
        (2, 5, "E4"), (2, 8, "G4"),
        (1, 5, "A4"), (1, 8, "C5"),
    ]
    actual = [(n["position"]["string"], n["position"]["fret"], n["pitch"]) for n in drill.notes]
    assert actual == expected


def test_pentatonic_uses_two_notes_per_string() -> None:
    drill = generate_scale_pattern(key="G", scale="major_pentatonic", start_string=6, start_fret=0, num_strings=5)
    assert len(drill.notes) == 10
    assert drill.parameters["notes_per_string"] == 2


def test_seven_note_scale_uses_three_notes_per_string() -> None:
    drill = generate_scale_pattern(key="C", scale="natural_minor", start_string=6, start_fret=0, num_strings=5)
    assert len(drill.notes) == 15
    assert drill.parameters["notes_per_string"] == 3


def test_note_count_matches_num_strings() -> None:
    drill = generate_scale_pattern(key="C", scale="major", start_string=6, start_fret=0, num_strings=4)
    assert len(drill.notes) == 12


def test_frets_within_bounds() -> None:
    drill = generate_scale_pattern(key="E", scale="harmonic_minor", start_string=6, start_fret=0, num_strings=6)
    for note in drill.notes:
        assert 0 <= note["position"]["fret"] <= 15


def test_pitches_strictly_ascending() -> None:
    drill = generate_scale_pattern(key="A", scale="melodic_minor", start_string=6, start_fret=2, num_strings=6)
    midis = [fret_to_midi(n["position"]["string"], n["position"]["fret"]) for n in drill.notes]
    assert midis == sorted(midis)
    assert len(midis) == len(set(midis))


def test_unsupported_key_raises() -> None:
    with pytest.raises(ValueError):
        generate_scale_pattern(key="C#", scale="major")


def test_unsupported_scale_raises() -> None:
    with pytest.raises(ValueError):
        generate_scale_pattern(key="C", scale="dorian")


def test_out_of_range_string_combination_raises() -> None:
    with pytest.raises(ValueError):
        generate_scale_pattern(key="C", scale="major", start_string=3, num_strings=6)


def test_start_fret_out_of_range_raises() -> None:
    with pytest.raises(ValueError):
        generate_scale_pattern(key="C", scale="major", start_fret=20)


def test_pattern_exceeding_max_fret_raises() -> None:
    with pytest.raises(ValueError):
        generate_scale_pattern(key="C", scale="major", start_string=1, start_fret=15, num_strings=1)
