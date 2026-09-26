# Identifier Preservation Rate

## Definition

Identifier Preservation Rate (IPR) is the proportion of protected identifier spans that survive a processing stage byte identical.

Formally:

$$
\mathrm{IPR} = \frac{\sum_{i=1}^{N} \mathbf{1}[\text{protected span } i \text{ survives byte-identically}]}{N}
$$

where $N$ is the total number of protected identifier spans considered for the stage under evaluation.

This metric is defined for protected identifier spans only, and it is applied after a stage of interest has processed the original instruction (for example, translation, spokenization, speech synthesis, ASR transcription, or OMNI audio processing).

---

## Protected span set

Let the set of protected spans in the original instruction be:

$$
S = \{s_1, s_2, \ldots, s_N\}
$$

Each protected span $s_i$ has:

- a span text,
- a protected type,
- and a source occurrence in the original instruction.

For this metric, the relevant span class is identifier spans, as defined by the VAAK protected-span taxonomy.

---

## Numerator

The numerator is the count of protected identifier spans that survive a processing stage under the rule below.

$$
\mathrm{Numerator} = \sum_{i=1}^{N} \mathbf{1}[\mathrm{survives}(s_i)]
$$

A protected span survives if and only if the processed output contains a corresponding identifier occurrence that is byte identical to the original span text according to the exact matching rule defined below.

---

## Denominator

The denominator is the total number of protected identifier spans in the original instruction.

$$
\mathrm{Denominator} = N
$$

This denominator is fixed by the protected-span annotation set for the original instruction, not by the number of matches found after processing.

---

## What "byte identical" means

A protected span survives byte identically when the processed representation contains the same byte sequence as the original protected span text, with no edits, insertions, deletions, or normalization changes.

More formally, let the original protected span text be $t$ and the candidate processed text be $u$. The span survives byte identically if and only if:

$$
\mathrm{bytes}(u) = \mathrm{bytes}(t)
$$

This is an exact string equality check on the underlying bytes, not a case-folded or normalized comparison.

Examples:

- `compute_metrics` survives if the processed output contains exactly `compute_metrics`.
- `compute_metrics` does not survive if it appears as `Compute_Metrics`.
- `compute_metrics` does not survive if it appears as `compute_metric`.
- `compute_metrics` does not survive if it is partially embedded in a larger token without exact byte equality.

The comparison is performed on the protected span text itself, not on a semantic interpretation or a reconstructed token.

---

## Case changes

Case changes do not count as survival.

A span is not counted as preserved when the same identifier differs only by case, even if it is otherwise the same word. For example:

- `FooBar` survives only if the processed output contains exactly `FooBar`.
- `foobar` does not count as survival of `FooBar`.
- `FOOBAR` does not count as survival of `FooBar`.

This rule is intentionally strict so that the metric measures exact preservation, not approximate matching.

---

## Partial matches

Partial matches do not count.

A protected span is not considered preserved when the processed output contains only a substring, a prefix, a suffix, or a distorted form of the original span. For example:

- `compute_metrics` is not preserved by `compute_metric`.
- `read_csv` is not preserved by `csv_read`.
- `parse_args` is not preserved by `parse`.

The requirement is exact byte identity of the protected span text itself.

---

## Repeated occurrences

Each input protected span occurrence is evaluated separately.

Repeated identical strings are separate occurrences and are counted separately in the denominator and numerator.

Rules:

- Each input protected span occurrence contributes one count to the denominator.
- Each output occurrence can match at most one input occurrence.
- One output occurrence cannot preserve multiple input occurrences.
- If two input occurrences exist but only one exact output occurrence exists, preservation is 1/2.
- Matching must respect occurrence identity and boundaries; one substring may not be counted as preserving multiple spans.

Concrete example:

```text
input: foo foo
output: foo
```

There are two protected input occurrences of `foo`, but only one exact output occurrence of `foo`. Therefore:

- denominator = 2
- numerator = 1
- IPR = 1/2 = 0.50

Another example:

```text
input: MyClass MyClass
output: MyClass MyClass
```

