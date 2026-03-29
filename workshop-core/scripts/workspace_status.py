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


def workspace_dir(root: Path, name: str) -> Path:
    return changes_dir(root) / name


def status_path(root: Path, name: str) -> Path:
    return workspace_dir(root, name) / "status.json"


def load_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_status(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

    link_plan = sub.add_parser("link-plan")
    link_plan.add_argument("project")
    link_plan.add_argument("plan")
    link_plan.add_argument("--plan-level", choices=["semester", "month", "week"], required=True)
    link_plan.set_defaults(func=cmd_link_plan)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
