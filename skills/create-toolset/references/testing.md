# Toolset testing and final review

## Live Editor loop

1. Compile C++ changes with `LiveCodingToolset.CompileLiveCoding` and fix diagnostics.
2. Invoke `AutomationTestToolset.DiscoverTests` before other automation-test tools.
3. Filter with `ListTests` to confirm discovery.
4. Run full test paths with `RunTests`.
5. Poll `GetTestStatus`.
6. Read detailed failures and warnings with `GetTestResults`.

Use `force_rediscover=true` after reloading Python packages when tests were added or removed.

## Coverage

For every tool, add at least:

- one success test that verifies the documented effect or returned data;
- one test for a meaningful empty or not-found result;
- one test for every condition that raises.

Use nearby `Plugins/Experimental/Toolsets` tests as the canonical style source. C++ tests normally use `BEGIN_DEFINE_SPEC` and Python tests extend `ToolCallTestCase`.

## Headless fallback

When no Editor is running:

```text
UnrealEditor-Cmd.exe <Project>.uproject -ExecCmds="Automation RunTests AI.MyToolset;quit" -Unattended -NullRHI
```

Match the test prefix and flags already used by the project.

## Final review

Review the whole toolset after tests pass. Remove duplicate behavior and boilerplate, align names and types with neighboring tools, test late-added errors, and cut documentation that can be inferred from signatures.
