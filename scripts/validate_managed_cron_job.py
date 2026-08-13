from __future__ import annotations


def managed_cron_job_violations(jobs: list[dict[str, object]]) -> tuple[str, ...]:
    if not jobs:
        return ("at_least_one_cron_job_is_required",)
    violations: list[str] = []
    seen_names: set[str] = set()
    for index, job in enumerate(jobs):
        name = job.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"job_{index}:name_is_required")
        elif name in seen_names:
            violations.append(f"job_{index}:name_must_be_unique")
        seen_names.add(name)
        schedule = job.get("schedule")
        if not isinstance(schedule, str) or len(schedule.split()) != 5 or schedule.strip() == "* * * * *":
            violations.append(f"job_{index}:schedule_must_be_bounded_five_field_cron")
        owner = job.get("owner")
        if not isinstance(owner, str) or not owner.strip() or owner == "root":
            violations.append(f"job_{index}:owner_must_be_explicit_non_root")
        log_path = job.get("log_path")
        if not isinstance(log_path, str) or not log_path.startswith("/var/log/") or ".." in log_path.split("/"):
            violations.append(f"job_{index}:log_path_must_be_under_var_log")
    return tuple(violations)


def managed_cron_job_is_safe(jobs: list[dict[str, object]]) -> bool:
    return not managed_cron_job_violations(jobs)
