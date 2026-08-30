"""Pure music-theory primitives: fret/string <-> MIDI <-> spelled pitch name.

No DB or FastAPI dependency here — this module is deterministic math only,
per CONSTITUTION.md Article I (fret/note content is never freehanded).
"""

from dataclasses import dataclass, field

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

MAX_FRET = 15  # matches the frontend Fretboard.tsx FRET_COUNT constant
MIN_STRING, MAX_STRING = 1, 6

PITCH_CLASSES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCH_CLASSES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# One key per pitch class (12 total) — the guitar-idiomatic choice between
# enharmonic equivalents (e.g. F# over Gb).
SHARP_KEYS = {"C", "G", "D", "A", "E", "B", "F#"}
FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db"}
SUPPORTED_KEYS = SHARP_KEYS | FLAT_KEYS

# Each supported key's root expressed as (natural letter, accidental), used by
# scale_pitch_class_spelling below for degree-by-degree diatonic spelling.
KEY_LETTER_ACCIDENTAL: dict[str, tuple[str, int]] = {
    "C": ("C", 0),
    "G": ("G", 0),
    "D": ("D", 0),
    "A": ("A", 0),
    "E": ("E", 0),
    "B": ("B", 0),
    "F#": ("F", 1),
    "F": ("F", 0),
    "Bb": ("B", -1),
    "Eb": ("E", -1),
    "Ab": ("A", -1),
    "Db": ("D", -1),
}

LETTERS_CYCLE = ["C", "D", "E", "F", "G", "A", "B"]
LETTER_NATURAL_PITCH_CLASS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# Scale formulas as (letter-offset-from-root, semitone-offset-from-root) pairs.
# The letter offset is the position in the 7-note diatonic cycle a degree
# occupies — for the four 7-note scales this is just its own index (0..6),
# but pentatonic scales are *subsets* of their parent scale (minor pentatonic
# = natural minor with the 2nd and 6th degrees dropped; major pentatonic =
# major with the 4th and 7th dropped), so their remaining degrees must keep
# the parent's letter positions rather than being renumbered 0..4 — that's
# what makes e.g. minor pentatonic spell as the correct subset of natural
# minor's letters instead of an unrelated 5-letter cycle.
SCALE_DEGREES: dict[str, list[tuple[int, int]]] = {
    "major": [(0, 0), (1, 2), (2, 4), (3, 5), (4, 7), (5, 9), (6, 11)],
    "natural_minor": [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 10)],
    "harmonic_minor": [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 11)],
    "melodic_minor": [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 9), (6, 11)],
    "major_pentatonic": [(0, 0), (1, 2), (2, 4), (4, 7), (5, 9)],
    "minor_pentatonic": [(0, 0), (2, 3), (3, 5), (4, 7), (6, 10)],
}

# Flat semitone-only view, derived from SCALE_DEGREES, for scale-membership
# checks (ascending_scale_tones) that don't need the letter-offset part.
SCALE_INTERVALS: dict[str, list[int]] = {
    name: [interval for _, interval in degrees] for name, degrees in SCALE_DEGREES.items()
}

# Triad formulas, same (letter-offset, semitone-offset) shape as SCALE_DEGREES
# — a triad's degrees (root, 3rd, 5th) sit at letter-offsets 0/2/4 in the same
# 7-note diatonic cycle scales use, so the identical spelling algorithm below
# applies unchanged. Used by Module 4's sweep-picking arpeggios.
ARPEGGIO_DEGREES: dict[str, list[tuple[int, int]]] = {
    "major_triad": [(0, 0), (2, 4), (4, 7)],
    "minor_triad": [(0, 0), (2, 3), (4, 7)],
    "diminished_triad": [(0, 0), (2, 3), (4, 6)],
}

ARPEGGIO_INTERVALS: dict[str, list[int]] = {
    name: [interval for _, interval in degrees] for name, degrees in ARPEGGIO_DEGREES.items()
}

_ACCIDENTAL_SYMBOLS = {0: "", 1: "#", 2: "##", -1: "b", -2: "bb"}


@dataclass
class Drill:
    """A generated drill's musical content, independent of DB/API concerns."""

    title: str
    parameters: dict
    notes: list[dict] = field(default_factory=list)  # [{"position": {"string", "fret"}, "pitch"}]


def fret_to_midi(string: int, fret: int) -> int:
    return OPEN_STRING_MIDI[string] + fret


def _pitch_class_spelling(key: str, degrees: list[tuple[int, int]]) -> dict[int, str]:
    """Shared spelling core for both scales and arpeggios (same algorithm,
    just a different degree/interval table) — see scale_pitch_class_spelling
    for the full rationale.
    """
    letter, accidental = KEY_LETTER_ACCIDENTAL[key]
    root_pc = (LETTER_NATURAL_PITCH_CLASS[letter] + accidental) % 12
    start_index = LETTERS_CYCLE.index(letter)

    spelling: dict[int, str] = {}
    for letter_offset, interval in degrees:
        degree_letter = LETTERS_CYCLE[(start_index + letter_offset) % 7]
        target_pc = (root_pc + interval) % 12
        diff = target_pc - LETTER_NATURAL_PITCH_CLASS[degree_letter]
        diff = (diff + 6) % 12 - 6  # normalize to [-6, 5]
        if diff not in _ACCIDENTAL_SYMBOLS:
            raise ValueError(f"Degree {degree_letter} needs an unsupported accidental ({diff})")
        spelling[target_pc] = f"{degree_letter}{_ACCIDENTAL_SYMBOLS[diff]}"
    return spelling


