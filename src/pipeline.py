from __future__ import annotations

from pathlib import Path

from src.dataset import DEFAULT_DATASET_PATH, load_instances, save_processed_instances
from src.spans import detect_spans

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.yaml"


def load_config(config_path: str | Path = DEFAULT_CONFIG_PATH) -> dict[str, str]:
    config: dict[str, str] = {}
    path = Path(config_path)
    if not path.exists():
        return config

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        config[key] = value.strip().strip('"\'')

    return config


def main() -> int:
    config = load_config()
    dataset_path = ROOT_DIR / config.get("input_dataset", "data/raw/issues.jsonl")
    output_path = ROOT_DIR / config.get("detected_spans_output", "spans/detected_spans.jsonl")

    try:
        issues = load_instances(dataset_path)
    except FileNotFoundError:
        print(f"Dataset file not found: {dataset_path}")
        print("The VAAK pipeline is ready, but the real dataset is missing.")
        return 0

    output_rows: list[dict[str, object]] = []
    for issue in issues:
        issue_id = issue["instance_id"]
        original_issue = issue["original_issue"]
        spans = detect_spans(original_issue)
        print(f"instance_id: {issue_id}")
        print(f"detected spans: {spans}")
        output_rows.append({"instance_id": issue_id, "spans": spans})

    save_processed_instances(output_rows, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
