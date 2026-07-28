---
name: unreal-usage-metrics
description: Manage the optional local-only usage metrics for Unreal Editor Skills for Codex. Trigger when the user accepts or declines the first-use metrics prompt, or asks to enable, disable, inspect, summarize, rate, or delete the plugin's stored usage metrics. Do not trigger for Unreal performance profiling, gameplay analytics, or unrelated telemetry.
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
- `Delete`: delete stored events while retaining the preference.
- `Feedback -Rating <1-5>`: record an optional local usefulness rating.

When the user answers the first-use question, run `Enable` for affirmative consent or `Disable` for refusal. Report the resulting state in plain language.

## Preserve consent boundaries

- Never enable collection without an affirmative user choice.
- Do not interpret silence or continued plugin use as consent.
- Keep disabling and deletion separate; delete only when explicitly requested.
- Do not upload or transmit metrics. This feature is local-only.
- If the script reports an error, explain it and leave the user's prior preference unchanged.
