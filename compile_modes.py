#!/usr/bin/env python3
"""Generate Roo custom mode assets.

This script merges the capabilities of `compile_modes.py` and
`convert_modes_to_windsurf_rules.py`.

It performs two tasks:
1. Compile all **custom** modes (excluding core built-ins) into consolidated
   `custom_modes.json` and `custom_modes.yaml` files that bundle metadata,
   role definitions and custom instructions (with shared instructions
   automatically appended).
2. Convert each custom mode into an individual Windsurf rule Markdown file
   plus an `_index.md` catalogue and a `workflow.md` Mermaid diagram.

Both tasks run in a single invocation so callers only need to execute **one
command** instead of two.

Example
-------
```bash
python generate_modes_assets.py \
  --modes-dir ./modes \
  --json-out ./custom_modes.json \
  --yaml-out ./custom_modes.yaml \
  --rules-out-dir ./.windsurf/rules/roo-modes
```
"""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import List, Dict

import yaml  # PyYAML is required

# Built-in modes that should **not** be treated as custom modes.
BUILTIN_MODES = {"architect", "code", "ask", "debug"}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    """Return UTF-8 text from *path* or empty string if the file is missing."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def first_sentence(text: str) -> str:
    """Extract a short description (first sentence/line) from *text*."""
    for sep in (". ", "\n"):
        if sep in text:
            return text.split(sep, 1)[0].strip()
    return text.strip()

# ---------------------------------------------------------------------------
# "Compile" stage – produce JSON / YAML aggregate files
# ---------------------------------------------------------------------------

def compile_modes(
    modes_dir: Path,
    yaml_out: Path,
    user: str | None = None,
) -> None:
    """Aggregate custom modes into *yaml_out*."""

    if not modes_dir.is_dir():
        raise FileNotFoundError(f"Modes directory not found: {modes_dir}")

    shared_instructions = read_file(modes_dir / "sharedinstructions.md")
    all_modes: List[dict] = []

    for mode_path in modes_dir.iterdir():
        if not mode_path.is_dir():
            continue
        if mode_path.name in BUILTIN_MODES:
            continue  # Skip built-ins shipped with Roo

        metadata_path = mode_path / "metadata.json"
        roledef_path = mode_path / "roledefinition.md"
        instructions_path = mode_path / "custominstructions.md"

        if not (metadata_path.exists() and roledef_path.exists() and instructions_path.exists()):
            print(f"[WARN] Incomplete mode skipped: {mode_path.name}")
            continue

        try:
            mode_meta = json.loads(read_file(metadata_path))
            role_definition = read_file(roledef_path)
            custom_instructions = read_file(instructions_path)

            mode_meta["roleDefinition"] = role_definition
            mode_meta["customInstructions"] = f"{custom_instructions}\n{shared_instructions}"

            all_modes.append(mode_meta)
        except Exception as exc:  # pragma: no cover – defensive
            print(f"[ERR] Failed processing {mode_path.name}: {exc}")

    output_data = {"customModes": all_modes}

    # Ensure parent dirs exist then write outputs
    yaml_out.parent.mkdir(parents=True, exist_ok=True)

    yaml_out.write_text(yaml.dump(output_data, indent=2, allow_unicode=True), encoding="utf-8")

    print(f"[OK] Wrote Roo modes to {yaml_out.relative_to(Path.cwd())}")

    # Optionally sync to IDE settings directories (for local development)
    if user:
        ide_targets = {"Code": "yaml", "Windsurf": "yaml"}
        base_tpl = (
            "/Users/{user}/Library/Application Support/{product}/User/globalStorage/"
            "rooveterinaryinc.roo-cline/settings/custom_modes.{ext}"
        )
        for product, ext in ide_targets.items():
            dest = Path(base_tpl.format(user=user, product=product, ext=ext))
            dest.parent.mkdir(parents=True, exist_ok=True)
            if ext == "yaml":
                dest.write_text(yaml.dump(output_data, indent=2, allow_unicode=True), encoding="utf-8")
            else:
                dest.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"[OK] Synced settings: {dest}")

# ---------------------------------------------------------------------------
# "Convert" stage – generate Windsurf rule Markdown files
# ---------------------------------------------------------------------------

def convert_modes_to_rules(modes_dir: Path, output_dir: Path) -> None:
    """Translate custom modes into individual Windsurf rule files."""

    if not modes_dir.is_dir():
        raise FileNotFoundError(f"Modes directory not found: {modes_dir}")

    shared_instructions = read_file(modes_dir / "sharedinstructions.md")
    output_dir.mkdir(parents=True, exist_ok=True)

    rule_summaries: List[Dict[str, str]] = []  # For the catalogue

    for mode_path in modes_dir.iterdir():
        if not mode_path.is_dir():
            continue
        if mode_path.name in BUILTIN_MODES:
            continue  # Skip core modes

        metadata_path = mode_path / "metadata.json"
        roledef_path = mode_path / "roledefinition.md"
        instructions_path = mode_path / "custominstructions.md"

        if not (metadata_path.exists() and roledef_path.exists() and instructions_path.exists()):
            print(f"[WARN] Incomplete mode skipped: {mode_path.name}")
            continue

        metadata = json.loads(read_file(metadata_path))
        slug = metadata.get("slug", mode_path.name)
        name = metadata.get("name", slug.replace("-", " ").title())

        role_definition = read_file(roledef_path)
        custom_instructions = read_file(instructions_path)

        rule_body = (
            f"""---
