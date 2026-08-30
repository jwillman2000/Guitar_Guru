# Deterministic rules engine: scale formulas, interval math, genre presets.
# Generates the actual notes/frets for Modules 1, 2, 4 (never freehanded by an
# LLM — see CONSTITUTION.md Article I). Called through this package's public
# API only, so future callers (AI param assist, audio analysis) don't need
# internal knowledge of how drills are generated — see Article V.

from app.engine.fretboard_literacy import generate_drill as generate_fretboard_literacy_drill
from app.engine.picking_technique import (
    generate_alternate_picking_drill,
    generate_economy_picking_drill,
    generate_hybrid_picking_drill,
    generate_string_skipping_drill,
    generate_sweep_picking_drill,
    generate_tremolo_drill,
)
from app.engine.scale_fluency import generate_scale_pattern as generate_scale_fluency_drill

__all__ = [
    "generate_fretboard_literacy_drill",
    "generate_scale_fluency_drill",
    "generate_alternate_picking_drill",
    "generate_economy_picking_drill",
    "generate_tremolo_drill",
    "generate_string_skipping_drill",
    "generate_sweep_picking_drill",
    "generate_hybrid_picking_drill",
]