Both occurrences survive, so numerator = 2 and denominator = 2.

---

## Dropped spans

If a protected span is absent from the output, it is a preservation failure.

A dropped span:

- remains in the denominator,
- contributes 0 to the numerator,
- must not be removed from the denominator.

Concrete example:

```text
input protected spans: [foo, bar]
output text: [foo]
```

- `foo` survives: numerator += 1
- `bar` is missing: numerator += 0
- denominator remains 2
- IPR = 1/2 = 0.50

A protected span is considered dropped if it is missing, changed, partially changed, case-changed, normalized, or otherwise non-identical.

---

## Direct-text procedure

For stages with text output:

1. Start with the protected spans identified in the input.
2. For each protected occurrence, locate the corresponding output occurrence/value.
3. Count it as preserved only when the output value is byte-identical to the original protected span.
4. Count missing, changed, partial, case-changed, normalized, or otherwise non-identical values as failures.
5. Compute numerator / denominator.

This procedure applies to direct textual outputs such as translated text, transcript text, or other text-stage outputs.

Do not introduce fuzzy matching, semantic matching, or case-insensitive matching.

---

## OMNI indirect procedure

The OMNI condition has no explicit transcript.

Define the procedure before any experimental results exist.

For each expected protected span in the input:

1. Identify the corresponding structured tool-call argument/value produced by the OMNI system.
2. Count the span as preserved only if the exact byte sequence of the expected protected span appears as the relevant generated argument/value.
3. Do not claim that raw audio preserved the span merely because the final tool call contains the correct value.
4. Do not use semantic equivalence, case-insensitive comparison, fuzzy matching, or human interpretation.
5. If no tool call is produced, the relevant argument is missing, or the generated value is changed, partial, or otherwise non-identical, count the protected span as NOT preserved.
6. If the same value appears in multiple arguments, use the argument corresponding to the expected tool-call field; do not arbitrarily select another occurrence.
7. Each expected input occurrence must be accounted for exactly once.

This OMNI procedure is an indirect operational measure of protected-span preservation. It measures whether the expected protected value survives into the model's structured tool-call output; it does not establish that the raw audio itself contained that exact byte sequence.

---

## Edge cases

The following cases are treated as failures unless the exact byte sequence is preserved:

- missing tool call
- missing argument
- wrong argument value
- partial value
- repeated values
- case changes
- Unicode/normalization differences
- extra surrounding text

Examples:

- `MyClass` vs `myclass` -> failure
- `v2.3.1` vs `2.3.1` -> failure
- `--verbose` vs `--verbose=true` -> failure
- `MyClass` vs `MyClassName` -> failure
- `foo` appearing twice in input and once in output -> one preserved, one failure
- Unicode normalization differences such as `é` vs composed/decomposed forms -> failure unless bytes are exactly identical

---

## Formula and example

The metric is:

$$
\mathrm{IPR} = \frac{\text{number of protected span occurrences surviving byte-identically}}{\text{total number of protected span occurrences in the input}}
$$

Example:

- 10 protected span occurrences in the input
- 8 survive byte-identically
- IPR = 8/10 = 0.80 = 80%

### Denominator zero case

If there are no protected spans in the input being evaluated, then the denominator is zero.

In that case, IPR is undefined / not applicable for that instance and should not be silently assigned a value such as 100%.

When aggregating across multiple instances, the implementation should handle the zero-denominator case explicitly, for example by excluding that instance from the denominator or reporting it as not applicable, rather than pretending it is a perfect preservation case.

---

## Scope and limitation

Task 4 defines the metric only. It does not claim any experimental result and does not modify the detector or other pipeline components.

This document is a formal definition of the preservation metric. It is not a claim about model performance, dataset quality, or any downstream experimental result.

---

## Final statement

This document defines the numerator, denominator, byte-identical matching rule, case handling, partial-match rule, repeated-occurrence handling, dropped-span handling, direct-text procedure, OMNI indirect procedure, edge cases, formula, and the zero-denominator policy necessary for a defensible preservation metric.

The metric is therefore fully specified before any experimental results exist.
