#!/usr/bin/env python3
"""Runtime setup helper for course-workshop-plugins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "schema": "course-workshop",
    "defaults": {
        "methodology": "pbl-huamei",
        "target_collection": "courses",
        "governance": {
            "approval_required": True,
            "approver_role": "curriculum-director",
        },
    },
    "models": {
        "planning": "gpt-5",
        "review": "gpt-5",
        "resource_check": "gpt-5-mini",
    },
    "publishing": {
        "default_target": {
            "kind": "local",
            "path": "courses",
        }
    },
    "runtime": {
        "projects_dir": ".workshop/projects",
        "plans_dir": ".workshop/plans",
        "kb_dir": ".workshop/kb",
        "archive_dir": ".workshop/archive",
    },
    "experts": {
        "custom_dir": ".workshop/agents/custom",
        "shared_dir": "experts",
    },
    "remote": {
        "cos": {
            "enabled": False,
            "bucket": "",
            "base_path": "",
        }
    },
    "lifecycle": {
        "phases": ["planning", "designing", "reviewing", "approved", "shipped"],
        "initial_phase": "planning",
    },
}


def runtime_dir(root: Path) -> Path:
    return root / ".workshop"


def config_path(root: Path) -> Path:
    return runtime_dir(root) / "config.yaml"


def find_root(explicit: str | None, create: bool = False) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if create or runtime_dir(root).is_dir():
            return root
        raise SystemExit(f".workshop/ not found under: {root}")
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if runtime_dir(candidate).is_dir():
            return candidate
    if create:
        return current
    raise SystemExit("Could not find project root containing .workshop/")


def parse_scalar(value: str) -> Any:
    if value == '""' or value == "''":
        return ""
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def dump_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None or value == "":
        return '""'
    return str(value)


def parse_yaml_subset(text: str) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))

    def parse_node(index: int, indent: int) -> tuple[Any, int]:
        if lines[index][1].startswith("- "):
            return parse_list(index, indent)
        return parse_dict(index, indent)

    def parse_dict(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent:
                break
            if line_indent != indent or content.startswith("- "):
                break
            key, _, rest = content.partition(":")
            if not _:
                raise SystemExit(f"Unsupported config line: {content}")
            rest = rest.strip()
            index += 1
            if rest:
                result[key] = parse_scalar(rest)
            elif index < len(lines) and lines[index][0] > indent:
                child, index = parse_node(index, lines[index][0])
                result[key] = child
            else:
                result[key] = {}
        return result, index

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent or line_indent != indent or not content.startswith("- "):
                break
            item = content[2:].strip()
            index += 1
            if item:
                result.append(parse_scalar(item))
            elif index < len(lines) and lines[index][0] > indent:
                child, index = parse_node(index, lines[index][0])
                result.append(child)
            else:
                result.append({})
        return result, index

    if not lines:
        return {}
    data, _ = parse_node(0, lines[0][0])
    return data


def dump_yaml_subset(data: Any, indent: int = 0) -> list[str]:
    lines: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{' ' * indent}{key}:")
                lines.extend(dump_yaml_subset(value, indent + 2))
            else:
                lines.append(f"{' ' * indent}{key}: {dump_scalar(value)}")
    elif isinstance(data, list):
        for value in data:
            if isinstance(value, (dict, list)):
                lines.append(f"{' ' * indent}-")
                lines.extend(dump_yaml_subset(value, indent + 2))
            else:
                lines.append(f"{' ' * indent}- {dump_scalar(value)}")
    return lines


def load_config(root: Path) -> dict[str, Any]:
    path = config_path(root)
    if not path.exists():
        raise SystemExit("Missing .workshop/config.yaml. Run /workshop-core:init first.")
    return parse_yaml_subset(path.read_text(encoding="utf-8"))


def write_config(root: Path, data: dict[str, Any]) -> None:
    path = config_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(dump_yaml_subset(data)) + "\n", encoding="utf-8")


def deep_get(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def deep_set(data: dict[str, Any], dotted_key: str, value: Any) -> Any:
    parts = dotted_key.split(".")
    current: dict[str, Any] = data
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            current[part] = next_value
        current = next_value
    old = current.get(parts[-1])
    current[parts[-1]] = value
    return old


def init_runtime(root: Path) -> dict[str, Any]:
    rt = runtime_dir(root)
    dirs = [
        rt / "projects",
        rt / "plans",
        rt / "agents" / "custom",
        rt / "kb" / "textbooks",
        rt / "kb" / "philosophy",
        rt / "kb" / "lesson-plans",
        rt / "kb" / "research-records",
        rt / "kb" / "calendars",
        rt / "archive",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        keep = directory / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    if not config_path(root).exists():
        write_config(root, DEFAULT_CONFIG)
    return {
        "runtime_root": str(rt.relative_to(root)),
        "config": str(config_path(root).relative_to(root)),
        "default_methodology": DEFAULT_CONFIG["defaults"]["methodology"],
    }


def kb_counts(root: Path) -> dict[str, int]:
    categories = ["textbooks", "philosophy", "lesson-plans", "research-records", "calendars"]
    counts: dict[str, int] = {}
    for category in categories:
        category_dir = runtime_dir(root) / "kb" / category
        counts[category] = len([p for p in category_dir.glob("*.md") if p.name != ".gitkeep"]) if category_dir.exists() else 0
    return counts


def onboarding_summary(
    root: Path,
    role: str | None,
    starting_mode: str | None,
    methodology: str | None,
    import_materials: str | None,
    publishing: str | None,
) -> dict[str, Any]:
    config = load_config(root)
    kb = kb_counts(root)
    plans = len([p for p in (runtime_dir(root) / "plans").iterdir() if p.is_dir() and p.name != ".gitkeep"]) if (runtime_dir(root) / "plans").exists() else 0
    projects = len([p for p in (runtime_dir(root) / "projects").iterdir() if p.is_dir() and p.name != ".gitkeep"]) if (runtime_dir(root) / "projects").exists() else 0
    kb_total = sum(kb.values())
    current_methodology = methodology or deep_get(config, "defaults.methodology")
    current_publishing = publishing or deep_get(config, "publishing.default_target.kind") or "local"
    next_steps: list[str] = []
    template_step = (
        f"/workshop-templates:template-select {current_methodology}"
        if current_methodology and current_methodology != "mixed"
        else "/workshop-templates:template-select <id>"
    )

    if current_methodology in {None, "", "mixed"}:
        next_steps.append("/workshop-core:config set defaults.methodology pbl-huamei")
    if kb_total == 0 and import_materials in {None, "now", "yes"}:
        next_steps.append("/workshop-kb:kb-import <path>")
    if (starting_mode or "planning-first") == "planning-first":
        next_steps.append("/workshop-planner:semester-plan <semester>")
        next_steps.append(template_step)
        first_hil = "project-framing after the first project is created and linked to a plan"
    elif starting_mode == "project-first":
        next_steps.append(template_step)
        first_hil = "project-framing right after template selection and basic project setup"
    else:
        next_steps.append(template_step)
        next_steps.append("/workshop-planner:semester-plan <semester>")
        first_hil = "project-framing once the pilot project scope is set"

    return {
        "role": role or "mixed team",
        "starting_mode": starting_mode or "planning-first",
        "default_methodology": current_methodology,
        "kb_status": "empty" if kb_total == 0 else "populated",
        "kb_counts": kb,
        "publishing": current_publishing,
        "existing_plans": plans,
        "existing_projects": projects,
        "first_hil": first_hil,
        "recommended_next_steps": next_steps,
    }


def render_onboarding(summary: dict[str, Any]) -> str:
    lines = [
        "Onboarding summary",
        "",
        f"- Role: {summary['role']}",
        f"- Starting mode: {summary['starting_mode']}",
        f"- Default methodology: {summary['default_methodology']}",
        f"- KB status: {summary['kb_status']}",
        f"- Existing plans: {summary['existing_plans']}",
        f"- Existing projects: {summary['existing_projects']}",
        f"- Publishing: {summary['publishing']}",
        f"- First HIL: {summary['first_hil']}",
        "",
        "Recommended next steps:",
    ]
    for index, step in enumerate(summary["recommended_next_steps"], start=1):
        lines.append(f"{index}. {step}")
    return "\n".join(lines)


def cmd_init_runtime(args: argparse.Namespace) -> None:
    root = find_root(args.root, create=True)
    print(json.dumps(init_runtime(root), ensure_ascii=False, indent=2))


def cmd_config_show(args: argparse.Namespace) -> None:
    root = find_root(args.root)
    config = load_config(root)
    if args.json:
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return
    print("\n".join(dump_yaml_subset(config)))


def cmd_config_set(args: argparse.Namespace) -> None:
    root = find_root(args.root)
    config = load_config(root)
    old = deep_set(config, args.key, parse_scalar(args.value))
    write_config(root, config)
    print(
        json.dumps(
            {
                "key": args.key,
                "old": old,
                "new": deep_get(config, args.key),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_onboarding_summary(args: argparse.Namespace) -> None:
    root = find_root(args.root)
    summary = onboarding_summary(
        root,
        args.role,
        args.starting_mode,
        args.methodology,
        args.import_materials,
        args.publishing,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    print(render_onboarding(summary))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Runtime setup helper")
    parser.add_argument("--root", default=None, help="Project root containing .workshop/")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init-runtime")
    init_cmd.set_defaults(func=cmd_init_runtime)

    config_show_cmd = sub.add_parser("config-show")
    config_show_cmd.add_argument("--json", action="store_true")
    config_show_cmd.set_defaults(func=cmd_config_show)

    config_set_cmd = sub.add_parser("config-set")
    config_set_cmd.add_argument("key")
    config_set_cmd.add_argument("value")
    config_set_cmd.set_defaults(func=cmd_config_set)

    onboarding_cmd = sub.add_parser("onboarding-summary")
    onboarding_cmd.add_argument("--role", choices=["curriculum-director", "classroom-teacher", "mixed-team"], default=None)
    onboarding_cmd.add_argument("--starting-mode", choices=["planning-first", "project-first", "mixed"], default=None)
    onboarding_cmd.add_argument("--methodology", choices=["pbl-huamei", "five-step", "mixed"], default=None)
    onboarding_cmd.add_argument("--import-materials", choices=["now", "later", "yes", "no"], default=None)
    onboarding_cmd.add_argument("--publishing", choices=["local", "cos"], default=None)
    onboarding_cmd.add_argument("--json", action="store_true")
    onboarding_cmd.set_defaults(func=cmd_onboarding_summary)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
