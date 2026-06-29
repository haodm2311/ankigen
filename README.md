# ankigen

Generate Anki cards from a JSON vocabulary file using AnkiConnect.

## Requirements

- Python 3.13+
- Anki installed and running
- AnkiConnect add-on installed (2055492159)
- Internet access for IPA and audio generation

## Setup

```bash
cd /path/to/ankigen
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

### Run via Python

```bash
python main.py -f vocab.json -d "English Vocab" -m "Basic"
```

### Run via installed script

```bash
generate_vocab_cards -f vocab.json -d "English Vocab" -m "Basic"
```

### Common options

- `-f, --file` : path to vocabulary JSON
- `-d, --deck` : target deck name
- `-m, --model` : Anki note type (default: `Basic`)
- `--audio` : generate pronunciation audio
- `--ipa` : use IPA from the JSON input (`ipa` field)
- `--dry-run` : preview cards without adding them
- `--list-models` : show available note types
- `--list-decks` : show existing Anki decks
- `--pick-template` : interactively choose fields for a note type

## Vocabulary JSON format

```json
[
  {
    "vocabulary": "Stigma",
    "ipa": "ˈstɪɡmə",
    "meanings": [
      {
        "meaning": "sự kỳ thị",
        "example": { "en": "...", "vi": "..." }
      }
    ]
  }
]
```

## Notes

- Anki must be open when running the tool.
- `--audio` requires `gtts`, which is included in the package dependencies.
