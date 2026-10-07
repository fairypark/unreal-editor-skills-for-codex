# First-time Unreal MCP setup

Use this reference for first-time MCP configuration or optional proxy installation. Steps 1-3 configure direct HTTP access. The optional proxy keeps the client session open while Unreal is unavailable; live tools still require the Editor.

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

## 4. Optional: configure the Engine proxy for Codex

Check for `Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy` in the installed Engine. Keep direct HTTP access when it is absent. The executable is supplied by the Engine, not by this plugin.

Choose the binary for the operating system running the MCP client:

| Platform | Binary under `Extras/Proxy` |
|---|---|
| Windows x64 | `Bin/Win64/unreal_mcp_proxy.exe` |
| macOS arm64 | `Bin/Mac/unreal_mcp_proxy` |
| Linux x64 | `Bin/Linux/unreal_mcp_proxy` |
| Linux arm64 | `Bin/LinuxArm64/unreal_mcp_proxy` |

The Engine installer operates on an MCP JSON file, not Codex's TOML configuration. Prepare a project-owned `.mcp.json` with a direct `unreal-mcp` HTTP entry matching the actual Editor endpoint. Do not run the installer against the bundled plugin file or overwrite existing project configuration. From `Extras/Proxy`, run the matching binary with the actual JSON path:

```powershell
.\Bin\Win64\unreal_mcp_proxy.exe --mcp-json "C:\path\to\project\.mcp.json" install
```

On macOS use `./Bin/Mac/unreal_mcp_proxy`; on Linux use `./Bin/Linux/unreal_mcp_proxy` or `./Bin/LinuxArm64/unreal_mcp_proxy` with the same arguments.

The installer replaces the HTTP entry with a STDIO `unreal-mcp-proxy` entry and retains the original under `_upstreamEntry`. Preserve that metadata in the JSON file. For Codex, copy the generated entry's exact `command` and `args` into `[mcp_servers.unreal-mcp-proxy]` in the project's `.codex/config.toml`. Do not guess executable arguments or insert the install subcommand into the runtime entry. Copy `cwd` only when generated or required by the Engine README. `_upstreamEntry` is installer metadata, not a Codex TOML server field.

Disable the direct connection before enabling the proxy. For a plugin-bundled server, use the installed plugin identifier in the project configuration; for example, the personal installation uses:

```toml
[plugins."unreal-editor-skills-for-codex@personal".mcp_servers.unreal-mcp]
enabled = false
```

Use `@fairypark` when that is the installed marketplace. Disable any separate `[mcp_servers.unreal-mcp]` entry with `enabled = false` as well. Keep exactly one active Unreal connection. See the [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Reload the client configuration once after installation and start a new Codex task. Later Editor shutdowns normally do not require stopping the proxy. If an Editor integration rewrites the proxy JSON, turn off that integration's automatic client-configuration writes after authorization.

To restore direct access, run the same Engine command with `uninstall`, restore the direct Codex URL from `_upstreamEntry`, remove or disable the proxy entry, and re-enable the direct server. Reload the client configuration afterward.

The proxy's cached catalog is scoped to the configuration path, proxy path, Engine build identity, and client protocol version. A cached catalog or connected proxy does not prove live access. Follow [operations.md](operations.md#proxy-recovery) and the installed Engine's `Extras/Proxy/README.md` for cache behavior and transport limits.

## Verify

- Confirm the Unreal Output Log shows server startup.
- Confirm the reported port matches the configured Codex URL and is owned by the Unreal Editor process.
- Confirm Codex lists the configured `unreal-mcp` or `unreal-mcp-proxy` connection. For a proxy, connection status alone does not establish Editor reachability.
- Call `list_toolsets`.
- Test a read-only request such as listing actors in the current level.
