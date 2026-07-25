# Unreal MCP operations and recovery

## Console commands

| Command | Purpose |
|---|---|
| `ModelContextProtocol.StartServer [port]` | Start the server, optionally on another port. |
| `ModelContextProtocol.StopServer` | Stop the server before a clean restart. |
| `ModelContextProtocol.RefreshTools` | Re-register toolsets after enabling a plugin. |
| `ModelContextProtocol.GenerateClientConfig Codex` | Generate Codex project configuration. |
| `ModelContextProtocol.GenerateClientConfig All` | Generate every supported client configuration. |

## Tool-search mode

Tool search is enabled by default and exposes only `list_toolsets`, `describe_toolset`, and `call_tool`. To expose every tool schema up front, set:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bEnableToolSearch=False
```

Keep the default enabled for ordinary Codex use because it reduces initial context.

## Recovery matrix

| Symptom | Recovery |
|---|---|
| Server absent or `list_toolsets` fails | Start the Editor and run `ModelContextProtocol.StartServer 8008` for the bundled configuration; inspect the Output Log. |
| Port already in use | Change `ServerPortNumber`, restart the Editor, and update `.mcp.json` or `.codex/config.toml`. |
| Expected toolset missing | Run `ModelContextProtocol.RefreshTools`; then verify the corresponding Unreal plugin is enabled. |
| Calls hang or fail | Wait for compilation or level loading; stop PIE when using Editor-only tools. |
| Docked context is empty | Dock the Codex surface inside a supported asset editor before querying docked context. |
| Calls collide | Stop parallel execution and serialize all Unreal MCP calls. |
