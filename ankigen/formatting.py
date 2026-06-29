def format_back_html(meanings: list[dict]) -> str:
    rows = []
    for i, m in enumerate(meanings, 1):
        meaning = m["meaning"]
        en = m["example"]["en"]
        vi = m["example"]["vi"]
        rows.append(
            f'<div style="margin-bottom:10px">'
            f'<b>{i}. {meaning}</b><br>'
            f'<span style="color:#555">&nbsp;&nbsp;{en}</span><br>'
            f'<span style="color:#888">&nbsp;&nbsp;{vi}</span>'
            f'</div>'
        )
    return "\n".join(rows)


def format_back_plain(meanings: list[dict]) -> str:
    rows = []
    for i, m in enumerate(meanings, 1):
        rows.append(
            f"  {i}. {m['meaning']}\n"
            f"     EN: {m['example']['en']}\n"
            f"     VI: {m['example']['vi']}"
        )
    return "\n".join(rows)


def format_front_html(word: str, ipa: str | None, sound_tag: str | None) -> str:
    html = word
    if ipa:
        html += f'<br><span style="color:#888;font-size:0.85em;font-style:italic">{ipa}</span>'
    if sound_tag:
        html += f"<br>{sound_tag}"
    return html
