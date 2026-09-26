import pytest

from src.spans import detect_spans


def test_identifier_spans():
    text = "The function compute_metrics should be updated."
    spans = detect_spans(text)
    assert any(span["span_type"] == "identifier" and span["span_text"] == "compute_metrics" for span in spans)


def test_file_path_spans():
    text = "Check src/config.py and tests/test_app.py for the regression."
    spans = detect_spans(text)
    assert any(span["span_type"] == "file_path" and span["span_text"] == "src/config.py" for span in spans)
    assert any(span["span_type"] == "file_path" and span["span_text"] == "tests/test_app.py" for span in spans)


def test_api_name_spans():
    text = "Call requests.get and json.loads to parse the response."
    spans = detect_spans(text)
    assert any(span["span_type"] == "api_name" and span["span_text"] == "requests.get" for span in spans)
    assert any(span["span_type"] == "api_name" and span["span_text"] == "json.loads" for span in spans)


def test_exception_type_spans():
    text = "The code raises ValueError and FileNotFoundError when parsing the input."
    spans = detect_spans(text)
    assert any(span["span_type"] == "exception_type" and span["span_text"] == "ValueError" for span in spans)
    assert any(span["span_type"] == "exception_type" and span["span_text"] == "FileNotFoundError" for span in spans)


def test_command_flag_spans():
    text = "Run the command with --verbose --dry-run and then exit."
    spans = detect_spans(text)
    assert any(span["span_type"] == "command_flag" and span["span_text"] == "--verbose" for span in spans)
    assert any(span["span_type"] == "command_flag" and span["span_text"] == "--dry-run" for span in spans)


def test_version_string_spans():
    text = "This issue affects Python 3.11 and pandas 2.2.0."
    spans = detect_spans(text)
    assert any(span["span_type"] == "version_string" and span["span_text"] == "3.11" for span in spans)
    assert any(span["span_type"] == "version_string" and span["span_text"] == "2.2.0" for span in spans)
