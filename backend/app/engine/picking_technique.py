"""Module 4 (Picking Technique) drill generators.

Builds on app.engine.theory's scale/arpeggio/pitch math (and Module 2's scale
pattern generator, for alternate/economy picking). Each generator produces a
note sequence and annotates it with pick-stroke direction or plucking method.

IMPORTANT — musical accuracy caveat: economy picking and sweep picking depend
on a physical pick-motion convention (which stroke direction "continues"
across a string change) that isn't asserted with full confidence here. Both
rules derive from the single constant below so a correction is a one-line
fix, not a scattered hunt. See the Module 4 plan for the full explanation —
this is the top review-priority item for musical accuracy sign-off.
"""

from app.engine.scale_fluency import generate_scale_pattern
from app.engine.theory import (
    ARPEGGIO_INTERVALS,
    MAX_FRET,
    MAX_STRING,
    MIN_STRING,
    SCALE_INTERVALS,
    SUPPORTED_KEYS,
    Drill,
    arpeggio_pitch_class_spelling,
    fret_to_midi,
    nearest_diatonic_tones_per_string,
    scale_pitch_class_spelling,
)

# The physical fact both rules below depend on: a downstroke naturally
# continues (without reversing) into the next string when a run's string
# number *decreases* — which is this engine's standard traversal direction
# (start_string down to the lowest string in range, ascending in pitch,
# matching Module 2's 3nps convention). The opposite transition (string
# number increasing) naturally continues an upstroke instead. This single
# fact drives both economy picking's "when do strokes repeat instead of
# alternate at a string change" exception and sweep picking's base stroke
# direction, so correcting it (if review shows it's backwards) is a one-line
# fix in one place, not a scattered hunt.
DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES = True


def _validate_string_range(start_string: int, num_strings: int) -> int:
    lowest_string = start_string - num_strings + 1
    if not (MIN_STRING <= lowest_string <= start_string <= MAX_STRING):
        raise ValueError(
            f"start_string={start_string} with num_strings={num_strings} falls outside "
            f"{MIN_STRING}-{MAX_STRING}"
        )
    return lowest_string


def _validate_key_scale(key: str, scale: str) -> None:
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}. Supported keys: {sorted(SUPPORTED_KEYS)}")
    if scale not in SCALE_INTERVALS:
        raise ValueError(f"Unsupported scale: {scale!r}. Supported scales: {sorted(SCALE_INTERVALS)}")


def _generate_single_position_run(
    key: str, scale: str, start_string: int, start_fret: int, num_strings: int
) -> list[dict]:
    """One note per string, in a compact single-position run — the shared
    note source for hybrid picking (and string-skipping, with a custom
    string order). Unlike the dense 3nps-style runs alternate/economy
    picking use, this stays sparse, matching how these techniques are
    actually played.
    """
    _validate_key_scale(key, scale)
    lowest_string = _validate_string_range(start_string, num_strings)
    if not (0 <= start_fret <= MAX_FRET):
        raise ValueError(f"start_fret must be within 0-{MAX_FRET}, got {start_fret}")

    spelling = scale_pitch_class_spelling(key, scale)
    strings = list(range(start_string, lowest_string - 1, -1))
    return nearest_diatonic_tones_per_string(strings, start_fret, set(spelling), spelling)


def _annotate_alternate(notes: list[dict]) -> list[dict]:
    directions = ["down", "up"]
    return [{**note, "pickDirection": directions[i % 2]} for i, note in enumerate(notes)]


def _annotate_economy(notes: list[dict]) -> list[dict]:
    """Alternate by default; repeat the stroke across a string change whose
    direction matches DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES. See
    the module docstring's accuracy caveat.
    """
    if not notes:
        return []
    annotated = [{**notes[0], "pickDirection": "down"}]
    for note in notes[1:]:
        prev = annotated[-1]
        prev_string = prev["position"]["string"]
        cur_string = note["position"]["string"]
        if cur_string == prev_string:
            direction = "up" if prev["pickDirection"] == "down" else "down"
        else:
            decreasing = cur_string < prev_string
            continues = decreasing == DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES
            if continues:
                direction = prev["pickDirection"]  # repeat
            else:
                direction = "up" if prev["pickDirection"] == "down" else "down"
        annotated.append({**note, "pickDirection": direction})
    return annotated


def generate_alternate_picking_drill(
    key: str = "C",
    scale: str = "major",
    start_string: int = 6,
    start_fret: int = 0,
    num_strings: int = 6,
) -> Drill:
    base = generate_scale_pattern(key, scale, start_string, start_fret, num_strings)
    notes = _annotate_alternate(base.notes)
    return Drill(
        title=f"Picking Technique — Alternate Picking, {key} {scale.replace('_', ' ').title()}",
        parameters={"technique": "alternate", **base.parameters},
        notes=notes,
    )


def generate_economy_picking_drill(
    key: str = "C",
    scale: str = "major",
    start_string: int = 6,
    start_fret: int = 0,
    num_strings: int = 6,
) -> Drill:
    base = generate_scale_pattern(key, scale, start_string, start_fret, num_strings)
    notes = _annotate_economy(base.notes)
    return Drill(
        title=f"Picking Technique — Economy Picking, {key} {scale.replace('_', ' ').title()}",
        parameters={"technique": "economy", **base.parameters},
        notes=notes,
    )


