---
name: unreal-usage-metrics
description: Manage the optional local-only usage metrics for Unreal Editor Skills for Codex and extension-specific usefulness summaries. Trigger when the user accepts or declines the first-use metrics prompt, or asks to enable, disable, inspect, summarize, share an aggregate, rate, or delete the plugin's stored usage metrics, including UnrealToolsetsExtension metrics. Do not trigger for Unreal performance profiling, gameplay analytics, or unrelated telemetry.
---

# Unreal Usage Metrics

Use the bundled deterministic settings script. Do not edit the settings or event files directly.

## Resolve the script

Resolve this skill directory, then use `../../scripts/usage-metrics.ps1`. Run it with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<script-path>" -Action <action>
```

Choose one action:

- `Enable`: persist explicit consent and begin new local collection.
- `Disable`: stop new collection without deleting existing events.
- `Status`: show the current preference and whether local data exists.
- `Summary`: aggregate the stored events without exposing raw data.
- `Summary -Target UnrealToolsetsExtension`: show the extension-only local aggregate.
- `Summary -Target UnrealToolsetsExtension -Shareable`: return a
  non-identifying aggregate that suppresses operation rows with fewer than
  five samples. Never upload it.
- `Delete`: delete stored events while retaining the preference.
- `Feedback -Rating <1-5>`: record an optional local usefulness rating.
- `Feedback -Rating <1-5> -Target UnrealToolsetsExtension`: record an optional
  extension-specific local rating.

When the user answers the first-use question, run `Enable` for affirmative consent or `Disable` for refusal. Report the resulting state in plain language.

## Preserve consent boundaries

- Never enable collection without an affirmative user choice.
- Do not interpret silence or continued plugin use as consent.
- Keep disabling and deletion separate; delete only when explicitly requested.
- Do not upload or transmit metrics. This feature is local-only.
- Treat an old consent version as unset and ask again before collecting the
  expanded extension, Engine-version, safe-error, and verification fields.
- Store only exact cataloged extension operation metadata and allowlisted error
  codes. Never store error detail, dry-run arguments, or response content.
- Report `mutation_capable` separately from confirmed mutation when the safe
  invocation mode is unavailable.
- If the script reports an error, explain it and leave the user's prior preference unchanged.
