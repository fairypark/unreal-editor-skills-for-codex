# Independent Visual Supervision

Use a separate read-only agent as the visual quality authority when agent delegation is available. Keep the primary agent as the builder. This separation prevents the author of a change from quietly lowering the acceptance bar for that same change.

## Default activation

Start one supervisor for any multi-system environment build, rebuild, dressing pass, visual-quality recovery, golden slice, or full-level acceptance review.

Do not add this overhead to a single isolated Actor placement unless the user requests an independent review.

Reuse the same supervisor throughout the level session. Send focused follow-up reviews instead of creating a new agent for every capture.

## Role contract

### Builder

- Own Unreal mutations, file edits, saves, captures, and implementation decisions.
- Supply the selected concept or reference, fixed-camera evidence, applicable scoring rubric, and prior audit when one exists.
- Keep historical audits. Never overwrite a failed verdict to make the current state appear accepted.
- Repair the weakest visible system before adding unrelated decoration.
- Do not declare a gate passed on the supervisor's behalf.

### Supervisor

- Remain read-only. Do not mutate Unreal state, project files, captures, audits, or source assets.
- Judge the raw evidence against the selected reference and quality gates.
- Treat target-level `PASS` and full-level `GO` as separate decisions. A target `PASS` does not imply full-level `GO`.
- Change a score only when the new evidence visibly supports the change.
- Report hard failures, per-camera blockers, the weakest system, and one next change.
- Do not reward Actor count, effort, tool success, or the builder's confidence.

## Preserve independence

When the delegation tool supports it, start the supervisor with no inherited conversation or only the minimum task-local turns. Give it:

- the primary concept or reference paths;
- raw capture paths and camera roles;
- the relevant rubric;
- the previous raw evidence or previous score when comparison is required;
- factual change scope, such as the affected system and Actor count.

Do not give it:

- the intended verdict;
- the builder's self-score;
- a defense of the implementation;
- a suspected answer disguised as a question.

Ask the supervisor to inspect artifacts directly. Do not substitute the builder's description for visual evidence.

## Required review points

### Golden-slice candidate

Before scaling the system across the map, obtain:

- fixed player-height and elevated evidence;
- a reverse view;
- applicable contact close-ups;
- a target verdict;
- a full golden-slice verdict.

Expand only after the golden slice has no unresolved hard failure.

### Target repair

After a failed gate, change one major system and request a focused before-and-after review. Require:

1. `PASS` or `FAIL` for the named target;
2. any new regression or hard failure;
3. one next change.

Do not interpret a target `PASS` as full-level acceptance.

### Full-level acceptance

After the final required camera set is captured, request the complete 1-to-5 category scores, aspirational visual impact, resolved findings, hard failures, per-camera blockers, weakest system, one next change, and `GO` or `NO-GO`.

The supervisor's unresolved hard failure blocks completion.

## Evidence protocol

- Use persistent cameras for arrival, hero, route, reverse, elevated overview, and required close audits.
- Compare the same camera, FOV, exposure, scalability, and weather state.
- Let temporal rendering settle before acceptance capture. Reject the first frame after a camera jump when Lumen, virtual textures, particles, fog, or temporal effects are visible.
- Reject captures with editor overlays, selection outlines, missing streaming state, or large rectangular or dithered temporal blocks.
- Keep baseline, candidate, and accepted evidence as separate files.

## Supervisor prompt template

Adapt this template without leaking the expected result:

```text
Act as the independent read-only visual supervisor for an Unreal environment.
Do not modify the project or create replacement evidence.

Reference:
- <concept or reference paths>

Evidence:
- arrival: <path>
- hero: <path>
- route: <path>
- reverse: <path>
- elevated or close audits: <paths>

Stage: <golden slice | target repair | full level>
Previous evidence or scores: <only when comparison is required>
Factual change scope: <system and affected content>

Judge only visible evidence. Do not reward effort or Actor count.
Return the requested verdict, hard failures, camera blockers, weakest system,
and one next change. Change scores only when the evidence supports it.
```

## Handling disagreement

The builder may challenge a finding only with concrete evidence such as a corrected capture, verified camera mismatch, missing reference, or measurable false premise. Send that evidence back to the same supervisor for reconsideration. Do not silently override the verdict.

If a capture is invalid, fix the evidence before changing content.

## Fallback when delegation is unavailable

Perform a separate read-only review pass and label it `self-review; not independently supervised`. Use the same rubric and evidence contract, but do not claim independent supervision.

If independent acceptance is required by the user or project policy, preserve the pending gate and request a later review from a separate agent or person.
