import json
from pathlib import Path


def load_vocab(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
    if not isinstance(data, list):
        raise ValueError("JSON must be a top-level array of vocabulary objects.")
    return data


def build_note(
    item: dict,
    *,
    deck: str,
    model: str,
    front_field: str,
    back_field: str,
    tags: list[str],
    allow_duplicates: bool,
    sound_tag: str | None = None,
    ipa: str | None = None,
) -> dict:
    from .formatting import format_back_html, format_front_html

    return {
        "deckName": deck,
        "modelName": model,
        "fields": {
            front_field: format_front_html(item["vocabulary"], ipa, sound_tag),
            back_field: format_back_html(item["meanings"]),
        },
        "options": {"allowDuplicate": allow_duplicates},
        "tags": tags,
    }