def scale_pitch_class_spelling(key: str, scale: str) -> dict[int, str]:
    """Spell each of a scale's degrees on its own diatonic letter name.

    This is the rigorous, letter-cycling method (not a coarse per-key
    sharp/flat table): each degree gets the letter its position in the
    7-note diatonic cycle implies (see SCALE_DEGREES), with whatever
    accidental is needed to hit the correct pitch class. This is what
    correctly spells a minor key's real signature (distinct from the
    same-named major key's), a harmonic/melodic minor's raised leading tone
    even in flat keys, and a pentatonic scale as the correct letter-subset of
    its parent scale rather than an unrelated 5-letter cycle. Returns
    {pitch_class: "F#", ...} for the scale's degrees; other pitch classes
    (non-scale tones) are absent since this engine's scale drills never
    generate chromatic passing tones.
    """
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}")
    if scale not in SCALE_DEGREES:
        raise ValueError(f"Unsupported scale: {scale!r}. Supported scales: {sorted(SCALE_DEGREES)}")
    return _pitch_class_spelling(key, SCALE_DEGREES[scale])


def arpeggio_pitch_class_spelling(key: str, chord_type: str) -> dict[int, str]:
    """Same spelling algorithm as scale_pitch_class_spelling, for triads."""
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}")
    if chord_type not in ARPEGGIO_DEGREES:
        raise ValueError(f"Unsupported chord_type: {chord_type!r}. Supported: {sorted(ARPEGGIO_DEGREES)}")
    return _pitch_class_spelling(key, ARPEGGIO_DEGREES[chord_type])


def _ascending_tones(key: str, intervals: list[int], start_midi: int, count: int) -> list[int]:
    """Shared core for ascending_scale_tones/ascending_arpeggio_tones."""
    letter, accidental = KEY_LETTER_ACCIDENTAL[key]
    root_pc = (LETTER_NATURAL_PITCH_CLASS[letter] + accidental) % 12
    pitch_classes = {(root_pc + interval) % 12 for interval in intervals}

    tones = []
    midi = start_midi
    while len(tones) < count:
        if midi % 12 in pitch_classes:
            tones.append(midi)
        midi += 1
    return tones


def ascending_scale_tones(key: str, scale: str, start_midi: int, count: int) -> list[int]:
    """The `count` lowest MIDI notes >= start_midi whose pitch class is in the scale."""
    if scale not in SCALE_INTERVALS:
        raise ValueError(f"Unsupported scale: {scale!r}. Supported scales: {sorted(SCALE_INTERVALS)}")
    return _ascending_tones(key, SCALE_INTERVALS[scale], start_midi, count)


def ascending_arpeggio_tones(key: str, chord_type: str, start_midi: int, count: int) -> list[int]:
    """The `count` lowest MIDI notes >= start_midi whose pitch class is in the arpeggio."""
    if chord_type not in ARPEGGIO_INTERVALS:
        raise ValueError(f"Unsupported chord_type: {chord_type!r}. Supported: {sorted(ARPEGGIO_INTERVALS)}")
    return _ascending_tones(key, ARPEGGIO_INTERVALS[chord_type], start_midi, count)


def nearest_diatonic_tones_per_string(
    strings: list[int], start_fret: int, pitch_classes: set[int], spelling: dict[int, str]
) -> list[dict]:
    """For each string in order, the lowest fret >= start_fret whose pitch
    class is in `pitch_classes` — a compact, single-position cross-string
    note selection.

    Unlike assign_tones_to_strings (one continuous ascending MIDI run sliced
    across strings, which only works when several notes share a string —
    3nps/2nps have room to climb within a string before the next string's
    open pitch catches up), this computes each string independently, so it's
    correct for one-note-per-string patterns (Module 4's alternate/economy/
    string-skipping/hybrid/sweep picking) where there's no such room.
    """
    notes = []
    for string in strings:
        fret = start_fret
        while fret_to_midi(string, fret) % 12 not in pitch_classes:
            fret += 1
            if fret > MAX_FRET:
                raise ValueError(f"No matching tone found on string {string} within fret range from {start_fret}")
        midi = fret_to_midi(string, fret)
        octave = midi // 12 - 1
        notes.append({"position": {"string": string, "fret": fret}, "pitch": f"{spelling[midi % 12]}{octave}"})
    return notes


def assign_tones_to_strings(
    tones: list[int], strings: list[int], notes_per_string: int, spelling: dict[int, str]
) -> list[dict]:
    """Slice an ascending tone list across a given string order, computing
    each note's fret and spelled pitch. `strings` need not be consecutive or
    descending — Module 4's string-skipping/sweep-picking drills pass custom
    orders through this same shared logic that Module 2's scale patterns use.
    """
    notes = []
    for index, string in enumerate(strings):
        for tone_midi in tones[index * notes_per_string : (index + 1) * notes_per_string]:
            fret = tone_midi - OPEN_STRING_MIDI[string]
            if not (0 <= fret <= MAX_FRET):
                raise ValueError(
                    f"Pattern exceeds playable fret range on string {string} (fret {fret}); "
                    "try different starting parameters."
                )
            octave = tone_midi // 12 - 1
            notes.append(
                {
                    "position": {"string": string, "fret": fret},
                    "pitch": f"{spelling[tone_midi % 12]}{octave}",
                }
            )
    return notes


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
