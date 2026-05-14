"""Squad reference utilities."""

from __future__ import annotations

from typing import TypedDict
from uuid import UUID

from ulid import ULID

from app.core.config import get_settings


class TransferRefParts(TypedDict):
    merchant_id: str
    job_short: str
    ulid: str


def build_transfer_ref(job_id: UUID) -> str:
    """Build a Squad-compliant transfer reference.

    Squad requires the merchant ID prefixed onto every transfer transaction reference.
    """
    settings = get_settings()
    merchant_id = settings.SQUAD_MERCHANT_ID.strip()
    if not merchant_id:
        raise ValueError("SQUAD_MERCHANT_ID must be configured to build a transfer reference")

    return f"{merchant_id}_{job_id.hex[:8]}_{ULID()}"


def parse_transfer_ref(ref: str) -> TransferRefParts:
    """Parse a transfer reference into its constituent parts."""
    # rsplit guards against merchant IDs that contain underscores;
    # the last two segments are always fixed-format.
    parts = ref.rsplit("_", 2)
    if len(parts) != 3 or not all(parts):
        raise ValueError("Invalid Squad transfer reference")

    merchant_id, job_short, ulid_value = parts
    if len(job_short) != 8:
        raise ValueError("Invalid job identifier in Squad transfer reference")

    try:
        ULID.from_str(ulid_value)
    except ValueError as exc:
        raise ValueError("Invalid ULID in Squad transfer reference") from exc

    return {
        "merchant_id": merchant_id,
        "job_short": job_short,
        "ulid": ulid_value,
    }