# Unreal Editor Skills for Codex

Community-maintained Codex workflows for controlling and extending a live Unreal Editor through MCP.

This project adapts Epic Games' MIT-licensed `unreal-engine-skills-for-claude-code-plugin` for Codex. It contains Codex skills, MCP wiring, and a Windows-native project-context hook. It does not bundle Unreal Engine code, `ModelContextProtocol`, or `AllToolsets`.

## Install

Add the Fairypark marketplace and install the plugin:

```powershell
codex plugin marketplace add fairypark/unreal-editor-skills-for-codex
codex plugin add unreal-editor-skills-for-codex@fairypark
```

Fully quit and restart the Codex or ChatGPT desktop app after installation. Start a new Codex task in the Unreal project so the installed skills, MCP connection, and session hook are loaded.

To update an existing installation:

```powershell
codex plugin marketplace upgrade fairypark
codex plugin add unreal-editor-skills-for-codex@fairypark
```

## Included skills

- `unreal-mcp`: inspect and mutate a live Unreal Editor safely.
- `create-toolset`: author AI-callable Unreal C++ or Python toolsets.
- `unreal-skill`: create project- or plugin-specific Unreal Agent Skills.
- `environment-level-design`: set up, build, and iteratively validate production-quality
  environment levels. It supports project-owned Visual Recipes, fixed-camera evidence,
  golden slices, and a separate read-only visual supervisor when agent delegation is available.
- `unreal-usage-metrics`: manage optional local-only usefulness metrics.

## Environment visual-quality onboarding

When an environment project has no project-owned quality policy, ask Codex to set one up.
The environment skill introduces an optional `off`, `recommended`, or `strict` workflow and
offers minimal, sample-informed, custom, or skipped setup. It never silently overwrites
`AGENTS.md` or treats the bundled CodexMiniArena case study as a universal preset.

The case study contains only the transferable procedure and judgment structure: establish
multi-direction concepts and fixed cameras, build a golden slice, request an independent
verdict, repair the weakest visible system, and recapture the same cameras before expansion.
Project-specific categories, thresholds, assets, coordinates, and art direction remain in the
user's project files.

한국어 생산 자산 안내는
[`재사용 가능한 생산 자산 사용 안내`](skills/environment-level-design/references/reusable-production-assets.ko.md)에서
확인할 수 있습니다. 설치 방법, 자갈길과 수생 식생 계약의 적용 순서, 재검증 및
UAsset 배포 범위를 한국어로 설명합니다.

## Optional local usage metrics

The plugin can collect small operational signals to help evaluate whether its Unreal
workflows are reliable and useful. Collection is off until the user explicitly opts in.
The first-use question appears only in an Unreal project and does not delay the current task.

Metrics remain on the user's device. The plugin never stores prompts, assistant messages,
paths, project names, Actor or Asset names, tool arguments, tool response contents, or raw
session identifiers. Events are retained for up to 90 days and can be summarized or deleted
at any time.

Ask Codex naturally:

- `Enable Unreal plugin usage metrics.`
- `Disable Unreal plugin usage metrics.`
- `Show my Unreal plugin usage metrics summary.`
- `Delete the stored Unreal plugin usage metrics.`

Disabling stops new collection but preserves existing events. Deletion is a separate explicit
action. See [`docs/USAGE_METRICS.md`](docs/USAGE_METRICS.md) for the complete privacy and
maintenance contract.

## Prerequisites

1. An Unreal Engine build that includes the `ModelContextProtocol` and `AllToolsets` plugins.
2. Both plugins enabled in the target `.uproject`.
3. Unreal Editor running with the server started:

   ```text
   ModelContextProtocol.StartServer
   ```

The bundled MCP connection uses Unreal's default endpoint, `http://127.0.0.1:8000/mcp`.

If the local environment requires a custom endpoint, configure it as a project-scoped override and keep the Unreal server endpoint and the effective Codex MCP URL in sync.

## Verify

1. Start Unreal Editor and its MCP server.
2. Start a new Codex task in the Unreal project.
3. Ask: `List the actors in the current level.`
4. Confirm that Codex discovers the Unreal toolsets and returns live Editor state.

The workflow was live-tested with Unreal Engine 5.8: MCP initialization, all three meta-tools, toolset discovery, project Agent Skill discovery, current-level lookup, and a read-only actor query completed successfully. The published default remains Unreal's port `8000`.

For environment work, the visual supervisor receives raw references and fixed-camera evidence
without the builder's intended verdict or self-score. The role is instruction-level read-only
unless the runtime supplies a technically restricted tool surface. Without delegation, the
review is labeled `self-review; not independently supervised`.

## Safety

MCP tools can modify live `UObject` state, assets, levels, and project files. Save and create a source-control recovery point before bulk operations. Keep Unreal MCP calls sequential, verify every result, and treat programmatic in-editor Python execution as privileged.

## Attribution

See `LICENSE` and `THIRD_PARTY_NOTICES.md`. This project is not affiliated with or endorsed by Epic Games, OpenAI, or Anthropic.

Reusable English and Korean introduction copy is available in
[`docs/PLUGIN_DESCRIPTION.md`](docs/PLUGIN_DESCRIPTION.md).
