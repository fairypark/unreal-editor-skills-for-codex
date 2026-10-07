# Unreal MCP operations and recovery

## Console commands

| Command | Purpose |
|---|---|
| `ModelContextProtocol.StartServer [port]` | Start the server, optionally on another port. |
| `ModelContextProtocol.StopServer` | Stop the server before a clean restart. |
| `ModelContextProtocol.RefreshTools` | Re-register toolsets after enabling a plugin. |
| `ModelContextProtocol.GenerateClientConfig Codex` | Generate Codex project configuration. |
| `ModelContextProtocol.GenerateClientConfig All` | Generate every supported client configuration. |

## Keep the effective endpoint consistent

Treat these as three independent facts that must agree:

1. the Codex MCP URL in `.mcp.json` or `.codex/config.toml`;
2. `ServerPortNumber` and `ServerUrlPath` in Unreal settings;
3. the address and port of the live listener owned by the Unreal Editor process.

Do not infer the live port from configuration alone. Verify the Unreal Output Log and the operating-system listener before reporting recovery.

The no-argument `ModelContextProtocol.StartServer` command can use the plugin's compiled default port instead of a saved custom-port setting. Never use it to restart a working custom-port server. A message such as “already running on port 8008, stopping first” followed by “starting on port 8000” is a failed recovery, not a harmless warning.

## Recover a custom-port connection

1. Read the effective Codex URL and Unreal settings before changing anything.
2. Inspect the listener owner. If the configured port is already owned by the target Unreal Editor, leave the server running.
3. Save the affected level and assets before any Editor restart.
4. If the server is down, run `ModelContextProtocol.StartServer <port>` only when the installed build demonstrably honors the argument. Stop if the Output Log reports another port; do not issue repeated start commands.
5. When console restart is unreliable, close the Editor cleanly and relaunch the project with:

   ```text
   UnrealEditor <Project>.uproject -ModelContextProtocolStartServer -ModelContextProtocolPort=<port>
   ```

6. Require all of the following before resuming mutations:
   - the process command line or startup configuration names the intended port;
   - the Unreal Output Log reports that exact port;
   - the operating system shows a listener on that port owned by Unreal Editor;
   - a newly initialized Codex task can call `list_toolsets`.

MCP tool inventory and connection state can be fixed at task initialization. Restoring the listener does not prove that the current task reconnected. Start a new task when the host still exposes no Unreal MCP meta-tools after server recovery.

## Run the deterministic preflight

Use this script for direct HTTP connections. It does not inspect a STDIO proxy's session or cached tool catalog; use the proxy recovery checks below for that transport.

From the `unreal-mcp` skill directory, run:

```text
python scripts/check_endpoint.py --project-root <project-root>
```

The script compares the discovered Codex HTTP URL, the per-user Unreal MCP
settings, the latest project log, the active TCP listener, and its owning
process. Treat a nonzero exit or `runtime_endpoint_verdict: FAIL` as a hard
stop. Do not restart the server merely because the preflight failed; resolve
the reported mismatch by evidence.

A runtime `PASS` deliberately returns `mutation_gate:
PENDING_LIST_TOOLSETS`. Clear that gate only from a newly initialized Codex
task by calling `list_toolsets` and one read-only Unreal query. The script does
not claim that the current task acquired MCP tools.

## Tool-search mode

Tool search is enabled by default and exposes only `list_toolsets`, `describe_toolset`, and `call_tool`. To expose every tool schema up front, set:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bEnableToolSearch=False
```

Keep the default enabled for ordinary Codex use because it reduces initial context.

## Proxy recovery

With the optional proxy, Codex connects to `unreal-mcp-proxy` over STDIO while the proxy reconnects to Unreal. Keep that configured connection during normal Editor recovery rather than adding a second direct HTTP connection.

- `unreal_mcp_status` reports whether the proxy holds an initialized upstream session. It does not test current reachability.
- Visible tools may come from a cached catalog. Require a successful `list_toolsets` call and a read-only Unreal query before resuming mutations.
- With no cached catalog and no upstream session, only `unreal_mcp_status` is exposed. After recovery the proxy sends `notifications/tools/list_changed`; the client must fetch `tools/list` again.
- If the host keeps a status-only or stale catalog, use its reconnect or configuration-reload action if available. Otherwise start a new Codex task; restart the client if its MCP session is still stale. Client refresh is separate from the proxy's normal reconnection to Unreal.
- Stopping an active proxy closes Codex's STDIO connection. `Transport closed` requires client reconnection; starting an unrelated proxy process does not repair it. Obtain authorization before stopping a proxy used by another active task.
- Inspect the recorded upstream endpoint, the target Editor's MCP startup log and listener owner, and proxy stderr when calls fail. Multiple running Editors do not establish which one the proxy targets. Follow the installed Engine's `Extras/Proxy/README.md` for its transport limits.

## Concurrent calls

MCP accepts concurrent requests and handles dispatch synchronization. Asynchronous operations can overlap, so submission order is not an execution or completion guarantee. Serialize dependent work and mutations affecting the same asset or Editor state. Keep game-thread MCP calls sequential under the project policy. Parallel work requires independent operations, explicit tool support for safe overlap, and permission from applicable project instructions. Coordinate ownership when multiple agents share one Editor.

## Recovery matrix

| Symptom | Recovery |
|---|---|
| Unreal tools are absent or `list_toolsets` fails | Check both direct and proxy configuration. Resolve the recorded endpoint and target Editor listener; follow Proxy recovery for a proxy connection. Use `ModelContextProtocol.StartServer` only for the compiled default port; follow custom-port recovery otherwise. |
| Configured port already in use | Identify the owning process. If it is the target Unreal Editor, keep the port. If another process owns it, choose one new port, update both sides, and restart cleanly. |
| Output Log switches from a custom port to the default | Treat recovery as failed. Save, close cleanly, and relaunch with explicit `-ModelContextProtocolStartServer -ModelContextProtocolPort=<port>` arguments. |
| Listener is healthy but tools remain absent | Start a new Codex task so the MCP client and tool inventory initialize again. |
| Expected toolset missing | Run `ModelContextProtocol.RefreshTools`; then verify the corresponding Unreal plugin is enabled. |
| Calls hang or fail | Wait for compilation or level loading; stop PIE when using Editor-only tools. |
| Docked context is empty | Dock the Codex surface inside a supported asset editor before querying docked context. |
| Concurrent calls produce conflicting results | Serialize dependent calls and mutations affecting the same state. Keep game-thread calls sequential; permit independent overlap only when tool support and project instructions allow it. |
