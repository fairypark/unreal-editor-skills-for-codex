# Unreal Editor Skills for Codex

Community-maintained Codex workflows for controlling and extending a live Unreal Editor through MCP.

This project adapts Epic Games' MIT-licensed `unreal-engine-skills-for-claude-code-plugin` for Codex. It contains Codex skills, MCP wiring, and a Windows-native project-context hook. It does not bundle Unreal Engine code, `ModelContextProtocol`, or `AllToolsets`.

## Included skills

- `unreal-mcp`: inspect and mutate a live Unreal Editor safely.
- `create-toolset`: author AI-callable Unreal C++ or Python toolsets.
- `unreal-skill`: create project- or plugin-specific Unreal Agent Skills.

## Prerequisites

1. An Unreal Engine build that includes the `ModelContextProtocol` and `AllToolsets` plugins.
2. Both plugins enabled in the target `.uproject`.
3. Unreal Editor running with the server started:

   ```text
   ModelContextProtocol.StartServer 8008
   ```

Unreal's default MCP port is `8000`. This plugin bundles `http://127.0.0.1:8008/mcp` to avoid a local port conflict. If you use another port or path, keep the Unreal server settings and `.mcp.json` in sync.

## Verify

1. Start Unreal Editor and its MCP server.
2. Start a new Codex task in the Unreal project.
3. Ask: `List the actors in the current level.`
4. Confirm that Codex discovers the Unreal toolsets and returns live Editor state.

The bundled configuration was live-tested with Unreal Engine 5.8 on port `8008`: MCP initialization, all three meta-tools, toolset discovery, project Agent Skill discovery, current-level lookup, and a read-only actor query completed successfully.

## Safety

MCP tools can modify live `UObject` state, assets, levels, and project files. Save and create a source-control recovery point before bulk operations. Keep Unreal MCP calls sequential, verify every result, and treat programmatic in-editor Python execution as privileged.

## Attribution

See `LICENSE` and `THIRD_PARTY_NOTICES.md`. This project is not affiliated with or endorsed by Epic Games, OpenAI, or Anthropic.
