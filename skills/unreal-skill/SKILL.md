---
name: unreal-skill
description: Create, update, or review an Unreal Engine Agent Skill registered inside a live Unreal project, distinct from Codex SKILL.md files. Trigger for UAgentSkill, AgentSkillToolset CreateSkill/ListSkills/GetSkills/UpdateSkill, Python @agent_skill classes, skill UAssets, or project/plugin Skills folders. Do not trigger when authoring a Codex skill, creating an MCP toolset, or merely invoking an existing Unreal Agent Skill.
---

# Author an Unreal Agent Skill

Package durable project knowledge that an agent cannot infer from tool schemas, such as naming rules, folder layout, setup constraints, and canonical multi-step workflows.

## Apply design principles

- Include novel project knowledge, not facts discoverable through tools.
- Brief a knowledgeable Unreal colleague instead of writing introductory documentation.
- Keep instructions flexible enough to survive routine project changes.
- Avoid fixed tool names, orchestration details, model names, and other fragile host-specific references.
- Spend as little context as possible.

## Choose the implementation path

1. Invoke `AgentSkillToolset.ListSkills` and inspect relevant existing skills with `GetSkills`.
2. Reuse or update an existing skill when it already covers the workflow.
3. Choose:
   - a Python `UAgentSkill` subclass when the skill belongs to a version-controlled code plugin;
   - a Content Browser UAsset when the skill is project-specific and does not belong in a plugin.

## Write the two fields

- **Description:** one or two sentences explaining what the skill covers and when it applies.
- **Instructions:** the essential guidance loaded when the skill activates.

Assume the runtime agent discovers tools dynamically. Describe workflow and constraints rather than a fixed tool inventory.

## Python skill

```python
import unreal
from toolset_registry.agent_skill import agent_skill

_INSTRUCTIONS = (
    "Apply the project's canonical setup before creating this asset.\n"
    "Verify the result against the project naming and folder rules.\n"
)

@agent_skill
class MySkill(unreal.AgentSkill):
    """Provides project-specific guidance for the X workflow."""

    instructions = _INSTRUCTIONS
```

Place skill files in the plugin package's existing `skills/` area, import them from its `__init__.py`, and ensure `init_unreal.py` imports the package. Skills register on import. Reload the Python package before verification.

## UAsset skill

Use `AgentSkillToolset` through `$unreal-mcp`:

- Create with `CreateSkill`, providing `FolderPath`, PascalCase `AssetName`, `Description`, and `FAgentSkillDetails.Instructions`.
- Update with `UpdateSkill`, providing the full `SkillPath`, revised `Description`, and revised details.

## Verify

Load the final skill with `GetSkills` and read its description and instructions together. Confirm that the description is sufficient for correct activation and that the instructions teach durable project knowledge without wasting context.
