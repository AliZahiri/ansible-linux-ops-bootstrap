from __future__ import annotations

from datetime import datetime
import re


_RELEASE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{2,127}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def kernel_reboot_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_deferral_seconds: int = 86400) -> tuple[str, ...]:
    if not isinstance(maximum_deferral_seconds, int) or isinstance(maximum_deferral_seconds, bool) or maximum_deferral_seconds <= 0:
        raise ValueError("maximum deferral must be a positive integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    violations: list[str] = []
    running = evidence.get("running_kernel")
    installed = evidence.get("installed_kernel")
    if not isinstance(running, str) or not _RELEASE.fullmatch(running):
        violations.append("running_kernel_release_is_invalid")
    if not isinstance(installed, str) or not _RELEASE.fullmatch(installed):
        violations.append("installed_kernel_release_is_invalid")
    if isinstance(running, str) and isinstance(installed, str) and _RELEASE.fullmatch(running) and _RELEASE.fullmatch(installed) and running != installed:
        if evidence.get("reboot_completed") is True:
            violations.append("running_kernel_does_not_match_installed_after_reboot")
        else:
            if not str(evidence.get("deferral_ticket", "")).strip():
                violations.append("kernel_reboot_requires_deferral_ticket")
            deadline = _timestamp(evidence.get("deferral_deadline"))
            if deadline is None:
                violations.append("deferral_deadline_must_be_timezone_aware")
            else:
                remaining = (deadline - now).total_seconds()
                if remaining <= 0:
                    violations.append("kernel_reboot_deferral_has_expired")
                elif remaining > maximum_deferral_seconds:
                    violations.append("kernel_reboot_deferral_exceeds_maximum")
    return tuple(violations)


def kernel_reboot_state_is_acceptable(evidence: dict[str, object], **policy: object) -> bool:
    return not kernel_reboot_evidence_violations(evidence, **policy)
