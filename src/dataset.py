from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = ROOT_DIR / "data" / "raw" / "issues.jsonl"


def _normalize_issue(raw_issue: dict[str, Any]) -> dict[str, str]:
    instance_id = (
        raw_issue.get("instance_id")
        or raw_issue.get("instanceId")
        or raw_issue.get("id")
    )
    original_issue = (
        raw_issue.get("original_issue")
        or raw_issue.get("issue")
        or raw_issue.get("problem")
        or raw_issue.get("text")
    )

    if instance_id is None or original_issue is None:
        raise ValueError(f"Issue record is missing required fields: {raw_issue}")

    return {
        "instance_id": str(instance_id),
        "original_issue": str(original_issue),
    }


def load_instances(dataset_path: str | Path = DEFAULT_DATASET_PATH) -> list[dict[str, str]]:
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        if isinstance(payload, list):
            issues = payload
        elif isinstance(payload, dict):
            issues = payload.get("instances", payload.get("data", []))
        else:
            issues = []

        return [_normalize_issue(issue) for issue in issues]

    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        issues: list[dict[str, str]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    raw_issue = json.loads(stripped)
                except json.JSONDecodeError as exc:  # pragma: no cover - defensive guard
                    raise ValueError(f"Invalid JSON on line {line_number} in {path}") from exc
                issues.append(_normalize_issue(raw_issue))
        return issues

    raise ValueError(f"Unsupported dataset format for {path}. Use JSON or JSONL.")


def save_processed_instances(
    instances: Iterable[dict[str, Any]],
    output_path: str | Path,
) -> Path:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as handle:
        for instance in instances:
            handle.write(json.dumps(instance, ensure_ascii=False))
            handle.write("\n")

    return destination
