import argparse
import sys
from pathlib import Path

from .anki_connect import (
    anki_version,
    create_deck,
    get_deck_names,
    get_model_field_names,
    get_model_names,
    get_models_with_fields,
    add_notes,
)
from .audio import build_sound_tags
from .ipa import build_ipa_map
from .vocab import build_note, load_vocab
from .formatting import format_back_plain


def print_models_table(models: dict[str, list[str]]) -> None:
    print(f"\n{'#':<4}  {'Note type':<40}  Fields")
    print("─" * 72)
    for i, (name, fields) in enumerate(models.items(), 1):
        print(f"{i:<4}  {name:<40}  {', '.join(fields)}")
    print()


def _pick_number(prompt: str, lo: int, hi: int) -> int:
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and lo <= int(raw) <= hi:
            return int(raw)
        print(f"  Please enter a number between {lo} and {hi}.")


def _pick_field(fields: list[str], role: str, default: str) -> str:
    print(f"\n  Fields available for '{role}':")
    for i, f in enumerate(fields, 1):
        marker = " (default)" if f == default else ""
        print(f"    [{i}] {f}{marker}")
    while True:
        raw = input(f"  Pick '{role}' field [{default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(fields):
            return fields[int(raw) - 1]
        if raw in fields:
            return raw
        print(f"  Invalid choice. Enter a number 1–{len(fields)} or the field name.")


def pick_template_interactive() -> tuple[str, str, str]:
    models = get_models_with_fields()
    model_list = list(models.items())

    print_models_table(models)
    idx = _pick_number(f"Pick a template [1-{len(model_list)}]: ", 1, len(model_list))
    model_name, fields = model_list[idx - 1]

    print(f"\n  Selected: {model_name}")
    print(f"  Fields  : {', '.join(fields)}")

    default_front = fields[0] if fields else "Front"
    default_back = fields[1] if len(fields) > 1 else fields[0]

    front_field = _pick_field(fields, "front (vocabulary word)", default_front)
    back_field = _pick_field(fields, "back (meanings + examples)", default_back)

    print(f"\n  ✓ Template : {model_name}")
    print(f"  ✓ Front    : {front_field}")
    print(f"  ✓ Back     : {back_field}\n")
    return model_name, front_field, back_field


def run_dry(vocab: list[dict], deck: str, with_ipa: bool = False) -> None:
    ipa_map = build_ipa_map(vocab) if with_ipa else {}
    print(f"DRY RUN — {len(vocab)} card(s) that would be added to deck '{deck}'\n")
    for item in vocab:
        word = item["vocabulary"]
        ipa = ipa_map.get(word, "")
        header = f"{word}  {ipa}".strip()
        print(f"┌─ FRONT: {header}")
        print(format_back_plain(item["meanings"]))
        print()


def run_add(
    vocab: list[dict],
    *,
    deck: str,
    model: str,
    front_field: str,
    back_field: str,
    tags: list[str],
    allow_duplicates: bool,
    with_audio: bool = False,
    with_ipa: bool = False,
) -> None:
    version = anki_version()
    print(f"Connected — AnkiConnect v{version}")

    available_models = get_model_names()
    if model not in available_models:
        sys.exit(
            f"\nModel '{model}' not found in Anki.\n"
            f"Available models:\n  " + "\n  ".join(available_models)
        )

    fields = get_model_field_names(model)
    for label, field in [("front", front_field), ("back", back_field)]:
        if field not in fields:
            sys.exit(
                f"\n--{label}-field '{field}' not in model '{model}'.\n"
                f"Fields available: {', '.join(fields)}"
            )

    create_deck(deck)
    print(f"Deck  : '{deck}'")
    print(f"Model : '{model}'  ({front_field} / {back_field})")
    print(f"Tags  : {tags}")
    print(f"Audio : {'yes' if with_audio else 'no'}")
    print(f"IPA   : {'yes' if with_ipa else 'no'}")
    print(f"Cards : {len(vocab)}\n")

    ipa_map: dict[str, str] = build_ipa_map(vocab) if with_ipa else {}
    sound_tags: dict[str, str] = build_sound_tags(vocab) if with_audio else {}

    notes = [
        build_note(
            item,
            deck=deck,
            model=model,
            front_field=front_field,
            back_field=back_field,
            tags=tags,
            allow_duplicates=allow_duplicates,
            sound_tag=sound_tags.get(item["vocabulary"]),
            ipa=ipa_map.get(item["vocabulary"]),
        )
        for item in vocab
    ]

    results = add_notes(notes)

    added = sum(1 for r in results if r is not None)
    skipped = len(results) - added
    print(f"Done — {added} added, {skipped} skipped (duplicates or validation errors)")

    if skipped:
        print("\nSkipped:")
        for item, note_id in zip(vocab, results):
            if note_id is None:
                print(f"  - {item['vocabulary']}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="generate_vocab_cards",
        description="Add Anki cards from a vocabulary JSON file via AnkiConnect.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    p.add_argument(
        "--list-models",
        action="store_true",
        help="Print all note types with their fields and exit.",
    )
    p.add_argument(
        "--list-decks",
        action="store_true",
        help="Print all decks in Anki and exit.",
    )
    p.add_argument(
        "--pick-template",
        action="store_true",
        help=(
            "Interactively choose a note type and map its fields. "
            "When combined with -f and -d, proceeds to add cards after picking."
        ),
    )

    p.add_argument("-f", "--file", help="Path to the vocabulary JSON file.")
    p.add_argument("-d", "--deck", help="Target deck name (created if absent).")
    p.add_argument(
        "-m",
        "--model",
        default="Basic",
        help="Note type name (default: Basic).",
    )

    p.add_argument(
        "--front-field",
        default="Front",
        metavar="FIELD",
        help="Field that receives the vocabulary word (default: Front).",
    )
    p.add_argument(
        "--back-field",
        default="Back",
        metavar="FIELD",
        help="Field that receives meanings + examples (default: Back).",
    )

    p.add_argument(
        "--audio",
        action="store_true",
        help=(
            "Generate an English pronunciation MP3 for each word and embed it "
            "in the card. Requires: pip install gtts"
        ),
    )
    p.add_argument(
        "--ipa",
        action="store_true",
        help=(
            "Fetch the IPA transcription for each word from the free Dictionary API "
            "and show it below the word on the front of the card. No extra install needed."
        ),
    )

    p.add_argument(
        "--tags",
        default="vocabulary",
        help="Comma-separated tags applied to every card (default: vocabulary).",
    )
    p.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Add the card even if it already exists in the deck.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cards without touching Anki.",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_models:
        print_models_table(get_models_with_fields())
        return
    if args.list_decks:
        print("\n".join(get_deck_names()))
        return

    model = args.model
    front_field = args.front_field
    back_field = args.back_field

    if args.pick_template:
        model, front_field, back_field = pick_template_interactive()
        if not args.file:
            return

    if not args.file:
        parser.error("--file is required (or use --list-models / --list-decks / --pick-template).")
    if not args.deck and not args.dry_run:
        parser.error("--deck is required when not using --dry-run.")

    try:
        vocab = load_vocab(Path(args.file))
    except ValueError as exc:
        sys.exit(str(exc))

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    if args.dry_run:
        run_dry(vocab, deck=args.deck or "(no deck)", with_ipa=args.ipa)
    else:
        run_add(
            vocab,
            deck=args.deck,
            model=model,
            front_field=front_field,
            back_field=back_field,
            tags=tags,
            allow_duplicates=args.allow_duplicates,
            with_audio=args.audio,
            with_ipa=args.ipa,
        )
