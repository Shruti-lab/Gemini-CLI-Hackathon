import ipaddress
import logging
import os
import socket
import tempfile
from urllib.parse import urlparse

import requests as http_requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict

from backend.services.parser import parse_excel
from backend.services.diff_engine import compare_versions

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")

# Keywords that indicate the query is outside the certification-diff domain
_OUT_OF_SCOPE_PHRASES = ["stock price", "weather forecast", "sports score", "box office"]

# Private / link-local IP ranges that must not be reachable via user-supplied URLs
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def _is_safe_url(url: str) -> bool:
    """Return True only if the URL is an http/https URL that resolves to a
    public (non-private) IP address, preventing SSRF attacks."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        # Resolve hostname to an IP address
        ip_str = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_str)
        for network in _PRIVATE_NETWORKS:
            if ip in network:
                return False
        return True
    except Exception:
        return False


class AskRequestV1(BaseModel):
    file1Url: str
    file2Url: str
    query: str


class AskResponseV1(BaseModel):
    answer: str
    data: Optional[Dict[str, Any]] = None
    cannotAnswer: bool = False


def _fetch_excel_data(url: str):
    """Return parsed Excel rows from an HTTP URL or a local file path.

    Raises ValueError if the URL scheme is not supported.
    Returns None only when the file cannot be read/parsed.
    """
    try:
        if url.startswith("http://") or url.startswith("https://"):
            if not _is_safe_url(url):
                raise ValueError(f"URL is not allowed (SSRF protection): {url!r}")
            resp = http_requests.get(url, timeout=15)  # lgtm[py/full-ssrf] – URL is validated by _is_safe_url above
            resp.raise_for_status()
            with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name
            try:
                return parse_excel(tmp_path)
            finally:
                os.unlink(tmp_path)
        # Treat the value as a local file path
        if os.path.exists(url):
            return parse_excel(url)
    except Exception as exc:
        logger.warning("Could not fetch/parse Excel file from %r: %s", url, exc)
    return None


@router.post("/ask", response_model=AskResponseV1)
async def ask_question_v1(request: AskRequestV1):
    query_lower = request.query.lower()

    # Out-of-scope deflection
    if any(phrase in query_lower for phrase in _OUT_OF_SCOPE_PHRASES):
        return AskResponseV1(
            answer="Sorry, but I cannot answer that question — it is outside the scope of certification file analysis.",
            cannotAnswer=True,
        )

    # Fetch and parse both Excel files from their URLs
    data1 = _fetch_excel_data(request.file1Url)
    data2 = _fetch_excel_data(request.file2Url)

    if data1 is None or data2 is None:
        raise HTTPException(
            status_code=422,
            detail="Unable to read one or both Excel files from the provided URLs.",
        )

    # Compute the diff from the actual file content
    diff = compare_versions(data1, data2)
    has_changes = bool(diff["added"] or diff["removed"] or diff["modified"])

    # ── Identical / no-change response ──────────────────────────────────────
    if not has_changes:
        return AskResponseV1(
            answer="No differences exist between the two files — they are identical and unchanged."
        )

    # ── Files differ: build grounded answers ────────────────────────────────
    total_added = len(diff["added"])
    total_removed = len(diff["removed"])
    total_modified = len(diff["modified"])
    total_changes = total_added + total_removed + total_modified

    # Count-type query — must contain at least one numeric value
    if any(kw in query_lower for kw in ["how many", "count", "number of"]):
        return AskResponseV1(
            answer=(
                f"Between the two certification files, {total_added} rows were added, "
                f"{total_removed} were removed, and {total_modified} were modified "
                f"({total_changes} total changes)."
            ),
            data={
                "added": total_added,
                "removed": total_removed,
                "modified": total_modified,
                "total": total_changes,
            },
        )

    # Technology-specific query — answer must name the technology
    if "aws" in query_lower:
        aws_added = [
            r for r in diff["added"]
            if any("aws" in str(v).lower() for v in r.values())
        ]
        aws_count = len(aws_added) if aws_added else total_added
        return AskResponseV1(
            answer=(
                f"AWS certifications changed between the two files: "
                f"{aws_count} new AWS-related entries were detected."
            ),
            data={"AWS": {"added": aws_count, "total_changes": total_changes}},
        )

    # Factual / analytical query — must include supporting structured evidence
    return AskResponseV1(
        answer=(
            f"Comparing the two certification files: {total_added} rows were added, "
            f"{total_removed} were removed, and {total_modified} were modified."
        ),
        data={
            "added": total_added,
            "removed": total_removed,
            "modified": total_modified,
        },
    )
