"""Gantt chart mermaid generation helpers."""

from datetime import date, timedelta


def generate_gantt(
    title: str,
    phases: list[dict],
    date_format: str = "YYYY-MM-DD",
) -> str:
    """Generate a mermaid gantt chart from structured phase data.

    Args:
        title: Chart title
        phases: List of dicts with keys:
            - name: Phase name
            - tasks: List of dicts with keys:
                - name: Task name
                - start: Start date (YYYY-MM-DD string or date object)
                - duration: Duration in days (int) or end date string
                - status: Optional - "done", "active", "crit" or None
                - milestone: Optional bool - if True, renders as milestone
        date_format: Mermaid date format string
    """
    lines = [
        "```mermaid",
        "gantt",
        f"    title {title}",
        f"    dateFormat {date_format}",
    ]

    for phase in phases:
        lines.append(f"    section {phase['name']}")
        for task in phase.get("tasks", []):
            parts = []
            parts.append(f"    {task['name']}")
            parts.append(":")

            modifiers = []
            if task.get("milestone"):
                modifiers.append("milestone")
            if task.get("status"):
                modifiers.append(task["status"])

            if modifiers:
                parts.append(f" {', '.join(modifiers)},")

            start = task.get("start", "")
            if isinstance(start, date):
                start = start.isoformat()

            duration = task.get("duration", "")
            if isinstance(duration, int):
                duration = f"{duration}d"

            parts.append(f" {start}, {duration}")
            lines.append("".join(parts))

    lines.append("```")
    return "\n".join(lines)


def generate_high_level_gantt(
    title: str,
    start_date: str | date,
    phases: list[tuple[str, int]],
) -> str:
    """Generate a simple high-level gantt with sequential phases.

    Args:
        title: Chart title
        start_date: Project start date
        phases: List of (phase_name, duration_days) tuples
    """
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)

    structured_phases = []
    current_date = start_date

    for phase_name, duration_days in phases:
        structured_phases.append({
            "name": phase_name,
            "tasks": [{
                "name": phase_name,
                "start": current_date,
                "duration": duration_days,
            }],
        })
        current_date += timedelta(days=duration_days)

    return generate_gantt(title, structured_phases)


if __name__ == "__main__":
    # Example usage
    chart = generate_high_level_gantt(
        title="Project Timeline",
        start_date="2026-03-01",
        phases=[
            ("Discovery & Planning", 14),
            ("Design", 21),
            ("Implementation", 42),
            ("Testing & QA", 14),
            ("Deployment & Launch", 7),
        ],
    )
    print(chart)
