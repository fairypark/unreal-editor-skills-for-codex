# First-time Unreal MCP setup

Use this reference only when the Unreal MCP server is not configured.

## 1. Enable Unreal plugins

Confirm the target `.uproject` path before editing it. Ensure its `Plugins` array enables:

```json
{
  "Name": "ModelContextProtocol",
  "Enabled": true
},
{
  "Name": "AllToolsets",
  "Enabled": true
}
```

`ModelContextProtocol` supplies the server and transport. `AllToolsets` supplies the tools. Enable selected toolset plugins instead of `AllToolsets` when a smaller surface is required.

## 2. Start the server

Start it for the current session from the Unreal console:

```text
ModelContextProtocol.StartServer 8008
```

For per-user auto-start, add this to:

```text
<Project>/Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini
```

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
```

The default endpoint is `http://127.0.0.1:8000/mcp`. Optional settings are:

```ini
ServerPortNumber=8008
ServerUrlPath=/mcp
```

Unreal's default endpoint uses port `8000`. This plugin intentionally bundles port `8008`; keep this setting and the Codex MCP URL matched. Use another port when required by the local environment.

## 3. Configure Codex

This plugin bundles the default endpoint in `.mcp.json`. When configuring a project without the plugin, run:

```text
ModelContextProtocol.GenerateClientConfig Codex
```

The command writes project-scoped `.codex/config.toml` for Codex. It refuses to overwrite an existing file; merge the server entry manually in that case.

A minimal manual entry is:

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8008/mcp"
```

Do not keep duplicate plugin-bundled and project-scoped definitions if the host reports a name collision.

## Verify

- Confirm the Unreal Output Log shows server startup.
- Confirm Codex lists `unreal-mcp` as connected.
- Call `list_toolsets`.
- Test a read-only request such as listing actors in the current level.
