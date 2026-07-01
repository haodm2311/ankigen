import io
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Semaphore

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


def _generate_via_gtts(word: str) -> tuple[str, bytes]:
    gTTS = _require_gtts()
    buf = io.BytesIO()
    gTTS(text=word, lang="en", slow=False).write_to_fp(buf)
    return _safe_filename(word), buf.getvalue()


CACHE_DIR = Path(".audio_cache")


def generate_audio(word: str) -> tuple[str, bytes]:
    """Return (filename, mp3_bytes). Use local cache when available."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    filename = _safe_filename(word)
    cache_path = CACHE_DIR / filename
    if cache_path.exists():
        try:
            return filename, cache_path.read_bytes()
        except Exception:
            # fallthrough to regenerate if reading cache fails
            pass

    filename, mp3 = _generate_via_gtts(word)
    try:
        cache_path.write_bytes(mp3)
    except Exception as exc:
        print(f"  ! Could not write cache for {word}: {exc}")
    return filename, mp3


def build_sound_tags(vocab: list[dict], max_workers: int = 2, request_delay: float = 0.15) -> dict[str, str]:
    # Rate limiting / retry settings
    MAX_TTS_RETRIES = 5
    BACKOFF_INITIAL = 1.0
    SLEEP_BETWEEN = request_delay
    
    # Throttle to limit concurrent TTS requests
    semaphore = Semaphore(max_workers)
    
    def process_word(item: dict) -> tuple[str, str | None]:
        """Generate audio for one word. Returns (word, sound_tag or None)."""
        word = item["vocabulary"]
        filename = None
        mp3 = None
        
        for attempt in range(1, MAX_TTS_RETRIES + 1):
            try:
                with semaphore:
                    filename, mp3 = generate_audio(word)
                break
            except Exception as exc:
                exc_str = str(exc)
                is_429 = "429" in exc_str
                
                if attempt == MAX_TTS_RETRIES:
                    print(f"  ✗ {word}  ({exc})")
                else:
                    # For 429s, use longer backoff
                    base_wait = BACKOFF_INITIAL * (2 ** (attempt - 1))
                    wait = base_wait * 3 if is_429 else base_wait
                    msg = f"  ! {word} attempt {attempt} failed: {exc} — retrying in {wait:.1f}s"
                    if is_429:
                        msg += " (rate limit detected, using extended backoff)"
                    print(msg)
                    time.sleep(wait)
        
        if mp3 is not None:
            try:
                store_media_file(filename, mp3)
                print(f"  ✓ {word}")
                return word, f"[sound:{filename}]"
            except Exception as exc:
                print(f"  ✗ {word}  (upload failed: {exc})")
        
        return word, None
    
    print(f"Generating audio for {len(vocab)} word(s)… (max_workers={max_workers}, delay={SLEEP_BETWEEN}s)")
    tags: dict[str, str] = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_word, item): item for item in vocab}
        for future in as_completed(futures):
            try:
                word, sound_tag = future.result()
                if sound_tag:
                    tags[word] = sound_tag
            except Exception as exc:
                print(f"  ✗ Worker error: {exc}")
            
            # polite pause between completions
            time.sleep(SLEEP_BETWEEN)
    
    ok = len(tags)
    fail = len(vocab) - ok
    print(f"Audio done — {ok} generated, {fail} failed\n")
    return tags
