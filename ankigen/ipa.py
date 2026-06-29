def build_ipa_map(vocab: list[dict]) -> dict[str, str]:
    print(f"Reading IPA for {len(vocab)} word(s)…")
    ipa_map: dict[str, str] = {}
    for item in vocab:
        word = item["vocabulary"]
        ipa = item.get("ipa")
        if ipa:
            ipa_map[word] = ipa
            print(f"  ✓ {word:<25} {ipa}")
        else:
            print(f"  ✗ {word:<25} (no IPA provided)")
    ok, fail = len(ipa_map), len(vocab) - len(ipa_map)
    print(f"IPA done — {ok} found, {fail} missing\n")
    return ipa_map
