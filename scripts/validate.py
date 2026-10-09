#!/usr/bin/env python3
"""Validate the MiniTools extension catalog using only the Python standard library."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "index.json"
PACKAGES_PATH = ROOT / "packages"
EVENTS_PATH = ROOT / "examples" / "notch-connect-events.json"

CAPABILITIES = {
    "applicationLaunch",
    "applicationDiscovery",
    "notifications",
    "processInspection",
    "processTermination",
    "screenshotEvents",
    "fileDragAndDrop",
    "keepAwake",
    "terminalSession",
}
PRESENTATIONS = {"compact", "expanded", "both"}
EVENT_NAMES = {
    "activity.started",
    "activity.updated",
    "activity.needsAttention",
    "activity.completed",
    "activity.failed",
    "activity.cancelled",
}
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")


class ValidationError(Exception):
    pass


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path.relative_to(ROOT)}: {error}") from error


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_manifest(manifest: dict, source: str) -> None:
    required = {
        "id",
        "name",
        "version",
        "minimumHostVersion",
        "contractVersion",
        "systemImage",
        "capabilities",
        "tabs",
        "priority",
    }
    missing = sorted(required - manifest.keys())
    require(not missing, f"{source}: missing fields: {', '.join(missing)}")
    require(manifest["contractVersion"] == "1", f"{source}: unsupported contractVersion")
    require(bool(SEMVER.fullmatch(manifest["version"])), f"{source}: invalid version")
    require(
        bool(SEMVER.fullmatch(manifest["minimumHostVersion"])),
        f"{source}: invalid minimumHostVersion",
    )
    capabilities = manifest["capabilities"]
    require(isinstance(capabilities, list), f"{source}: capabilities must be an array")
    unknown = sorted(set(capabilities) - CAPABILITIES)
    require(not unknown, f"{source}: unknown capabilities: {', '.join(unknown)}")
    require(len(capabilities) == len(set(capabilities)), f"{source}: duplicate capabilities")
    require(isinstance(manifest["tabs"], list) and manifest["tabs"], f"{source}: tabs required")
    for tab in manifest["tabs"]:
        require(
            {"id", "title", "systemImage", "presentation"} <= tab.keys(),
            f"{source}: incomplete tab",
        )
        require(tab["presentation"] in PRESENTATIONS, f"{source}: invalid presentation")


def validate_catalog() -> int:
    catalog = load_json(CATALOG_PATH)
    require(catalog.get("schemaVersion") == 1, "index.json: unsupported schemaVersion")
    plugins = catalog.get("plugins")
    require(isinstance(plugins, list) and plugins, "index.json: plugins must not be empty")

    identifiers: set[str] = set()
    for entry in plugins:
        identifier = entry.get("id", "<missing-id>")
        require(identifier not in identifiers, f"index.json: duplicate plugin {identifier}")
        identifiers.add(identifier)

        download_url = entry.get("downloadURL", "")
        parsed_url = urlparse(download_url)
        require(parsed_url.scheme == "https", f"{identifier}: downloadURL must use HTTPS")
        package_path = PACKAGES_PATH / Path(parsed_url.path).name
        require(package_path.is_file(), f"{identifier}: package file is missing")

        package_bytes = package_path.read_bytes()
        checksum = hashlib.sha256(package_bytes).hexdigest()
        require(checksum == entry.get("sha256"), f"{identifier}: SHA-256 mismatch")

        manifest = json.loads(package_bytes)
        validate_manifest(manifest, str(package_path.relative_to(ROOT)))
        for field in ("id", "name", "version", "minimumHostVersion", "capabilities"):
            require(entry.get(field) == manifest.get(field), f"{identifier}: catalog {field} mismatch")

    return len(plugins)


def validate_events() -> int:
    events = load_json(EVENTS_PATH)
    require(isinstance(events, list) and events, f"{EVENTS_PATH.name}: events required")
    for index, event in enumerate(events):
        prefix = f"{EVENTS_PATH.name}[{index}]"
        require(event.get("schemaVersion") == 1, f"{prefix}: invalid schemaVersion")
        require(event.get("event") in EVENT_NAMES, f"{prefix}: invalid event")
        source = event.get("source", {})
        require(source.get("bundleIdentifier") and source.get("name"), f"{prefix}: source required")
        activity = event.get("activity", {})
        require(activity.get("id") and activity.get("title"), f"{prefix}: activity required")
        progress = activity.get("progress")
        require(progress is None or 0 <= progress <= 100, f"{prefix}: invalid progress")
        require(event.get("timestamp"), f"{prefix}: timestamp required")
    return len(events)


def main() -> int:
    try:
        package_count = validate_catalog()
        event_count = validate_events()
    except (ValidationError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {package_count} packages and {event_count} Notch Connect examples validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
