# Roo Prompts Mode Workflow (Adaptive)

This document outlines the intended workflow based on the custom mode definitions found in the `/modes` directory, incorporating an adaptive approach to manage complexity and context size.

While you can compile your own modes, you can also use the pre-compiled modes:
1. For Roo in ./custom_modes.yaml
2. For Windsurf in ./.windsurf

The primary workflow involves the interaction of three key modes: **Project Manager**, **Architect**, and **Code**, operating with adaptive context management.

## Adaptive Workflow Steps:

1.  **Initiation (User -> Project Manager):**
    *   The user interacts with the `Project Manager` mode to define high-level project goals, scope, constraints, and desired outcomes.
    *   The Project Manager focuses on understanding the big picture.

2.  **Delegation to Planning (Project Manager -> Architect):**
    *   The `Project Manager` delegates the detailed planning phase to the `Architect` mode.

3.  **Adaptive Planning & User Collaboration (Architect <-> User):**
    *   The `Architect` gathers context and assesses task complexity.
    *   **Lite-Touch (Default):** For simple tasks, the Architect creates a single, concise `plan.md` and may execute simple steps directly.
    *   **Heavy-Touch (If Needed):** For complex tasks, the Architect performs deeper research (using MCP), evaluates options, iterates with the user (Strawgate), and produces a full set of plans: `plan.md`, individual `plan-X.md` for workers, and `plan-verify.md`. It also defines worker requirements.
    *   **Context Monitoring:** The Architect monitors context size during planning.

4.  **Plan Review & Implementation Kick-off (Project Manager -> Code Agents):**
    *   The `Project Manager` reviews the plan(s).
    *   For heavy-touch plans, the PM assigns tasks to `Code` agents using their `plan-X.md` files and specifies logging requirements.

5.  **Task Execution (Code Agents):**
    *   Assigned `Code` agents execute steps from their `plan-X.md`.
    *   They use tools (like MCP) as needed and log progress (excluding raw code) to their work log.
    *   **Context Monitoring:** Code agents monitor context size during execution.

6.  **Adaptive Context Handoff (Architect/Code -> User/PM -> New Agent):**
    *   **Trigger:** If the Architect (during planning) or a Code agent (during execution) approaches a context size threshold (e.g., ~50k tokens), they propose a handoff to the user.
    *   **Handoff File Creation:** If approved, the current agent creates a `/plans/<plan_name>/handoff-<timestamp>.md` file containing: link to the main plan, status summary, remaining tasks, critical context, and the next step.
    *   **Notification:** The agent notifies the user/PM that the handoff file is ready.
    *   **New Instance Launch:** The `Project Manager` receives the handoff notification (directly or via the user), identifies the next required agent, and initiates a *new task* for that agent.
    *   **Context Transfer:** The PM instructs the new agent to use the specified `handoff-<timestamp>.md` file as its primary starting context, along with the original plan files.

7.  **Verification & Completion (Project Manager -> Verification Agent -> User):**
    *   Once work (potentially across multiple agent instances) is complete, the `Project Manager` assigns an agent to perform verification using `plan-verify.md`.
    *   After successful verification, the `Project Manager` oversees the final handoff to the user (Strawgate).

This adaptive workflow aims to optimize token usage by defaulting to simpler processes and segmenting tasks via file-based handoffs when context limits are approached, while still leveraging the specialized roles of each mode.

# Compiling Modes

```bash
uv sync 
uv run compile_modes.py
```

This will compile the modes into the following files:
1. ./custom_modes.yaml
2. ./.windsurf/rules/roo-modes

You can then use these files in your Roo or Windsurf instances.