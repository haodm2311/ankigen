import io

from .anki_connect import store_media_file


def _require_gtts():
    try:
        from gtts import gTTS
        return gTTS
    except ImportError:
        raise ImportError(
            "--audio requires the gtts package. Install it with: pip install gtts"
        )


def _safe_filename(word: str) -> str:
    safe = "".join(c if c.isalnum() else "_" for c in word.lower()).strip("_")
    return f"vocab_{safe}.mp3"


def generate_audio(word: str) -> tuple[str, bytes]:
    gTTS = _require_gtts()
    buf = io.BytesIO()
    gTTS(text=word, lang="en", slow=False).write_to_fp(buf)
    return _safe_filename(word), buf.getvalue()


def build_sound_tags(vocab: list[dict]) -> dict[str, str]:
    print(f"Generating audio for {len(vocab)} word(s)…")
    tags: dict[str, str] = {}
    for item in vocab:
        word = item["vocabulary"]
        try:
            filename, mp3 = generate_audio(word)
            store_media_file(filename, mp3)
            tags[word] = f"[sound:{filename}]"
            print(f"  ✓ {word}")
        except Exception as exc:
            print(f"  ✗ {word}  ({exc})")
    ok = len(tags)
    fail = len(vocab) - ok
    print(f"Audio done — {ok} generated, {fail} failed\n")
    return tags
