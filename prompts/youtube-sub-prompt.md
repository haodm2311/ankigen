You will be given a script from a CBC news video. Extract useful vocabulary
for an English learner at the B2–C1 (upper-intermediate to advanced) level.
Include single words, phrasal verbs, and common idioms/collocations.

Then, for each item, provide the most common Vietnamese meanings and return
the result strictly as a valid JSON array saved to a file named
"vocabulary.json".

## Selection rules
- Extract 20–40 items (adjust to script length; never fewer than 15).
- Skip trivial words (a, the, is, and, common nouns any beginner knows).
- Reduce each word to its dictionary/base form (e.g. "running" → "run"),
  and merge duplicates so each item appears only once.
- Keep phrasal verbs and idioms as full expressions (e.g. "crack down on").

## Meaning rules
- List the sense used in the script FIRST, then up to 2 more of the most
  common meanings (3 total by default).
- If a word has more than 3 common meanings, you may include more.
- If it has fewer than 3, include only the available ones.
- Prefix every Vietnamese meaning with its part-of-speech tag in parentheses,
  matching the sense of that specific meaning: (v) verb, (n) noun, (adj) adjective,
  (adv) adverb, (prep) preposition, (conj) conjunction, (phr v) phrasal verb,
  (idiom) idiom. If different meanings of the same word are different parts of
  speech, tag each one accordingly.
- Each example sentence must use the word in the exact sense of that meaning.
- Examples should be natural and easy to understand.

## Format rules
- Attach US IPA in slashes with stress marks, e.g. /ˈtʃɑːrdʒ/.
- Include the part of speech for each item.
- Output ONLY the JSON array — no explanations, no markdown fences.

## Output structure
[
  {
    "vocabulary": "word",
    "pos": "noun | verb | adjective | phrasal verb | idiom | ...",
    "ipa": "US IPA transcription in slashes",
    "meanings": [
      {
        "meaning": "(pos) Vietnamese meaning 1",
        "example": {
          "en": "English example sentence.",
          "vi": "Vietnamese translation of the example."
        }
      }
    ]
  }
]

## Script
[PASTE SCRIPT HERE]
