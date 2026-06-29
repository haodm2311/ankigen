import base64
import json
import sys
import urllib.error
import urllib.request

ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_CONNECT_VERSION = 6


def _request(action: str, **params):
    payload = json.dumps(
        {"action": action, "version": ANKI_CONNECT_VERSION, "params": params}
    ).encode()
    try:
        req = urllib.request.Request(ANKI_CONNECT_URL, payload)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError:
        sys.exit(
            "\nCannot connect to AnkiConnect at http://localhost:8765\n"
            "  1. Make sure Anki is open.\n"
            "  2. Install the AnkiConnect add-on (code: 2055492159).\n"
            "  3. Restart Anki after installing.\n"
        )
    if result.get("error"):
        raise RuntimeError(f"AnkiConnect error: {result['error']}")
    return result["result"]


def anki_version() -> int:
    return _request("version")


def get_model_names() -> list[str]:
    return sorted(_request("modelNames"))


def get_deck_names() -> list[str]:
    return sorted(_request("deckNames"))


def get_model_field_names(model: str) -> list[str]:
    return _request("modelFieldNames", modelName=model)


def get_models_with_fields() -> dict[str, list[str]]:
    names = get_model_names()
    return {name: get_model_field_names(name) for name in names}


def create_deck(deck: str) -> None:
    _request("createDeck", deck=deck)


def add_notes(notes: list[dict]) -> list[int | None]:
    return _request("addNotes", notes=notes)


def store_media_file(filename: str, data: bytes) -> None:
    _request("storeMediaFile", filename=filename, data=base64.b64encode(data).decode())
