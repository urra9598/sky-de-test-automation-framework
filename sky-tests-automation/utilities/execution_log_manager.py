"""Execution log manager

Provides utilities to save the latest execution report to
`<repo>/sky-tests-automation/reports/latest_execution_logs.log` and
rotate any existing log to `log_<timestamp>.log` before writing the new one.

Functions:
- save_execution_report(report, logs_dir=None, log_name='latest_execution_logs.log')
- read_latest_report(logs_dir=None, log_name='latest_execution_logs.log')
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from typing import List

try:
    # prefer using the project's ConfigManager if available
    from utilities.config_manager import config as CONFIG
except Exception:
    CONFIG = None

LOG = logging.getLogger(__name__)


def _default_reports_dir() -> Path:
    """Return the default reports directory at repo root.
    
    This utility is at: repo_root/sky-tests-automation/utilities/execution_log_manager.py
    parents[2] = repo_root
    reports_dir = repo_root / "reports"  (at repo root, not inside sky-tests-automation)
    """
    try:
        script_path = Path(__file__).resolve()
        repo_root = script_path.parents[2]
        return repo_root / "reports"
    except Exception:
        # Fallback: relative to this file (but this shouldn't happen)
        return Path(__file__).resolve().parents[1].parent / "reports"


def _timestamp(fmt: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.now().strftime(fmt)


def _rotate_file(path: Path, timestamp_fmt: str = "%Y%m%d_%H%M%S") -> Optional[Path]:
    """If `path` exists, rename it to `log_<timestamp>.log` and return the new path.
    Returns None if no rotation was necessary.
    """
    if not path.exists():
        return None
    ts = _timestamp(timestamp_fmt)
    new_name = f"log_{ts}.log"
    target = path.with_name(new_name)
    path.rename(target)
    LOG.debug("Rotated log %s -> %s", path, target)
    return target


def save_execution_report(
    report: Union[dict, str],
    logs_dir: Optional[Union[str, Path]] = None,
    log_name: str = "latest_execution_logs.log",
    as_json: bool = True,
    timestamp_fmt: str = "%Y%m%d_%H%M%S",
) -> Path:
    """Write `report` to `logs_dir/log_name`. If a previous file exists it will be
    rotated to `log_<timestamp>.log`.

    - report: dict or string to write. If dict and as_json=True the file will be JSON.
    - logs_dir: directory to place logs (defaults to <repo>/sky-tests-automation/reports)
    - log_name: filename for the latest log (default: latest_execution_logs.log)
    - timestamp_fmt: timestamp format used for rotated file names

    Returns the Path to the newly written latest log file.
    """
    logs_path = Path(logs_dir) if logs_dir else _default_reports_dir()
    logs_path.mkdir(parents=True, exist_ok=True)

    latest_path = logs_path / log_name

    try:
        _rotate_file(latest_path, timestamp_fmt=timestamp_fmt)
    except Exception:
        LOG.exception("Failed rotating existing log file: %s", latest_path)

    # Write the new latest log
    if isinstance(report, dict) and as_json:
        # serialize as pretty JSON
        with latest_path.open("w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
    else:
        with latest_path.open("w", encoding="utf-8") as fh:
            fh.write(str(report))

    LOG.info("Saved latest execution report to %s", latest_path)

    # Enforce retention policy for rotated logs
    try:
        retention = None
        if CONFIG:
            try:
                retention = int(CONFIG.get("log_retention", 10))
            except Exception:
                retention = 10
        else:
            retention = 10

        if retention and retention > 0:
            _enforce_retention(logs_path, pattern="log_*.log", keep=retention)
    except Exception:
        LOG.exception("Failed to enforce log retention policy")
    return latest_path


def _enforce_retention(logs_path: Path, pattern: str = "log_*.log", keep: int = 10) -> None:
    """Keep only the most recent `keep` files matching `pattern` in `logs_path`.
    Older files are deleted. Matching is based on file modification time.
    """
    if keep <= 0:
        return

    files: List[Path] = [p for p in logs_path.glob(pattern) if p.is_file()]
    # Sort by modification time (newest first)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    # Files to remove
    to_remove = files[keep:]
    for f in to_remove:
        try:
            f.unlink()
            LOG.debug("Removed old rotated log: %s", f)
        except Exception:
            LOG.exception("Failed to remove old rotated log: %s", f)


def read_latest_report(
    logs_dir: Optional[Union[str, Path]] = None,
    log_name: str = "latest_execution_logs.log",
) -> Optional[Union[dict, str]]:
    """Read and return the latest execution report. If it's JSON, return dict, else string.
    Returns None if file does not exist.
    """
    logs_path = Path(logs_dir) if logs_dir else _default_reports_dir()
    latest_path = logs_path / log_name
    if not latest_path.exists():
        return None

    text = latest_path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except Exception:
        return text
