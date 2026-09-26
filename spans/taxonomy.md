# Protected Span Taxonomy

This document defines the protected span taxonomy used by VAAK. It is intentionally operational: another person should be able to label protected spans consistently from issue text alone.

The taxonomy contains exactly six protected categories:

1. identifier
2. file path
3. API name
4. exception type
5. command flag
6. version string

The categories are intended to be mutually distinguishable as much as reasonably possible. When an item could plausibly fall under more than one category, the boundary and precedence rules below determine the label.

---

## General labeling principles

1. Label only spans that are explicitly recoverable from the source issue text.
2. Do not infer hidden or implied identifiers that are not textually present.
3. Do not label broad prose phrases or natural-language descriptions.
4. If a token could match multiple categories, apply the precedence rule in this order:
   - file path
   - API name
   - exception type
   - command flag
   - version string
   - identifier
5. This precedence is only a tie-breaker for ambiguous strings that could otherwise satisfy more than one definition.
6. The goal is consistent annotation, not semantic guessing.

---

## 1. Identifier

### Definition

An identifier is a symbolic name used to refer to a program entity, variable, function, method, class, module, attribute, constant, or other software object.

It is a token that serves as a programmatic name, not ordinary prose.

### Included forms

- function names such as `compute_metrics`
- method names such as `to_dict`
- class names such as `MyClass`
- variable names such as `config_path`
- attribute names such as `__init__`
- module-like names when they are used as program symbols in context
- constant names such as `DEFAULT_TIMEOUT`

### Excluded forms

- ordinary English words used in prose
- file paths
- API names that are qualified object paths rather than standalone identifiers
- exception names that are class names but are being treated as exception types under their specific rule
- command flags
- version strings
- package names or library names when they are not clearly acting as code identifiers

### Clean boundary rule

An identifier should be labeled as a standalone symbol token, not as the surrounding sentence.

Boundary rules:

- Start and end on token boundaries.
- Do not include surrounding punctuation.
- Do not include leading or trailing quotes, brackets, or sentence punctuation.
- Do not capture adjacent prose words.
- If a symbol is part of a qualified API reference, prefer the API-name rule unless the symbol is clearly being used as a standalone identifier in a local naming context.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## 2. File path

### Definition

A file path is a string that identifies a file or directory location in a filesystem or repository.

### Included forms

- relative paths such as `src/config.py`
- nested paths such as `tests/unit/test_app.py`
- repository-rooted paths such as `docs/guide.md`
- Windows-style paths such as `C:\\temp\\logs\\app.log`
- paths with dot segments such as `./src/main.py` or `../lib/util.py`
- directories and files when they clearly function as paths rather than prose

### Excluded forms

- ordinary prose words that merely mention a filename without an actual path structure
- URLs unless the issue is explicitly describing a local filesystem path and the URL is being used as a path-like reference
- identifiers, API names, exception types, command flags, and version strings
- shell fragments that are not clearly file paths

### Clean boundary rule

A file path must include path separators or path-like structure that clearly indicates a file or directory location.

Boundary rules:

- Include the full path as it appears in text.
- Do not include trailing punctuation such as a comma or period unless it is part of the path token itself.
- Do not extend to surrounding prose.
- Prefer the full path string over a partial directory fragment when the full path is explicit.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## 3. API name

### Definition

An API name is the name of a callable software interface, library function, method, module attribute, or code-level service access pattern as it appears in software usage.

This category covers names that are invoked or referenced as interfaces, not ordinary local variables unless they are functionally acting as an API reference in context.

### Included forms

- qualified calls such as `requests.get`
- module and method patterns such as `json.loads`
- library call names such as `os.path.join`
- method names used as API references such as `session.close`
- object.method call patterns that clearly represent a callable interface

### Excluded forms

- local function names used as identifiers without API-like qualification
- file paths
- exception types
- command flags
- version strings
- ordinary English verbs or function names in a narrative sentence unless they are clearly being used as a code API

### Clean boundary rule

API names should be labeled as the qualified or callable symbol itself, not the surrounding surrounding sentence.

