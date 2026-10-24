# Evidence and Supervision Operations

This reference defines how the execution layer produces and verifies fixed-camera evidence. The Handbook owns the general validation and independent-review principles.

## Persistent capture

When `VisualEvidenceExtensionToolset` is available:

1. Use a loaded persistent `CameraActor`, never an unrecorded viewport pose.
2. Call `CaptureCameraToPng` with a stable role such as `arrival`, `hero`, `route`, `reverse`, `elevated`, or `contact`.
3. Write each capture to a unique versioned `.png` path beneath the project's `Saved` directory. Do not overwrite prior evidence.
4. Require at least 1280x720 output and reject Editor overlays, selection outlines, incomplete streaming, compilation, or visible temporal blocks.
5. Preserve the paired `.evidence.json` receipt and the PNG and receipt SHA-256 values returned by the capture call outside both evidence files.
6. After moving the camera, wait for at least three warmup draws and two consecutive stable frame pairs when the tool reports those states.

The receipt must bind the persistent camera identity and role, world, transform, view and post-process state, FOV, dimensions, byte count, capture times, file modification time, settlement state, and 64-character SHA-256 digest.

## Gameplay-camera authority

For a documented native capture failure, consult [capture-fallback.md](capture-fallback.md). It preserves project authority, original frames, camera/state identity, freshness and independent review while explicitly labeling weaker evidence; it cannot replace a required native trust property.

- Read the project's actual player tracking camera before creating gameplay-visibility evidence. Record its height above local ground and FOV, including the representative state or mode when gameplay changes either value.
- Configure fixed arrival, route, landmark, reverse, building-scale, and typology cameras from that height-and-FOV contract. Preserve the local-ground relationship across elevation changes; do not reuse an arbitrary world Z.
- Label high overview or bird's-eye cameras `DIAGNOSTIC_ONLY`. Use them for zone, route, water-crossing, footprint, and marker-coverage audits only; never use them to approve player visibility, landmark readability, scale, or typology.
- Reject a gameplay-visibility packet when its receipt does not match the recorded player-camera height and FOV or when overview-only evidence is offered as acceptance proof.

## Handoff-time verification

Immediately before review, call `VerifyEvidenceForSupervision` with the capture-returned PNG and receipt hashes as external trust anchors. Reject missing, stale, jointly rewritten, mismatched, thumbnail-sized, or otherwise invalid pairs. Successful verification proves artifact integrity at handoff time; it does not prove visual quality.

If the project provides a schema-restricted Review Submission and supervisor-packet builder:

- reject unknown fields and builder-authored scores, intended verdicts, completion claims, implementation defenses, or persuasive summaries;
- revalidate every concept, capture, receipt, camera role, dimension, freshness rule, and external hash while generating the packet;
- write a new immutable Supervisor Packet containing only verified references, evidence, rubric, factual change scope, and neutral review instructions;
- stop the handoff when packet generation fails instead of substituting a hand-written summary.

## Independent reviewer handoff

Keep the builder responsible for Unreal mutations and the reviewer read-only. Follow the current host or project policy for the independent reviewer configuration. Supply:

- the selected references or concept;
- verified raw captures and camera roles;
- the applicable project rubric;
- previous equivalent evidence when comparison is required;
- factual change scope.

Do not supply the intended verdict or builder self-score. Ask the reviewer for the named target result, regressions, hard failures, weakest visible system, and one next change. A focused target pass does not imply full-level acceptance.

If independent delegation is unavailable, perform a separate comparison pass and label it `self-review; not independently supervised`.

## Mandatory blockout fidelity loop

For the blockout promotion gate, independent delegation is mandatory rather than optional. A self-review may identify defects but cannot set `BLOCKOUT_REFERENCE_FIDELITY_REVIEW` to `PASS` or unlock a representative slice, full layout, production meshing, or dressing. If the separate reviewer cannot run, keep the gate `PENDING_EVIDENCE` and report the delay immediately.

Build each immutable packet from:

- the applicable approved source references, including raw concept art and floor plan when required by the contract, with exact IDs, versions, crops or pages, approval and authority scopes; retain predeclared `NOT_APPLICABLE` decisions and never use them to waive missing required evidence;
- the execution trace: Handbook Stage 2a when available, otherwise the fallback plan-feature trace binding source and plan versions, feature and zone IDs, planned rules and tolerances, mutation scope, realized measurements, results, and unresolved deviations;
- verified fixed overview captures for macro layout and the runtime-camera captures or route samples declared by the current Handbook or fallback contract for player-facing relationships; Handbook stage numbering is not a standalone prerequisite;
- the project rubric, category floors, hard failures, prohibited readings, and camera-authority limits;
- the previous equivalent packet, iteration ID, factual change scope, elapsed time, and builder-reported checks not run.

Ask the reviewer to return only evidence-grounded findings: gate state, category results, hard failures, regressions, the weakest visible or spatial system, and one bounded next change. `PASS` requires the exact candidate to meet every applicable category floor with no hard failure and no unresolved mismatch among the applicable source-reference reading, floor-plan conformance, and runtime evidence. Evaluate concept-art categories only when the approved contract requires concept art. Relative improvement, aggregate score, Actor count, tool success, or a persuasive builder summary is insufficient.

On `FAIL`, preserve the packet and candidate. The builder changes one major system, captures the same camera and runtime conditions, and submits a new immutable packet to the separate reviewer. Continue this repair-capture-review loop until `PASS`. Do not reveal prior reviewer prose, consensus, or a desired verdict when a fresh or panel review must remain blind under host or project policy.

If repeated materially distinct repairs leave the same hard failure or show no credible convergence, stop broad mutation and produce a root-cause record separating implementation, asset or proxy, terrain or route representation, tool, capture, evaluator, platform, and budget causes from conflicting, underspecified, or infeasible concept-art and floor-plan requirements. Set `DESIGN_REVIEW_REQUIRED` only when the evidence supports reopening the source design; reopen the responsible Handbook stages when available, or the fallback contract, Area Composition Plan, and execution trace otherwise. Do not use redesign to excuse an implementation defect.

Before the first review, record the iteration/time budget and expected capture and review latency. Immediately report any issue likely to materially delay the loop: reviewer unavailability, timeouts, unstable Editor or streaming state, invalid receipts, changed cameras, unresolved source conflicts, missing assets or representation capability, repeated no-improvement, or projected budget overrun. Include cause, impact, current gate and downstream lock, elapsed attempts, safe work that remains possible, recovery options, and any owner decision required. Do not wait until the budget expires before reporting.

## Rendered acceptance evidence

When a project requires Movie Render Queue or Movie Render Graph output, use a reusable project-owned beauty configuration and enable `Render Warm Up Frames`. Record the configuration asset and output paths. Keep Object ID and other diagnostic passes separate from beauty evidence.

Preserve baseline, candidate, accepted, failed, and superseded artifacts as separate files. Never rewrite a failed result into a pass.
