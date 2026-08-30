from app.models import Tag, TagCategory
from app.tagging import split_tags


def _tag(category: TagCategory, name: str) -> Tag:
    return Tag(category=category, name=name, slug=name.lower().replace(" ", "-"))


def test_split_tags_separates_genre_and_technique() -> None:
    tags = [
        _tag(TagCategory.GENRE, "Metal"),
        _tag(TagCategory.TECHNIQUE, "Sweep Picking"),
        _tag(TagCategory.GENRE, "Jazz"),
    ]
    genre_tags, technique_tags = split_tags(tags)
    assert genre_tags == ["Metal", "Jazz"]
    assert technique_tags == ["Sweep Picking"]


def test_split_tags_excludes_position_category() -> None:
    tags = [_tag(TagCategory.POSITION, "Position 1 (C Shape)"), _tag(TagCategory.GENRE, "Country")]
    genre_tags, technique_tags = split_tags(tags)
    assert genre_tags == ["Country"]
    assert technique_tags == []


def test_split_tags_empty() -> None:
    assert split_tags([]) == ([], [])
