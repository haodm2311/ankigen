# Book Vocabulary Extraction Prompt

You are given the text of a book, book chapter, or uploaded book file. Analyze the content and automatically extract useful English vocabulary, phrasal verbs, collocations, and idioms.

A book may contain multiple units. Each unit may contain sections labeled `A`, `B`, `C`, `D`, and `E`.

Detect the units and sections automatically. Process every available section in each unit and create one separate `book_vocabulary.json` file for each unit.

## Input

The input may be:

* A complete book
* A book containing multiple units
* One or more book chapters
* Extracted text from a PDF, EPUB, DOCX, or TXT file
* A pasted passage from a book

Do not expect vocabulary items to be provided one per line. Identify and extract them automatically from the book content.

## Unit Detection

A book may contain units labeled in different ways, such as:

* `Unit 1`, `Unit 2`, `Unit 3`
* `UNIT ONE`, `UNIT TWO`
* `Lesson 1`, `Lesson 2`
* `Chapter 1`, `Chapter 2`
* Named units without unit numbers

Detect units by examining:

* Headings
* Page structure
* Table-of-contents information
* Unit numbers and titles
* Repeated formatting patterns

Follow these rules:

* Process each unit independently.
* Preserve the original unit order.
* Do not combine vocabulary from different units.
* Remove duplicate expressions only within the same unit.
* The same expression may appear in multiple unit files if it occurs in multiple units.
* Ignore copyright pages, indexes, answer keys, and appendices unless they are explicitly part of a unit.
* If no identifiable units exist, treat the entire book as one unit named `unit_01`.

## Section Detection

Each unit may contain sections labeled:

* `A`
* `B`
* `C`
* `D`
* `E`

Section headings may appear in formats such as:

* `A`
* `A.`
* `Section A`
* `Part A`
* `A: Reading`
* `A. Getting Started`
* `B. Conversation`
* `C. Grammar`
* `D. Practice`
* `E. Review`

Detect section boundaries by examining:

* Lettered headings
* Heading styles
* Font and layout patterns
* Page boundaries
* Repeated section structures
* Titles following section letters

## Section Processing Rules

* Examine every available section in each unit.
* Process sections in their original order: `A`, `B`, `C`, `D`, and `E`.
* Do not stop after the first section.
* Do not skip sections containing exercises or instructional content.
* Extract useful language from:

  * Reading passages
  * Dialogues
  * Stories
  * Listening transcripts
  * Grammar explanations
  * Grammar examples
  * Vocabulary exercises
  * Speaking activities
  * Questions
  * Instructions
  * Example sentences
  * Review exercises
  * Answer choices that contain meaningful vocabulary or expressions
* If a section is missing, process all available sections without inventing it.
* If no section headings are detected, process the complete unit as one section.
* A unit is complete only after all its available sections have been examined.
* Combine the extracted results from all sections of the unit into one `book_vocabulary.json` file.

## Items to Extract

Extract the following language items.

### Vocabulary

Extract useful:

* Nouns
* Verbs
* Adjectives
* Adverbs
* Intermediate or advanced words
* Words that may be difficult for English learners
* Words important for understanding the unit

### Phrasal Verbs

Extract complete phrasal verbs, such as:

* `give up`
* `look into`
* `run out of`
* `put up with`
* `look forward to`

Preserve the full phrasal verb. Do not extract only the main verb.

### Collocations

Extract natural word combinations, such as:

* `make a decision`
* `heavy rain`
* `deeply concerned`
* `take responsibility`
* `reach an agreement`
* `strongly recommend`

Preserve the complete collocation.

### Idioms

Extract complete idiomatic expressions, such as:

* `break the ice`
* `under the weather`
* `get cold feet`
* `by the skin of your teeth`

Preserve the complete idiom.

## Items Not to Extract

Do not extract:

* Proper names unless they also have a common dictionary meaning
* Page numbers
* Headers and footers
* Unit numbers
* Section letters by themselves
* Exercise numbers
* Formatting artifacts
* Random or incomplete sentence fragments
* Extremely basic words such as `the`, `a`, `book`, `good`, or `go`
* Expressions that only make sense within the book's fictional context
* Individual words when the complete phrasal verb, collocation, or idiom is more useful
* Duplicate expressions within the same unit

