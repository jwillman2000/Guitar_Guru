"""Pure music-theory primitives: fret/string <-> MIDI <-> spelled pitch name.

No DB or FastAPI dependency here — this module is deterministic math only,
per CONSTITUTION.md Article I (fret/note content is never freehanded).
"""

# String numbering matches the frontend's FretPosition convention: 1 = high E,
# 6 = low E. Values are the MIDI note number of each string's open pitch.
OPEN_STRING_MIDI: dict[int, int] = {
    1: 64,  # E4
    2: 59,  # B3
    3: 55,  # G3
    4: 50,  # D3
    5: 45,  # A2
    6: 40,  # E2
}

PITCH_CLASSES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCH_CLASSES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# One key per pitch class (12 total) — the guitar-idiomatic choice between
# enharmonic equivalents (e.g. F# over Gb).
SHARP_KEYS = {"C", "G", "D", "A", "E", "B", "F#"}
FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db"}
SUPPORTED_KEYS = SHARP_KEYS | FLAT_KEYS


def fret_to_midi(string: int, fret: int) -> int:
    return OPEN_STRING_MIDI[string] + fret


def midi_to_pitch_name(midi: int, key: str) -> str:
    """Spell a MIDI note per the given key's sharp/flat convention.

    Known simplification: keys with 6 sharps (F#) diatonically require a
    double-letter spelling (E#) for one scale degree. This table renders it
    as the enharmonic "F" instead — flagged for musical-accuracy review
    rather than silently handled, since it deviates from strict theory.
    """
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}")
    pitch_class = midi % 12
    octave = midi // 12 - 1
    table = PITCH_CLASSES_SHARP if key in SHARP_KEYS else PITCH_CLASSES_FLAT
    return f"{table[pitch_class]}{octave}"
