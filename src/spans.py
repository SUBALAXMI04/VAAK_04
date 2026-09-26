from __future__ import annotations

import re
from typing import Any


IDENTIFIER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:[a-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_]*[A-Z][A-Za-z0-9_]*)\b"
)
FILE_PATH_RE = re.compile(
    r"(?<![\w./])(?:\.\.?/)?(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)?(?![\w.])"
    r"|(?<!\S)(?:[A-Za-z]:)?(?:[\\/][A-Za-z0-9_.-]+)+"
)
API_NAME_RE = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_]*\.)+[A-Za-z_][A-Za-z0-9_]*\b")
EXCEPTION_TYPE_RE = re.compile(r"\b(?:[A-Z][A-Za-z0-9_]*Error|[A-Z][A-Za-z0-9_]*Exception)\b")
COMMAND_FLAG_RE = re.compile(r"(?<!\S)(?:--[A-Za-z0-9][A-Za-z0-9-]*|-[A-Za-z0-9])\b")
VERSION_STRING_RE = re.compile(r"(?<!\d)(?:v?\d+\.\d+(?:\.\d+)*)(?!\d)")


def _make_span(span_text: str, span_type: str, start: int, end: int) -> dict[str, Any]:
    return {
        "span_text": span_text,
        "span_type": span_type,
        "char_start": start,
        "char_end": end,
    }


def _deduplicate_spans(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority = {
        "file_path": 0,
        "api_name": 1,
        "exception_type": 2,
        "command_flag": 3,
        "version_string": 4,
        "identifier": 5,
    }

    accepted: list[dict[str, Any]] = []
    for span in sorted(
        spans,
        key=lambda item: (
            item["char_start"],
            -(item["char_end"] - item["char_start"]),
            priority.get(item["span_type"], 99),
        ),
    ):
        overlaps = False
        for chosen in accepted:
            if max(span["char_start"], chosen["char_start"]) < min(span["char_end"], chosen["char_end"]):
                overlaps = True
                break
        if not overlaps:
            accepted.append(span)

    accepted.sort(key=lambda item: item["char_start"])
    return accepted


def detect_spans(text: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []

    for pattern, span_type in (
        (FILE_PATH_RE, "file_path"),
        (API_NAME_RE, "api_name"),
        (EXCEPTION_TYPE_RE, "exception_type"),
        (COMMAND_FLAG_RE, "command_flag"),
        (VERSION_STRING_RE, "version_string"),
        (IDENTIFIER_RE, "identifier"),
    ):
        for match in pattern.finditer(text):
            span_text = match.group(0)
            start, end = match.span()
            matches.append(_make_span(span_text, span_type, start, end))

    return _deduplicate_spans(matches)
