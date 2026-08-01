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
ModelContextProtocol.StartServer
```

Use the no-argument command only for the compiled default endpoint. For a custom port, read [operations.md](operations.md) before restarting an existing server. Do not assume that a saved `ServerPortNumber` changes the no-argument console command in every installed build.

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
ServerPortNumber=8000
ServerUrlPath=/mcp
```

This plugin bundles Unreal's default port `8000`. Use another port when required by the local environment, and keep the Unreal setting and the effective Codex MCP URL matched.

For reliable custom-port startup, launch the Editor with:

```text
UnrealEditor <Project>.uproject -ModelContextProtocolStartServer -ModelContextProtocolPort=<port>
```

After startup, verify the exact port in the Unreal Output Log and on the operating-system listener. Configuration files alone are not runtime evidence.

## 3. Configure Codex

This plugin bundles the default endpoint in `.mcp.json`. When configuring a project without the plugin, run:

```text
ModelContextProtocol.GenerateClientConfig Codex
```

The command writes project-scoped `.codex/config.toml` for Codex. It refuses to overwrite an existing file; merge the server entry manually in that case.

A minimal manual entry is:

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"
```

When a project uses a custom endpoint, override the same server name in the target project's `.codex/config.toml` and keep it matched to the Unreal server. Do not publish machine-specific endpoints in the plugin defaults.

Do not keep duplicate plugin-bundled and project-scoped definitions if the host reports a name collision.

## Verify

- Confirm the Unreal Output Log shows server startup.
- Confirm the reported port matches the configured Codex URL and is owned by the Unreal Editor process.
- Confirm Codex lists `unreal-mcp` as connected.
- Call `list_toolsets`.
- Test a read-only request such as listing actors in the current level.
