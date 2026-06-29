# Vocabulary Definition Prompt

You are given a list of English vocabulary words. For each English word, provide the 3 most common Vietnamese meanings. Each meaning must include a clear example sentence in English and its Vietnamese translation. Return the result strictly as a JSON array and save it to a JSON file.

## Output Structure

Each item in the array must be an object with this structure:

```json
[
  {
    "vocabulary": "word",
    "ipa": "US IPA transcription",
    "meanings": [
      {
        "meaning": "Vietnamese meaning 1",
        "example": {
          "en": "English example sentence.",
          "vi": "Vietnamese translation of the example."
        }
      }
    ]
  }
]
```

## Rules

- Pick the 3 most common meanings for each word. If a word has more than 3 common meanings, feel free to include more than 3.
- If a word has fewer than 3 common meanings, return only the available common meanings.
- The examples should be natural and easy to understand.
- Do not include any explanations outside the JSON array.
- Make sure the output is valid JSON and save it to a JSON file.
- Attach the US IPA for each word.
- If any word in the list has a grammar or spelling error, correct it.

## Words

(One per line below.)

```

```