## Output Directory Structure

Create one directory for every detected unit.

Save one file named `book_vocabulary.json` inside each unit directory.

```text
output/
├── unit_01/
│   └── book_vocabulary.json
├── unit_02/
│   └── book_vocabulary.json
├── unit_03/
│   └── book_vocabulary.json
└── unit_04/
    └── book_vocabulary.json
```

Each unit file must include expressions extracted from all available sections in that unit.

For example:

```text
Unit 1
├── Section A
├── Section B
├── Section C
├── Section D
└── Section E
```

All extracted expressions from sections A through E must be combined into:

```text
output/unit_01/book_vocabulary.json
```

Do not create a separate JSON file for each section.

Do not create one combined JSON file for the entire book.

## Unit Directory Names

Use two-digit sequential unit numbers:

```text
unit_01
unit_02
unit_03
...
unit_10
unit_11
```

When a unit has a meaningful title, the title may optionally be included:

```text
unit_01_getting_started
unit_02_daily_routines
```

Directory names must:

* Use lowercase letters
* Replace spaces with underscores
* Remove punctuation and special characters
* Remain concise
* Preserve the original unit order

## Required JSON Output Structure

Each `book_vocabulary.json` file must contain one valid JSON array.

The output must use exactly this structure:

```json
[
  {
    "vocabulary": "word",
    "ipa": "US IPA transcription",
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
```

Use the `vocabulary` field for every extracted item, including:

* Single vocabulary words
* Phrasal verbs
* Collocations
* Idioms

Examples:

```json
[
  {
    "vocabulary": "resilient",
    "ipa": "/rɪˈzɪliənt/",
    "meanings": [
      {
        "meaning": "(adj) kiên cường, có khả năng phục hồi nhanh",
        "example": {
          "en": "Children are often more resilient than adults expect.",
          "vi": "Trẻ em thường kiên cường hơn người lớn nghĩ."
        }
      }
    ]
  },
  {
    "vocabulary": "carry out",
    "ipa": "/ˈkæri aʊt/",
    "meanings": [
      {
        "meaning": "(phr v) thực hiện, tiến hành",
        "example": {
          "en": "The researchers carried out several experiments.",
          "vi": "Các nhà nghiên cứu đã tiến hành một số thí nghiệm."
        }
      }
    ]
  },
  {
    "vocabulary": "make a decision",
    "ipa": "/meɪk ə dɪˈsɪʒən/",
    "meanings": [
      {
        "meaning": "(collocation) đưa ra quyết định",
        "example": {
          "en": "You should consider all the facts before making a decision.",
          "vi": "Bạn nên cân nhắc tất cả các dữ kiện trước khi đưa ra quyết định."
        }
      }
    ]
  },
  {
    "vocabulary": "break the ice",
    "ipa": "/breɪk ði aɪs/",
    "meanings": [
      {
        "meaning": "(idiom) phá vỡ sự ngượng ngùng ban đầu",
        "example": {
          "en": "The teacher told a joke to break the ice.",
          "vi": "Giáo viên kể một câu chuyện cười để phá vỡ sự ngượng ngùng ban đầu."
        }
      }
    ]
  }
]
```

Do not add fields such as:

* `type`
* `source`
* `unit`
* `section`
* `book_context`
* `frequency`
* `difficulty`
* `notes`

Each object must contain only:

* `vocabulary`
* `ipa`
* `meanings`

## Expression Normalization Rules

Use the standard dictionary form whenever appropriate:

* `walked` → `walk`
* `running` → `run`
* `children` → `child`
* `gave up` → `give up`
* `carried out` → `carry out`
* `made a decision` → `make a decision`

Do not incorrectly reduce fixed expressions:

* Keep `look forward to`, not `look`
* Keep `put up with`, not `put`
* Keep `make a decision`, not `decision`
* Keep `break the ice`, not `break`

Correct obvious spelling or grammar errors before adding an expression.

## Duplicate Rules

* Remove duplicate expressions within the same unit.
* Compare expressions without considering capitalization.
* Treat inflected forms as duplicates of their normalized dictionary form.
* If an expression occurs in sections A and C of the same unit, include it only once.
* Preserve its position based on where it first appears in the unit.
* The same expression may appear again in another unit's JSON file.

