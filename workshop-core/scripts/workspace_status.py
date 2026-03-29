#!/usr/bin/env python3
"""Workspace status helper for course-workshop-plugins.

This script provides a minimal executable layer for managing
`studio/changes/*/status.json` files.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def find_studio_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not (root / "studio").is_dir():
            raise SystemExit(f"studio/ not found under: {root}")
        return root

    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "studio").is_dir():
            return candidate
    raise SystemExit("Could not find project root containing studio/")


def changes_dir(root: Path) -> Path:
    return root / "studio" / "changes"


def archive_dir(root: Path) -> Path:
    return root / "studio" / "archive"


def kb_dir(root: Path) -> Path:
    return root / "studio" / "kb"


def workspace_dir(root: Path, name: str) -> Path:
    return changes_dir(root) / name


def status_path(root: Path, name: str) -> Path:
    return workspace_dir(root, name) / "status.json"


def load_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_default_methodology(root: Path) -> str | None:
    config = root / "studio" / "config.yaml"
    if not config.exists():
        return None
    for line in config.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("methodology:"):
            return stripped.split(":", 1)[1].strip()
    return None


def write_status(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deliverables_for_workspace(root: Path, name: str) -> dict[str, bool]:
    ws = workspace_dir(root, name)
    return {
        "proposal": (ws / "proposal.md").exists(),
        "lesson": (ws / "lesson-plan.md").exists(),
        "quality_report": (ws / "quality-report.md").exists(),
        "review_comments": (ws / "review-comments.md").exists(),
        "resource_plan": (ws / "resource-plan.md").exists(),
        "resource_check_report": (ws / "resource-check-report.md").exists(),
    }


def required_skills_for(deliverables: dict[str, bool]) -> list[str]:
    required: list[str] = []
    if deliverables["proposal"]:
        required.extend(
            [
                "driving-question",
                "network-map",
                "inquiry-scaffold",
                "activity-design",
                "proposal-generate",
            ]
        )
    if deliverables["lesson"]:
        required.extend(
            [
                "lesson-objective",
                "lesson-scaffold",
                "lesson-detail",
                "lesson-generate",
            ]
        )
    return required


def completion_summary(skills: dict[str, Any]) -> tuple[int, int]:
    total = len(skills)
    done = sum(1 for value in skills.values() if value in {"done", "approved"})
    return done, total


def classify_workspace(root: Path, name: str, data: dict[str, Any]) -> str:
    ws = workspace_dir(root, name)
    status_type = data.get("type")
    if status_type == "planning":
        return "planning"
    if status_type == "project":
        return "project"
    if status_type in {"plugin", "domain"}:
        if data.get("target_dir") or data.get("action") or (ws / "plugin.json.draft").exists():
            return "planning"
    if (ws / "semester-plan.md").exists() or (ws / "month-plan.md").exists() or any(ws.glob("week*-plan.md")):
        return "planning"
    if (ws / "brief.md").exists() or (ws / "skill-map.md").exists() or (ws / "plugin.json.draft").exists():
        return "planning"
    return "project"


def summarize_workspace(root: Path, name: str) -> dict[str, Any]:
    ws = workspace_dir(root, name)
    data = load_status(status_path(root, name))
    kind = classify_workspace(root, name, data)
    config_path = ws / "config.yaml"
    methodology = None
    if config_path.exists():
        for line in config_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("methodology:"):
                methodology = stripped.split(":", 1)[1].strip()
                break

    if kind == "planning":
        planning_files = []
        for candidate in ["semester-plan.md", "month-plan.md"]:
            if (ws / candidate).exists():
                planning_files.append(candidate)
        planning_files.extend(sorted(path.name for path in ws.glob("week*-plan.md")))
        return {
            "name": name,
            "type": "planning",
            "phase": data.get("phase", "unknown"),
            "plan_level": data.get("plan_level"),
            "linked_projects": data.get("linked_projects", []),
            "files": planning_files,
        }

    deliverables = deliverables_for_workspace(root, name)
    skills = data.get("skills", {})
    done, total = completion_summary(skills)
    deliverable_list = [key for key, exists in deliverables.items() if exists and key in {"proposal", "lesson"}]
    return {
        "name": name,
        "type": "project",
        "phase": data.get("phase", "unknown"),
        "methodology": methodology,
        "plan_refs": data.get("plan_refs", {"semester": None, "month": None, "week": None}),
        "deliverables": deliverable_list,
        "skills_done": done,
        "skills_total": total,
    }


def summarize_archives(root: Path) -> list[dict[str, Any]]:
    archive = archive_dir(root)
    if not archive.exists():
        return []
    entries = sorted(
        [path for path in archive.iterdir() if path.is_dir()],
        key=lambda p: p.name,
        reverse=True,
    )[:5]
    result = []
    for entry in entries:
        data = load_status(entry / "status.json")
        result.append({"name": entry.name, "shipped_to": data.get("shipped_to")})
    return result


def summarize_kb(root: Path) -> dict[str, int]:
    kb = kb_dir(root)
    categories = ["textbooks", "philosophy", "lesson-plans", "research-records", "calendars"]
    counts: dict[str, int] = {}
    for category in categories:
        category_dir = kb / category
        if not category_dir.exists():
            counts[category] = 0
            continue
        counts[category] = len([p for p in category_dir.glob("*.md") if p.name != ".gitkeep"])
    return counts


def summarize_status(root: Path) -> dict[str, Any]:
    changes = changes_dir(root)
    projects = []
    planning = []
    if changes.exists():
        for entry in sorted(changes.iterdir()):
            if entry.name == ".gitkeep" or not entry.is_dir():
                continue
            summary = summarize_workspace(root, entry.name)
            if summary["type"] == "project":
                projects.append(summary)
            else:
                planning.append(summary)
    return {
        "default_methodology": read_default_methodology(root),
        "knowledge_base": summarize_kb(root),
        "planning": planning,
        "projects": projects,
        "archives": summarize_archives(root),
    }


def validate_project(root: Path, name: str, required_phase: str | None) -> dict[str, Any]:
    ws_path = workspace_dir(root, name)
    data = load_status(status_path(root, name))
    if not data:
        raise SystemExit(f"Missing status.json for workspace: {name}")
    if data.get("type") == "planning":
        raise SystemExit(f"Workspace '{name}' is planning, not a shippable project.")

    deliverables = deliverables_for_workspace(root, name)
    if not deliverables["proposal"] and not deliverables["lesson"]:
        raise SystemExit(
            f"Workspace '{name}' has no final deliverable. Expected proposal.md or lesson-plan.md."
        )

    if required_phase and data.get("phase") != required_phase:
        raise SystemExit(
            f"Workspace '{name}' is in phase '{data.get('phase')}', expected '{required_phase}'."
        )

    skills = data.get("skills", {})
    required_skills = required_skills_for(deliverables)
    missing_skills = [skill for skill in required_skills if skills.get(skill) not in {"done", "approved"}]

    return {
        "workspace": name,
        "type": data.get("type", "legacy"),
        "phase": data.get("phase"),
        "deliverables": deliverables,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "optional_reviews": {
            "quality_report": deliverables["quality_report"],
            "review_comments": deliverables["review_comments"],
            "resource_plan": deliverables["resource_plan"],
            "resource_check_report": deliverables["resource_check_report"],
        },
        "ready": len(missing_skills) == 0,
    }


def ensure_project_status(root: Path, name: str, theme: str | None) -> dict[str, Any]:
    path = status_path(root, name)
    data = load_status(path)
    data.setdefault("type", "project")
    data.setdefault("project", name)
    data.setdefault("theme", theme or name)
    data.setdefault("target_collection", "courses")
    data.setdefault("phase", "planning")
    data.setdefault("created_at", iso_now())
    data.setdefault("plan_refs", {"semester": None, "month": None, "week": None})
    data.setdefault("skills", {})
    write_status(path, data)
    return data


def ensure_planning_status(root: Path, name: str, plan_level: str) -> dict[str, Any]:
    path = status_path(root, name)
    data = load_status(path)
    data.setdefault("type", "planning")
    data.setdefault("plan_level", plan_level)
    data.setdefault("plan_name", name)
    data.setdefault("phase", "planning")
    data.setdefault("created_at", iso_now())
    data.setdefault("linked_projects", [])
    write_status(path, data)
    return data


def cmd_ensure_project(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    data = ensure_project_status(root, args.workspace, args.theme)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_ensure_planning(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    data = ensure_planning_status(root, args.workspace, args.plan_level)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_set_skill(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    path = status_path(root, args.workspace)
    data = load_status(path)
    if not data:
        raise SystemExit(f"Missing status.json for workspace: {args.workspace}")
    data.setdefault("skills", {})
    data["skills"][args.skill] = args.value
    write_status(path, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_set_phase(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    path = status_path(root, args.workspace)
    data = load_status(path)
    if not data:
        raise SystemExit(f"Missing status.json for workspace: {args.workspace}")
    data["phase"] = args.phase
    if args.phase == "approved":
        data["approved_at"] = iso_now()
        if args.approved_by:
            data["approved_by"] = args.approved_by
    write_status(path, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_complete_project_skill(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    data = ensure_project_status(root, args.workspace, args.theme)
    data.setdefault("skills", {})
    data["skills"][args.skill] = args.value
    if args.phase:
        data["phase"] = args.phase
        if args.phase == "approved":
            data["approved_at"] = iso_now()
            if args.approved_by:
                data["approved_by"] = args.approved_by
    write_status(status_path(root, args.workspace), data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_complete_planning(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    data = ensure_planning_status(root, args.workspace, args.plan_level)
    if args.linked_project:
        linked = data.setdefault("linked_projects", [])
        if args.linked_project not in linked:
            linked.append(args.linked_project)
    write_status(status_path(root, args.workspace), data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_link_plan(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    project = ensure_project_status(root, args.project, None)
    planning = ensure_planning_status(root, args.plan, args.plan_level)

    plan_refs = project.setdefault("plan_refs", {"semester": None, "month": None, "week": None})
    plan_refs[args.plan_level] = args.plan

    linked = planning.setdefault("linked_projects", [])
    if args.project not in linked:
        linked.append(args.project)

    write_status(status_path(root, args.project), project)
    write_status(status_path(root, args.plan), planning)

    print(
        json.dumps(
            {
                "project": project["project"],
                "plan_level": args.plan_level,
                "plan": args.plan,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_validate_project(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    result = validate_project(root, args.workspace, args.required_phase)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ready"]:
        raise SystemExit(2)


def cmd_summarize_status(args: argparse.Namespace) -> None:
    root = find_studio_root(args.root)
    result = summarize_status(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Workspace status helper")
    parser.add_argument("--root", help="Project root containing studio/", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    ensure_project = sub.add_parser("ensure-project")
    ensure_project.add_argument("workspace")
    ensure_project.add_argument("--theme", default=None)
    ensure_project.set_defaults(func=cmd_ensure_project)

    ensure_planning = sub.add_parser("ensure-planning")
    ensure_planning.add_argument("workspace")
    ensure_planning.add_argument("--plan-level", choices=["semester", "month", "week"], required=True)
    ensure_planning.set_defaults(func=cmd_ensure_planning)

    set_skill = sub.add_parser("set-skill")
    set_skill.add_argument("workspace")
    set_skill.add_argument("skill")
    set_skill.add_argument("--value", default="done")
    set_skill.set_defaults(func=cmd_set_skill)

    set_phase = sub.add_parser("set-phase")
    set_phase.add_argument("workspace")
    set_phase.add_argument("phase", choices=["planning", "designing", "reviewing", "approved", "shipped"])
    set_phase.add_argument("--approved-by", default=None)
    set_phase.set_defaults(func=cmd_set_phase)

    complete_project_skill = sub.add_parser("complete-project-skill")
    complete_project_skill.add_argument("workspace")
    complete_project_skill.add_argument("skill")
    complete_project_skill.add_argument("--theme", default=None)
    complete_project_skill.add_argument("--value", default="done")
    complete_project_skill.add_argument(
        "--phase",
        choices=["planning", "designing", "reviewing", "approved", "shipped"],
        default=None,
    )
    complete_project_skill.add_argument("--approved-by", default=None)
    complete_project_skill.set_defaults(func=cmd_complete_project_skill)

    complete_planning = sub.add_parser("complete-planning")
    complete_planning.add_argument("workspace")
    complete_planning.add_argument("--plan-level", choices=["semester", "month", "week"], required=True)
    complete_planning.add_argument("--linked-project", default=None)
    complete_planning.set_defaults(func=cmd_complete_planning)

    link_plan = sub.add_parser("link-plan")
    link_plan.add_argument("project")
    link_plan.add_argument("plan")
    link_plan.add_argument("--plan-level", choices=["semester", "month", "week"], required=True)
    link_plan.set_defaults(func=cmd_link_plan)

    validate_project_cmd = sub.add_parser("validate-project")
    validate_project_cmd.add_argument("workspace")
    validate_project_cmd.add_argument(
        "--required-phase",
        choices=["planning", "designing", "reviewing", "approved", "shipped"],
        default=None,
    )
    validate_project_cmd.set_defaults(func=cmd_validate_project)

    summarize_status_cmd = sub.add_parser("summarize-status")
    summarize_status_cmd.set_defaults(func=cmd_summarize_status)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