Boundary rules:

- Include the module and member path when both are present as a single API reference.
- Exclude surrounding punctuation.
- Do not include trailing parentheses unless they are part of the exact textual API reference in context.
- If a token looks like a plain identifier but is used as a call target with module qualification, treat it as an API name.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## 4. Exception type

### Definition

An exception type is the name of an exception, error class, or runtime error type in the source issue text.

### Included forms

- standard exception names such as `ValueError`
- module-specific error types such as `FileNotFoundError`
- custom exception class names when they are clearly used as exception types in issue text
- names of runtime failures written as class-like types

### Excluded forms

- ordinary prose references like "error" or "exception"
- identifiers that are not explicitly used as an exception type
- file paths
- command flags
- version strings
- API names unless the issue specifically names a class-like exception in API form

### Clean boundary rule

An exception type is the class name itself, not surrounding explanatory text.

Boundary rules:

- Include the class name exactly as written.
- Exclude surrounding punctuation.
- Do not include neighboring words such as "raises" or "error".
- If a name is both an identifier and an exception type, prefer the exception-type label only when it is explicitly used as the error class name in the issue text.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## 5. Command flag

### Definition

A command flag is a command-line option or switch used in software or shell commands.

### Included forms

- long flags such as `--verbose`
- short flags such as `-v`
- compound flags such as `--dry-run`
- flag-like options used in CLI invocations

### Excluded forms

- ordinary words that happen to start with a hyphen in prose
- version strings that look numeric
- identifiers or API references
- file paths
- exception types

### Clean boundary rule

A command flag is the option token itself, not the surrounding command text.

Boundary rules:

- Include the full flag token exactly as written.
- Do not include surrounding shell quoting unless the quote is part of the actual token string in the source text.
- Do not include the command name preceding the flag.
- Do not include trailing values unless the full value is part of the exact flag expression in the source text.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## 6. Version string

### Definition

A version string is a software, library, framework, package, language, or tool version identifier written in text.

### Included forms

- version numbers such as `3.11`
- multi-part versions such as `2.2.0`
- language versions such as `Python 3.11`
- prefixed versions such as `v2.3.1`
- package versions such as `pandas 2.2.0`

### Excluded forms

- ordinary numeric values that are not version-like
- dates or timestamps unless they are explicitly used as software versions in context
- file paths and identifiers containing periods but not serving as version strings
- command flags
- API names
- exception types

### Clean boundary rule

A version string is the version token itself, not adjacent prose.

Boundary rules:

- Include the version token exactly as written.
- Do not include surrounding words like "Python" or "pandas" unless they are part of a version expression that is explicitly documented as such in the issue text and should be labeled as a coordinated expression.
- Keep the match to the numeric version token itself when it is unambiguous.
- Do not silently normalize case or punctuation.

### Examples pending dataset access

- Example 1: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.
- Example 2: Pending frozen-50 dataset access; to be filled from the actual VAAK issue set.

---

## Precedence and ambiguity rules

Some strings could plausibly match more than one category. Use the following precedence to resolve ambiguous cases:

1. file path
2. API name
3. exception type
4. command flag
5. version string
6. identifier

This precedence applies only when the string can be reasonably interpreted under multiple labels. The purpose is to avoid inconsistent labels when the same token might otherwise belong to more than one category.

Examples:

- `src/config.py` is a file path, not an identifier.
- `requests.get` is an API name, not a plain identifier.
- `ValueError` is an exception type, not a generic identifier.
- `--verbose` is a command flag, not a version string.
- `3.11` is a version string, not a general numeric token.

---

## Remaining blocker

The taxonomy definitions, inclusion/exclusion rules, and boundary rules above are complete and operational.

The two real examples for each category remain blocked pending access to the actual frozen 50 SWE-bench issue set. Those example slots are intentionally left as placeholders and explicitly marked as pending dataset access.

This document does not invent issue examples or pretend to have the frozen 50. It remains a valid operational taxonomy definition while awaiting the real dataset.
