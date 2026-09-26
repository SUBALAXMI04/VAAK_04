# VAAK

## An Empirical Study of Spoken Software Task Instructions in Indian Languages

VAAK investigates how **spoken software task instructions in Indian languages** affect the performance of AI agents that perform software engineering tasks.

As AI coding agents increasingly interact with developers through natural language, software development is no longer limited to traditional text-based interfaces. Developers may provide instructions through speech, while multilingual developers may express those instructions in languages other than English. However, software instructions contain specialized information—such as identifiers, file paths, API names, exception types, command flags, and version strings—that may be particularly vulnerable to errors during translation, speech synthesis, speech recognition, and audio understanding.

VAAK studies this problem empirically by examining the interaction between **language, speech, and software-specific terminology**.

## Motivation

Previous work has shown that translating software engineering instructions into non-English languages can introduce a performance cost, while research on audio-based tool-calling agents has also observed a gap between text and voice interaction.

These observations raise an important question:

> **What happens when multilingual software instructions are also delivered through speech?**

The loss may not be limited to ordinary natural-language content. Software-specific tokens can be critical to completing a coding task correctly. A small change in an identifier, file path, API name, exception type, command flag, or version string can alter the meaning of an instruction or prevent an agent from correctly interacting with a software environment.

VAAK therefore examines whether spoken multilingual instructions introduce additional information loss and whether that loss affects software engineering task performance.

## Research Objective

The primary objective of VAAK is to measure the effect of **speech and multilingual interaction on software task instructions** and to identify whether software-specific information is preserved throughout the interaction pipeline.

The project particularly investigates:

* Whether protected software-specific spans survive translation and speech processing.
* Whether spoken instructions reduce the ability of AI agents to successfully resolve software engineering tasks.
* Whether speech introduces additional loss beyond multilingual text translation.
* Whether different audio-agent architectures behave differently.
* Whether the effects vary across Indian languages.
* Whether errors in protected software-specific information are associated with downstream task failures.

## Experimental Setup

VAAK uses software engineering issues as the source instructions and evaluates them under multiple interaction conditions.

The experimental conditions include:

1. **English Text Baseline**
   The original English software task instruction is provided as text.

2. **Translated Text Control**
   The instruction is translated into the target Indian language and provided as text. This provides a comparison for measuring the effect of language translation without speech.

3. **English Speech**
   The English instruction is converted to speech and provided through the speech interaction pipeline. This isolates the effect of speech from the effect of multilingual translation.

4. **Translated Speech**
   The instruction is translated into an Indian language, converted into speech, and provided to the agent.

5. **Cascade Speech Architecture**
   Audio is first processed by a speech-recognition system to obtain text, after which the resulting text is provided to the software agent.

6. **Omni Audio-Direct Architecture**
   Audio is provided directly to an audio-capable/omni-modal model without an explicit intermediate transcription stage.

These conditions allow the study to separate the effects of **translation, speech, recognition, and agent architecture**.

## Experimental Pipeline

The planned pipeline is:

```text
SWE-bench Issues
        │
        ▼
   Spokenization
        │
        ▼
Protected-Span Identification
        │
        ▼
    Translation
        │
        ▼
  Speech Synthesis
        │
        ▼
 Speech / Audio Agent
        │
        ▼
Software Engineering Task
        │
        ▼
     Evaluation
```

The study uses software engineering issues and prepares equivalent instructions for the different experimental conditions while preserving comparability between them.

## Protected Software Spans

A central component of VAAK is the identification of **protected spans**: pieces of software-specific information that should remain unchanged when an instruction is translated or converted into spoken form.

The project currently considers six categories:

* **Identifier** — names used to identify program entities or other software-specific objects.
* **File Path** — paths identifying files or directories.
* **API Name** — names of APIs or callable software interfaces.
* **Exception Type** — names of exception or error classes/types.
* **Command Flag** — command-line options or flags.
* **Version String** — software, library, framework, or tool version identifiers.

The taxonomy is defined using actual instances from the study rather than invented examples.

These spans are important because their alteration can change the meaning of a software task or make an instruction difficult for an agent to execute correctly.

