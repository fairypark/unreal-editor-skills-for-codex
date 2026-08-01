# Independent Visual Supervision

Use a separate read-only agent as the visual quality authority when agent delegation is available. Keep the primary agent as the builder. This separation prevents the author of a change from quietly lowering the acceptance bar for that same change.

## Default activation

Start one supervisor for any multi-system environment build, rebuild, dressing pass, visual-quality recovery, golden slice, or full-level acceptance review.

Do not add this overhead to a single isolated Actor placement unless the user requests an independent review.

Reuse the same supervisor throughout the level session. Send focused follow-up reviews instead of creating a new agent for every capture.

## Reasoning profile

- Spawn the independent supervisor with `model="gpt-5.6-sol"` and
  `reasoning_effort="xhigh"` when supported.
- Prefer a `visual_critic` custom agent configured with the same model,
  reasoning effort, and read-only role.
- Keep the builder's reasoning effort independent from the supervisor setting.
- If `xhigh` or the preferred model is unavailable, use the highest supported
  reasoning effort and disclose the fallback before relying on the verdict.
- Never silently downgrade an independent visual gate or describe a
  lower-effort self-review as equivalent supervision.

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

### Sanitized supervisor packet

When project tooling supports it, require this handoff chain:

1. The builder writes a schema-restricted Review Submission containing only
   the recipe, review kind, factual change scope, required camera entries,
   evidence receipts, and external PNG/receipt hash trust anchors.
2. A project-owned packet builder rejects unknown fields and specifically
   forbids builder scores, intended verdicts, completion claims,
   implementation rationale, persuasive summaries, and suspected answers.
3. The builder revalidates every referenced concept, PNG, receipt, camera role,
   dimension, temporal threshold, and external hash at packet-generation time.
4. The tool writes a new immutable Supervisor Packet containing only the
   verified references, applicable observable frame contracts, evidence,
   rubric, factual scope, and neutral review instructions.
5. The supervisor receives that packet and its raw referenced files. It does
   not receive the Review Submission authoring conversation.

Packet generation failure blocks handoff. A hand-written summary is not a
fallback for a rejected or incomplete packet.

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
- Treat a recorded transform without a matching loaded `CameraActor` as invalid evidence.
- Compare the same camera, FOV, exposure, scalability, and weather state.
- Let temporal rendering settle before acceptance capture. Reject the first frame after a camera jump when Lumen, virtual textures, particles, fog, or temporal effects are visible.
- Reject captures with editor overlays, selection outlines, missing streaming state, or large rectangular or dithered temporal blocks.
- Keep baseline, candidate, and accepted evidence as separate files.

### Persistent capture gate

When `VisualEvidenceExtensionToolset` is available, use
`CaptureCameraToPng` for fixed-camera viewport evidence:

- pass the persistent `CameraActor`, never an unrecorded viewport pose;
- assign a stable `CameraRole` such as `arrival`, `hero`, `route`, `reverse`,
  `elevated`, or `contact`;
- write a unique versioned `.png` path beneath Project `Saved`; existing PNG
  and receipt paths must fail rather than overwrite history;
- require at least 1280x720 evidence unless the project explicitly documents a
  stricter minimum;
- use at least three warmup draws for Lumen, fog, virtual textures, particles,
  and other temporal systems, followed by two consecutive stable frame pairs
  under a mean RGB pixel-delta threshold no looser than 0.5;
- accept the file only when `CaptureCameraToPng` returns a paired
  `.evidence.json` receipt binding the expected role, loaded camera object
  path, world, applied camera-component view and post process, camera and
  viewport state, pixel dimensions, byte count, PNG
  64-character SHA-256, capture start and end, file modification time, UI-clean state, and
  zero remaining streaming, asset-compilation, and shader-compilation work.
  The receipt must also record the applied minimum dimensions and pixel-delta
  threshold.
- preserve the capture-returned PNG SHA-256 and receipt SHA-256 outside the
  receipt file as handoff trust anchors; do not recover either expected value
  from the files being verified.

Immediately before giving evidence to the supervisor, call
`VerifyEvidenceForSupervision` with the same persistent `CameraActor`, camera
role, relative PNG path, minimum dimensions, capture-returned PNG SHA-256, and
capture-returned receipt SHA-256. Handoff is prohibited unless that verifier
succeeds at handoff time. Treat a missing or modified receipt, stale or
jointly-rewritten PNG/receipt pair, camera or world mismatch, changed complete
camera view or post-process state, undersized image, overlay-contaminated
capture, or unsettled render state as a failed evidence gate.

The 1280x720 and 0.5 limits are tool-owned quality floors. A request may be
stricter but must never relax them, and the verifier must reject a receipt that
claims weaker applied thresholds.

Do not send a supervisor a stale screenshot merely because a requested path
exists. Reject zero-size files, non-PNG signatures, thumbnail-sized fallback
images, mismatched camera metadata, missing hashes or receipts, and files whose
timestamp falls outside the recorded capture interval.

If the extension tool is unavailable, persist the official viewport capture
through another verified file-writing path and record the same metadata. Keep
the gate pending until a raw local image can be inspected independently.

Before golden-slice or full-level promotion, prefer a reusable Movie Render
Queue or Movie Render Graph beauty-evidence configuration for the persistent
camera set. Enable `Render Warm Up Frames`; a warm-up count that only advances
the game thread is insufficient for render-dependent virtual textures, GPU
particles, fog, and similar systems. Record the configuration asset and output
paths, and never substitute Object ID or other diagnostic passes for the final
beauty evidence.

## Supervisor prompt template

Adapt this template without leaking the expected result:

```text
Act as the independent read-only visual supervisor for an Unreal environment.
Do not modify the project or create replacement evidence.

Reference:
- <concept or reference paths>

Evidence:
- arrival: <verified PNG path + receipt path>
- hero: <verified PNG path + receipt path>
- route: <verified PNG path + receipt path>
- reverse: <verified PNG path + receipt path>
- elevated or close audits: <verified PNG and receipt paths>

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