## Meaning Rules

For each vocabulary item:

* Provide the three most common Vietnamese meanings.
* If fewer than three common meanings exist, include only the available meanings.
* More than three meanings may be included only when they are common and useful.
* Prioritize meanings relevant to the expression's use in the book.
* Do not include rare or highly technical meanings merely to reach three meanings.
* Keep clearly different meanings in separate objects inside `meanings`.

Prefix every Vietnamese meaning with the correct part-of-speech tag:

* `(v)` verb
* `(n)` noun
* `(adj)` adjective
* `(adv)` adverb
* `(prep)` preposition
* `(conj)` conjunction
* `(phr v)` phrasal verb
* `(collocation)` collocation
* `(idiom)` idiom

The tag must match the specific meaning.

Example:

```json
{
  "vocabulary": "address",
  "ipa": "/əˈdres/",
  "meanings": [
    {
      "meaning": "(v) giải quyết, xử lý",
      "example": {
        "en": "The company must address the problem immediately.",
        "vi": "Công ty phải giải quyết vấn đề ngay lập tức."
      }
    },
    {
      "meaning": "(v) phát biểu hoặc nói chuyện với",
      "example": {
        "en": "The president addressed the audience.",
        "vi": "Tổng thống đã phát biểu trước khán giả."
      }
    },
    {
      "meaning": "(n) địa chỉ",
      "example": {
        "en": "Please write your home address on the form.",
        "vi": "Vui lòng viết địa chỉ nhà của bạn vào biểu mẫu."
      }
    }
  ]
}
```

## IPA Rules

* Use US IPA transcription.
* Include IPA for every extracted item.
* For phrasal verbs, provide IPA for the complete expression.
* For collocations, provide IPA for the complete expression.
* For idioms, provide IPA for the complete expression.
* Use one consistent American pronunciation.
* Do not use British IPA unless the book explicitly teaches British English.

## Example Rules

Each meaning must include:

* One natural English example
* One accurate Vietnamese translation

Examples must:

* Clearly demonstrate the corresponding meaning
* Be grammatically correct
* Sound natural
* Be easy to understand
* Be newly written
* Not copy long sentences from the book
* Not reuse the same example for different meanings

## JSON Validation Rules

For every unit:

* Return a valid JSON array.
* Use exactly the required structure.
* Do not include Markdown in the JSON file.
* Do not include comments.
* Do not include explanations before or after the JSON array.
* Do not use trailing commas.
* Escape quotation marks, backslashes, line breaks, and special characters correctly.
* Use UTF-8 encoding so Vietnamese characters are preserved.
* Ensure every item contains `vocabulary`, `ipa`, and `meanings`.
* Ensure every meaning contains `meaning` and `example`.
* Ensure every example contains `en` and `vi`.
* Validate the JSON before saving it.

Save each result as:

```text
output/<unit_directory>/book_vocabulary.json
```

## Completeness Validation

Before saving each unit file, verify that:

1. The unit was detected correctly.
2. Every available section from A through E was examined.
3. No available section was skipped.
4. Vocabulary was extracted from passages, dialogues, examples, instructions, and exercises.
5. Phrasal verbs, collocations, and idioms were preserved as complete expressions.
6. Duplicate expressions were removed within the unit.
7. Every item uses the required JSON structure.
8. The JSON is valid.
9. The unit has exactly one `book_vocabulary.json` file.

Do not include this validation checklist inside the JSON file.

## Processing Large Books

For large books:

1. Detect all units.
2. Detect sections A through E inside each unit.
3. Process one unit at a time.
4. Process every available section in the unit.
5. Extract vocabulary, phrasal verbs, collocations, and idioms.
6. Normalize expressions into dictionary forms.
7. Remove duplicates within the unit.
8. Generate Vietnamese meanings and examples.
9. Validate the JSON.
10. Save the unit's `book_vocabulary.json` file.
11. Continue with the next unit.
12. Confirm that every detected unit has one output file.

Do not save a unit file until every available section in that unit has been processed.

## Book Content

Analyze the book content supplied in the attached file 