## Spokenization

The project creates a spoken form of each software instruction before speech synthesis.

Spokenization converts a written issue into a plausible developer-spoken instruction while retaining the protected software spans exactly.

The spoken instructions are intended to:

* Use a natural spoken register.
* Avoid unnecessary written formatting.
* Preserve software-specific terminology.
* Maintain the meaning of the original issue.
* Provide a consistent basis for speech synthesis and evaluation.

## Translation

The translated instructions are produced while explicitly accounting for protected spans.

The purpose is not simply to translate ordinary natural-language content, but to examine whether important software-specific information survives the translation process.

The project also compares relevant instances against published multilingual software-engineering data where overlap exists, including the MAPS benchmark.

## Speech Synthesis

Translated and spoken instructions are converted into audio using speech-synthesis systems.

The synthesis stage is treated as a separate component of the experimental pipeline so that failures introduced by the audio itself can be distinguished from failures caused by recognition or agent reasoning.

Audio fidelity is evaluated for a subset of clips by checking whether the spoken instructions are understandable and whether protected spans remain audible.

## Speech-Agent Architectures

VAAK considers two major approaches to processing spoken instructions.

### Cascade Architecture

The audio is first passed through an automatic speech recognition system.

```text
Audio
  ↓
Speech Recognition
  ↓
Transcript
  ↓
Software Agent
```

This makes it possible to study information loss introduced by the speech-recognition stage.

### Omni-Modal Architecture

The audio is provided directly to an audio-capable model.

```text
Audio
  ↓
Omni-Modal Agent
  ↓
Software Task
```

This avoids requiring an explicit transcription stage and allows comparison between cascade and audio-direct interaction.

## Evaluation Metrics

VAAK evaluates both **information preservation** and **downstream software-task performance**.

### Protected-Span Preservation

The project defines a formal preservation measure for protected spans.

A protected span is considered preserved when the relevant software-specific value survives a processing stage according to the project's predefined matching procedure.

The metric measures the proportion of protected spans that remain intact.

The definition explicitly considers cases such as:

* Exact preservation.
* Case differences.
* Partial matches.
* Repeated occurrences of the same span.
* Completely dropped spans.
* Preservation in audio-only conditions where an explicit transcript may not exist.

### Task Resolution

The project measures whether the software engineering agent successfully resolves the underlying task.

This provides the downstream outcome against which information loss can be compared.

### Speech-Channel Loss

Speech-channel loss compares the performance of translated text instructions with the corresponding speech-based condition.

This helps isolate the additional effect introduced by the speech channel beyond translation itself.

### Architecture-by-Language Effects

The study examines whether the effect of language changes depending on whether the agent receives:

* Text,
* Recognized speech through a cascade, or
* Audio directly through an omni-modal model.

### Speech Fidelity

A subset of synthesized clips is manually evaluated for:

* Human intelligibility.
* Audibility of protected spans.

Recognition quality such as WER may also be used where applicable.

## Data and Evaluation Procedure

The initial study works with a frozen set of **50 software engineering issues**.

A subset of these instances is manually annotated to establish a gold standard for protected spans.

Two annotators independently label the same instances. Disagreements are resolved by refining the taxonomy and documenting the disagreement categories rather than simply choosing one annotator's label.

The resulting annotations are used to evaluate the automatic span-detection process and to establish the basis for the preservation metric.

The experimental evaluation uses repeated runs for agent conditions, with paired comparisons and statistical analysis planned according to the final experimental design.

## Quality Checks

VAAK includes several checks throughout the pipeline.

### Span Consistency

The project checks whether protected spans identified in the original written instruction are still present in the spokenized version.

### Detector Evaluation

Detector misses and false positives are manually inspected and categorized to understand why the automatic span detector fails.

### Translation Cross-Check

Where VAAK instances overlap with published multilingual software-engineering data, the corresponding translations are compared, with particular attention to protected-span preservation.

### Audio Evaluation

Synthesized audio clips are manually inspected to determine whether they are human-intelligible and whether protected software spans are audible.