trigger: model_decision
description: {first_sentence(role_definition)}
---
# {name}

## Role Definition
{role_definition}

## Custom Instructions
{custom_instructions}
"""
        )

        rule_path = output_dir / f"{slug}.md"
        rule_path.write_text(rule_body, encoding="utf-8")
        print(f"[OK] Wrote rule: {rule_path.relative_to(Path.cwd())}")

        rule_summaries.append(
            {"slug": slug, "name": name, "description": first_sentence(role_definition)}
        )

    # ---------------------------------------------------------------------
    # _index.md (always_on)
    # ---------------------------------------------------------------------
    bullets = (
        "\n".join(
            f"* **{item['name']}** (`{item['slug']}.md`) — {item['description']}" for item in rule_summaries
        )
        if rule_summaries
        else "*(No rules generated)*"
    )

    index_body = (
        f"""---
trigger: always_on
description: Overview of Roo custom mode rules converted for Windsurf.
---
# Roo Custom Mode Rules — Overview

This file is **always on** and provides a catalogue of all converted Roo
custom modes. Each individual rule is loaded with `trigger: model_decision` and
will only activate when relevant to the current model decision context.

## Available Rules
{bullets}

## Shared Instructions (apply to all modes)
{shared_instructions}
"""
    )

    (output_dir / "_index.md").write_text(index_body, encoding="utf-8")
    print(f"[OK] Wrote index: {(output_dir / '_index.md').relative_to(Path.cwd())}")

    # ---------------------------------------------------------------------
    # workflow.md (Mermaid diagram)
    # ---------------------------------------------------------------------
    # Build adaptive workflow diagram from README details
    workflow_body = textwrap.dedent(
        """
        # Adaptive Mode Workflow

        The following Mermaid diagram summarizes the adaptive workflow outlined in `readme.md`.

        ```mermaid
        graph TD
            U[User] --> PM[Project Manager]
            PM -->|Delegates planning| A[Architect]
            A -->|Lite-Touch| PlanLite[plan.md]
            A -->|Heavy-Touch| PlanHeavy[plan.md & plan-X.md & plan-verify.md]
            A --> U
            PM -->|Review plan| Code[Code Agents]
            Code -->|Execute tasks| Work[Work Log]
            Code -->|Context threshold| Handoff[handoff-<timestamp>.md]
            Handoff --> PM
            PM -->|Launch new agent| NewAgent[Next Agent]
            PM --> Verify[Verification Agent]
            Verify --> U
        ```
        """
    ).lstrip()

    (output_dir / "workflow.md").write_text(workflow_body, encoding="utf-8")
    print(f"[OK] Wrote workflow: {(output_dir / 'workflow.md').relative_to(Path.cwd())}")

# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate compiled mode files and Windsurf rules from Roo custom modes."
    )
    parser.add_argument(
        "--modes-dir", default="./modes", help="Directory containing the Roo modes (default: %(default)s)"
    )
    parser.add_argument(
        "--roo-out", default="./custom_modes.yaml", help="Path for aggregated YAML output (default: %(default)s)"
    )
    parser.add_argument(
        "--windsurf-out",
        default="./.windsurf/rules/roo-modes",
        help="Directory to write Windsurf rule Markdown files (default: %(default)s)",
    )
    parser.add_argument(
        "--user",
        default=None,
        help="If set, also copy the compiled JSON/YAML into local IDE settings paths for the given macOS user.",
    )
    args = parser.parse_args()

    modes_dir = Path(args.modes_dir).expanduser().resolve()
    yaml_out = Path(args.roo_out).expanduser().resolve()
    rules_out_dir = Path(args.windsurf_out).expanduser().resolve()

    # Run both stages
    compile_modes(modes_dir, yaml_out, user=args.user)
    convert_modes_to_rules(modes_dir, rules_out_dir)


if __name__ == "__main__":
    main()
