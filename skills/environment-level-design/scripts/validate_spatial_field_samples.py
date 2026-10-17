#!/usr/bin/env python3
"""Compare recorded scalar field samples without granting visual approval."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


IDENTITY = ("field_id", "revision", "coordinate_frame", "units")


def number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{label} must be a number")
    try:
        result = float(value)
    except (ValueError, OverflowError) as error:
        raise ValueError(f"{label} must be finite") from error
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def identity(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("authority must be an object")
    result = {}
    for key in IDENTITY:
        item = value.get(key)
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"authority.{key} must be a nonempty string")
        result[key] = item
    return result


def samples(value: object) -> dict[str, tuple[tuple[float, ...], float]]:
    if not isinstance(value, list) or not value:
        raise ValueError("samples must be a nonempty list")
    result = {}
    for row in value:
        if not isinstance(row, dict):
            raise ValueError("sample must be an object")
        key = row.get("id")
        if not isinstance(key, str) or not key.strip() or key in result:
            raise ValueError("sample IDs must be nonempty and unique")
        position = row.get("position")
        if not isinstance(position, list) or len(position) != 3:
            raise ValueError(f"{key}: position must contain XYZ")
        xyz = tuple(number(v, f"{key}.position") for v in position)
        scalar = number(row.get("value"), f"{key}.value")
        if not 0 <= scalar <= 1:
            raise ValueError(f"{key}: field value must be in [0,1]")
        result[key] = (xyz, scalar)
    return result


def validate(data: object) -> dict[str, object]:
    """Return parity for the provided samples; reject malformed input explicitly."""
    limits = {"visual_approval": "NOT_GRANTED", "sample_provenance": "NOT_VERIFIED"}
    try:
        if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise ValueError("schema_version must be integer 1")
        authority = identity(data.get("authority"))
        tolerance = number(data.get("tolerance"), "tolerance")
        if not 0 <= tolerance <= 1:
            raise ValueError("tolerance must be in [0,1]")
        reference = samples(data.get("reference_samples"))
        consumers = data.get("consumers")
        if not isinstance(consumers, list) or not consumers:
            raise ValueError("consumers must be a nonempty list")
        rows, ids = [], set()
        for consumer in consumers:
            if not isinstance(consumer, dict):
                raise ValueError("consumer must be an object")
            key = consumer.get("id")
            if not isinstance(key, str) or not key.strip() or key in ids:
                raise ValueError("consumer IDs must be nonempty and unique")
            ids.add(key)
            if identity(consumer) != authority:
                raise ValueError(f"{key}: field identity, revision, coordinates or units differ")
            actual = samples(consumer.get("samples"))
            if set(actual) != set(reference):
                raise ValueError(f"{key}: sample coverage differs")
            errors = []
            for sid, (position, expected) in reference.items():
                if actual[sid][0] != position:
                    raise ValueError(f"{key}/{sid}: sample positions differ")
                errors.append(abs(actual[sid][1] - expected))
            maximum = max(errors)
            rows.append({"id": key, "samples": len(errors), "max_absolute_error": maximum, "within_tolerance": maximum <= tolerance})
        return {"status": "PASS_PARITY_ONLY" if all(r["within_tolerance"] for r in rows) else "FAIL_PARITY", "authority": authority, "tolerance": tolerance, "consumers": rows, **limits}
    except ValueError as error:
        return {"status": "INVALID_INPUT", "error": str(error), **limits}


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject ambiguous JSON objects instead of silently keeping the last key."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.samples.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object))
    except (OSError, UnicodeError, ValueError) as error:
        result = {"status": "INVALID_INPUT", "error": str(error), "visual_approval": "NOT_GRANTED", "sample_provenance": "NOT_VERIFIED"}
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["status"] == "PASS_PARITY_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
