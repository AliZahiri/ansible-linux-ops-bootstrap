from __future__ import annotations


def audit_log_storage_violations(config: dict[str, object], *, minimum_space_left_mib: int = 1024, minimum_num_logs: int = 5) -> tuple[str, ...]:
    if not isinstance(minimum_space_left_mib, int) or isinstance(minimum_space_left_mib, bool) or minimum_space_left_mib < 1:
        raise ValueError("minimum_space_left_mib must be positive")
    if not isinstance(minimum_num_logs, int) or isinstance(minimum_num_logs, bool) or minimum_num_logs < 2:
        raise ValueError("minimum_num_logs must be at least two")
    if not isinstance(config, dict):
        return ("audit_log_storage_config_must_be_an_object",)

    violations: list[str] = []
    space_left = config.get("space_left_mib")
    if not isinstance(space_left, int) or isinstance(space_left, bool) or space_left < minimum_space_left_mib:
        violations.append("audit_space_left_threshold_is_below_minimum")
    if config.get("space_left_action") not in {"email", "exec", "single"}:
        violations.append("audit_space_left_action_must_alert_or_contain")
    if config.get("admin_space_left_action") not in {"single", "halt"}:
        violations.append("audit_admin_space_left_action_must_contain")
    if config.get("disk_full_action") not in {"single", "halt"}:
        violations.append("audit_disk_full_action_must_contain")
    if config.get("disk_error_action") not in {"single", "halt"}:
        violations.append("audit_disk_error_action_must_contain")
    if config.get("max_log_file_action") != "rotate":
        violations.append("audit_logs_must_rotate")
    num_logs = config.get("num_logs")
    if not isinstance(num_logs, int) or isinstance(num_logs, bool) or num_logs < minimum_num_logs:
        violations.append("audit_retained_log_count_is_below_minimum")
    return tuple(violations)


def audit_log_storage_is_resilient(config: dict[str, object], **policy: object) -> bool:
    return not audit_log_storage_violations(config, **policy)
