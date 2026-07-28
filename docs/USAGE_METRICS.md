# Optional local usage metrics

This document records the product and maintenance decisions for measuring whether
Unreal Editor Skills for Codex is useful in real Codex work.

## Purpose

The feature measures outcomes rather than treating raw invocation counts as usefulness.
Its initial signals are:

- eligible Unreal sessions;
- Unreal MCP tool calls and explicit success or failure;
- retries within a turn;
- mutation turns followed by a read or verification call;
- optional user ratings from 1 to 5.

Do not collapse these signals into a single usefulness score until enough representative
data exists. Review activation, reliability, verification, efficiency, and feedback
separately first.

## Consent model

The preference has three states:

- `unset`: no decision has been saved;
- `enabled`: new local events may be collected;
- `disabled`: no new events are collected and the first-use question is not repeated.

When the preference is unset, the `SessionStart` hook may ask once after the user's current
task, and only in an Unreal project. The current task must continue without collection.
Silence, continued plugin use, or installing the plugin is not consent.

Disabling collection does not delete existing data. Deletion is a separate explicit action.
If the collected fields, storage destination, retention, or transmission policy materially
changes, increment `consent_version` and ask again.

## Privacy contract

Collection is local-only. The plugin must not transmit metrics.

Never store:

- user prompts or assistant messages;
- transcripts or transcript paths;
- working directories, project names, or file paths;
- Actor, Asset, object, or package names;
- MCP tool arguments;
- MCP tool response content;
- raw session, turn, or tool-call identifiers.

Session, turn, and tool-call identifiers are salted and hashed locally. Only generic MCP
meta-tool names, Toolset names, operation names, operation classes, outcomes, timestamps,
counts, durations, plugin versions, and explicit ratings may be stored.

Events are retained for at most 90 days and capped at 10,000 records. The storage root is
the user's local application-data directory:

```text
Codex/plugin-data/unreal-editor-skills-for-codex
```

`UNREAL_CODEX_METRICS_HOME` is a test and development override. It must not be used to add
remote or shared storage.

## Event model

`scripts/usage-metrics.ps1` writes newline-delimited JSON with `schema_version: 1`.

- `session_eligible`: a consented Unreal session started or resumed.
- `tool_started`: an observed Unreal MCP call began.
- `tool_finished`: the call completed with an explicit success/failure classification.
- `turn_summary`: aggregate counts for a turn containing Unreal MCP activity.
- `user_feedback`: an optional local 1-5 rating.

The first version observes exact Unreal MCP activity. Codex does not expose a dedicated
Skill-start hook, so `create-toolset` and `unreal-skill` activation must not be guessed from
prompt text or broad shell/file telemetry. Expand coverage only when a deterministic,
privacy-preserving signal is available.

## User controls

The `unreal-usage-metrics` Skill exposes deterministic actions:

- enable collection;
- disable new collection;
- show status;
- show an aggregate summary;
- record a 1-5 rating;
- delete stored events.

These controls should be available through natural-language requests. Do not require users
to locate or edit JSON files.

## Upstream isolation

Epic Games' repository remains the source of product behavior for the three upstream-derived
skills and the Unreal project-context workflow. Metrics are a Codex-specific extension.

Keep these upstream-derived areas free of metrics instructions:

- `skills/unreal-mcp/`;
- `skills/create-toolset/`;
- `skills/unreal-skill/`;
- `hooks/unreal-context.ps1`.

Keep metrics in:

- `scripts/usage-metrics.ps1`;
- `skills/unreal-usage-metrics/`;
- metrics-specific tests and documentation;
- small, clearly scoped entries in `hooks/hooks.json`.

When syncing upstream:

1. Compare the revision in `THIRD_PARTY_NOTICES.md` with Epic's current revision.
2. Port upstream behavior before changing the metrics integration.
3. Review `hooks/hooks.json` as the primary merge hotspot.
4. Re-run privacy, consent, Hook, Plugin, and Skill validation.
5. Update the recorded upstream revision only after the port is reviewed.

If Epic introduces overlapping analytics, consent, or lifecycle behavior, do not combine
the systems automatically. Review duplicate collection, consent scope, and event semantics
first.

## Required validation

Every metrics or Hook change must verify:

- no collection before affirmative consent;
- no prompt in non-Unreal directories;
- disabling immediately stops new collection;
- deletion retains the preference;
- private payload values cannot appear in the event log;
- Hook errors fail open and do not block Unreal work;
- `Stop` emits valid JSON;
- Plugin and every Skill pass the official validators;
- the plugin is reinstalled through the personal marketplace with a fresh cachebuster;
- a new Codex task loads the installed version.

Start live Unreal checks with read-only tools and keep game-thread MCP calls sequential.
