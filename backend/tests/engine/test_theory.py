import pytest

from app.engine.theory import (
    ascending_scale_tones,
    fret_to_midi,
    midi_to_pitch_name,
    scale_pitch_class_spelling,
)


@pytest.mark.parametrize(
    "string,expected_open_pitch",
    [
        (1, "E4"),
        (2, "B3"),
        (3, "G3"),
        (4, "D3"),
        (5, "A2"),
        (6, "E2"),
    ],
)
def test_open_string_pitches(string: int, expected_open_pitch: str) -> None:
    assert midi_to_pitch_name(fret_to_midi(string, 0), key="C") == expected_open_pitch


def test_twelfth_fret_is_one_octave_above_open_string() -> None:
    assert midi_to_pitch_name(fret_to_midi(6, 12), key="C") == "E3"
    assert midi_to_pitch_name(fret_to_midi(1, 12), key="C") == "E5"


@pytest.mark.parametrize(
    "key,fret_on_low_e,expected_pitch",
    [
        ("C", 2, "F#2"),  # sharp key: pitch class 6 spelled with a sharp
        ("G", 9, "C#3"),  # sharp key: pitch class 1
        ("F", 9, "Db3"),  # flat key: same pitch class, spelled with a flat
        ("F", 6, "Bb2"),  # flat key: pitch class 10
        ("Db", 8, "C3"),  # flat key, natural pitch class
    ],
)
def test_key_dependent_enharmonic_spelling(key: str, fret_on_low_e: int, expected_pitch: str) -> None:
    assert midi_to_pitch_name(fret_to_midi(6, fret_on_low_e), key=key) == expected_pitch


def test_f_sharp_major_known_simplification() -> None:
    """F# major's diatonic 7th degree is theoretically "E#" (enharmonic to F).

    This engine uses a simple per-key sharp/flat table rather than full
    diatonic letter-spelling, so it renders "F" instead. Documented as a
    known simplification (see theory.midi_to_pitch_name docstring) rather
    than silently wrong — flagged for musical-accuracy review.
    """
    assert midi_to_pitch_name(fret_to_midi(6, 1), key="F#") == "F2"


def test_unsupported_key_raises() -> None:
    with pytest.raises(ValueError):
        midi_to_pitch_name(60, key="C#")


def test_g_major_scale_spelling() -> None:
    assert scale_pitch_class_spelling("G", "major") == {
        7: "G",
        9: "A",
        11: "B",
        0: "C",
        2: "D",
        4: "E",
        6: "F#",
    }


def test_g_harmonic_minor_raised_seventh_spells_as_sharp() -> None:
    """Regression test for the bug this design specifically fixes: a coarse
    per-key sharp/flat table would misspell G harmonic minor's raised 7th as
    "Gb" (since G is a flat-side key), but the correct diatonic spelling is
    "F#" (the natural minor's F, raised). Degree-by-degree letter-cycling
    spelling gets this right regardless of the key's overall flat/sharp bias.
    """
    spelling = scale_pitch_class_spelling("G", "harmonic_minor")
    assert spelling == {7: "G", 9: "A", 10: "Bb", 0: "C", 2: "D", 3: "Eb", 6: "F#"}


def test_db_natural_minor_produces_expected_rare_spelling() -> None:
    """Db natural minor is a genuinely remote key: strict letter-cycling
    spelling correctly produces a double-flat (Bbb) and enharmonic spellings
    (Fb, Cb) a guitarist would normally call E/B. This is correct, expected
    notation for this key — not a computation error.
    """
    spelling = scale_pitch_class_spelling("Db", "natural_minor")
    assert spelling == {1: "Db", 3: "Eb", 4: "Fb", 6: "Gb", 8: "Ab", 9: "Bbb", 11: "Cb"}


def test_scale_pitch_class_spelling_rejects_unsupported_scale() -> None:
    with pytest.raises(ValueError):
        scale_pitch_class_spelling("C", "dorian")


def test_ascending_scale_tones_c_major() -> None:
    assert ascending_scale_tones("C", "major", start_midi=60, count=7) == [60, 62, 64, 65, 67, 69, 71]


def test_g_major_pentatonic_spelling_is_correct_letter_subset() -> None:
    """G major pentatonic must be G,A,B,D,E (dropping C and F#) — the correct
    letter-subset of G major's spelling, not a renumbered 5-letter cycle.
    """
    assert scale_pitch_class_spelling("G", "major_pentatonic") == {7: "G", 9: "A", 11: "B", 2: "D", 4: "E"}


def test_e_minor_pentatonic_spelling_is_correct_letter_subset() -> None:
    """E minor pentatonic must be E,G,A,B,D — the correct letter-subset of E
    natural minor's spelling (dropping the 2nd and 6th degrees).
    """
    assert scale_pitch_class_spelling("E", "minor_pentatonic") == {4: "E", 7: "G", 9: "A", 11: "B", 2: "D"}

