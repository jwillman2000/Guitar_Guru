"""Seed the starting tag taxonomy (genre/technique/position).

Idempotent: safe to run repeatedly against any environment. Tags are labels,
not musical content, so they're fine to seed directly per the content rules
in CLAUDE.md — actual lick/exercise reference data still requires
hand-curation or the rules engine.

Usage: python -m app.db.seed_tags
"""

from sqlalchemy.dialects.postgresql import insert

from app.db.session import SessionLocal
from app.models.tag import Tag, TagCategory

GENRES = ["Metal", "Jazz", "Country"]

TECHNIQUES = [
    "Alternate Picking",
    "Economy Picking",
    "Sweep Picking",
    "String Skipping",
    "Hybrid Picking",
    "Tremolo Picking",
]

# Standard CAGED positions; extend via the same tags table as needed.
POSITIONS = [
    "Position 1 (C Shape)",
    "Position 2 (A Shape)",
    "Position 3 (G Shape)",
    "Position 4 (E Shape)",
    "Position 5 (D Shape)",
]


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("(", "").replace(")", "")


def seed() -> None:
    rows = [
        {"category": category, "name": name, "slug": slugify(name)}
        for category, names in (
            (TagCategory.GENRE, GENRES),
            (TagCategory.TECHNIQUE, TECHNIQUES),
            (TagCategory.POSITION, POSITIONS),
        )
        for name in names
    ]

    with SessionLocal() as db:
        stmt = insert(Tag).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=["category", "slug"])
        result = db.execute(stmt)
        db.commit()
        print(f"Inserted {result.rowcount} new tag(s); {len(rows)} total defined.")


if __name__ == "__main__":
    seed()
