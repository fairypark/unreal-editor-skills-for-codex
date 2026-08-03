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

## Rendered acceptance evidence

When a project requires Movie Render Queue or Movie Render Graph output, use a reusable project-owned beauty configuration and enable `Render Warm Up Frames`. Record the configuration asset and output paths. Keep Object ID and other diagnostic passes separate from beauty evidence.

Preserve baseline, candidate, accepted, failed, and superseded artifacts as separate files. Never rewrite a failed result into a pass.