def generate_tremolo_drill(
    key: str = "C",
    scale: str = "major",
    string: int = 1,
    fret: int = 0,
    repeat_count: int = 8,
) -> Drill:
    _validate_key_scale(key, scale)
    if not (MIN_STRING <= string <= MAX_STRING):
        raise ValueError(f"string must be within {MIN_STRING}-{MAX_STRING}, got {string}")
    if not (0 <= fret <= MAX_FRET):
        raise ValueError(f"fret must be within 0-{MAX_FRET}, got {fret}")

    midi = fret_to_midi(string, fret)
    spelling = scale_pitch_class_spelling(key, scale)
    pitch_class = midi % 12
    if pitch_class not in spelling:
        raise ValueError(f"Fret {fret} on string {string} isn't a diatonic tone of {key} {scale}")
    octave = midi // 12 - 1
    note = {"position": {"string": string, "fret": fret}, "pitch": f"{spelling[pitch_class]}{octave}"}
    notes = _annotate_alternate([note] * repeat_count)

    return Drill(
        title=f"Picking Technique — Tremolo Picking, {note['pitch']}",
        parameters={"technique": "tremolo", "key": key, "scale": scale, "string": string, "fret": fret,
                    "repeat_count": repeat_count},
        notes=notes,
    )


def generate_string_skipping_drill(
    key: str = "C",
    scale: str = "major",
    start_string: int = 6,
    start_fret: int = 0,
    num_strings: int = 3,
    skip: int = 2,
) -> Drill:
    _validate_key_scale(key, scale)
    if skip < 2:
        raise ValueError(f"skip must be >= 2 (a skip of 1 would just be adjacent strings), got {skip}")
    if not (0 <= start_fret <= MAX_FRET):
        raise ValueError(f"start_fret must be within 0-{MAX_FRET}, got {start_fret}")

    strings = [start_string - i * skip for i in range(num_strings)]
    if any(not (MIN_STRING <= s <= MAX_STRING) for s in strings):
        raise ValueError(f"String pattern {strings} falls outside {MIN_STRING}-{MAX_STRING}")

    spelling = scale_pitch_class_spelling(key, scale)
    notes = _annotate_alternate(nearest_diatonic_tones_per_string(strings, start_fret, set(spelling), spelling))

    scale_label = scale.replace("_", " ").title()
    return Drill(
        title=f"Picking Technique — String Skipping, {key} {scale_label}",
        parameters={"technique": "string_skipping", "key": key, "scale": scale, "start_string": start_string,
                    "start_fret": start_fret, "num_strings": num_strings, "skip": skip},
        notes=notes,
    )


def generate_sweep_picking_drill(
    key: str = "C",
    chord_type: str = "major_triad",
    start_string: int = 6,
    start_fret: int = 0,
    num_strings: int = 5,
) -> Drill:
    if key not in SUPPORTED_KEYS:
        raise ValueError(f"Unsupported key: {key!r}. Supported keys: {sorted(SUPPORTED_KEYS)}")
    if chord_type not in ARPEGGIO_INTERVALS:
        raise ValueError(f"Unsupported chord_type: {chord_type!r}. Supported: {sorted(ARPEGGIO_INTERVALS)}")
    lowest_string = _validate_string_range(start_string, num_strings)
    if not (0 <= start_fret <= MAX_FRET):
        raise ValueError(f"start_fret must be within 0-{MAX_FRET}, got {start_fret}")

    spelling = arpeggio_pitch_class_spelling(key, chord_type)
    strings = list(range(start_string, lowest_string - 1, -1))  # string number decreases as we ascend
    ascending_notes = nearest_diatonic_tones_per_string(strings, start_fret, set(spelling), spelling)

    ascending_direction = "down" if DOWNSTROKE_CONTINUES_WHEN_STRING_NUMBER_DECREASES else "up"
    descending_direction = "up" if ascending_direction == "down" else "down"
    notes = [{**n, "pickDirection": ascending_direction} for n in ascending_notes]
    notes += [{**n, "pickDirection": descending_direction} for n in reversed(ascending_notes)]

    chord_label = chord_type.replace("_", " ").title()
    return Drill(
        title=f"Picking Technique — Sweep Picking, {key} {chord_label}",
        parameters={"technique": "sweep", "key": key, "chord_type": chord_type, "start_string": start_string,
                    "start_fret": start_fret, "num_strings": num_strings},
        notes=notes,
    )


def generate_hybrid_picking_drill(
    key: str = "C",
    scale: str = "major",
    start_string: int = 6,
    start_fret: int = 0,
    num_strings: int = 6,
) -> Drill:
    """Bass/lower strings get pick, treble/higher strings get fingers — a
    simplified convention (real chicken-pickin' voicings are more
    piece-specific); see the plan's confidence notes.
    """
    notes = _generate_single_position_run(key, scale, start_string, start_fret, num_strings)
    midpoint = len(notes) / 2
    annotated = [
        {**note, "pluckMethod": "pick" if i < midpoint else "finger"} for i, note in enumerate(notes)
    ]
    scale_label = scale.replace("_", " ").title()
    return Drill(
        title=f"Picking Technique — Hybrid Picking, {key} {scale_label}",
        parameters={"technique": "hybrid", "key": key, "scale": scale, "start_string": start_string,
                    "start_fret": start_fret, "num_strings": num_strings},
        notes=annotated,
    )
