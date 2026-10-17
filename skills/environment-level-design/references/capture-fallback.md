# Conditional fixed-camera capture fallback

Use only after a recorded native capture failure or unavailable capability prevents valid evidence. The preferred path remains native persistent-camera capture and handoff-time receipt verification. This reference does not waive a project's required native trust anchor or authorize a builder to lower an evidence gate. See the paired [Korean review](environment-reuse-review.ko.md).

## Admission

Record the failed attempt, engine/build, backend, failure signature, required camera set, candidate identity, expected render state, exception owner, and intended evidence scope. Classify content defects separately from capture failures. Repeated capture alone cannot repair changed cameras, incomplete streaming, or an invalid candidate.

Use an alternative only when the controlling contract permits it and the designated reviewer accepts its evidence class. If required native authenticity or other properties cannot be supplied, leave that gate `PENDING_EVIDENCE`; continue only work outside that dependency. Preserve original failures rather than rewriting them as success.

## Example: real-time PIE frame capture

This is a version-dependent adapter example, not an API guarantee or fixed timing recipe. Discover the available tools and validate a bounded canary in the target Editor before general use.

1. Resolve each persistent source camera and its matching PIE counterpart by stable identity. Read back the effective player camera manager location, rotation, FOV, aspect, post-process, exposure, viewport dimensions, and render settings. Compare them with the frozen source contract; a similarly named Actor is insufficient.
2. Hold the same view in an unpaused world. Record both world-time progress and completed ticks or draws. Choose the warmup and stability limits before capture. One tested static scene used at least three seconds and thirty ticks; these numbers do not establish settlement for other content.
3. Request ordinary engine screenshots to new versioned paths, serialize requests, and wait for each completed file. Preserve at least three original engine PNGs for two consecutive comparisons. Record request/completion times and frame counters, byte size, dimensions, file time, SHA-256, and effective state immediately before and after each request.
4. Reject absent, partial, reused, overwritten, wrong-size, wrong-camera, changed-state, paused, or stale output. Verify increasing frame/world time and capture order. Recompute file hashes and state comparisons at handoff; keep the manifest's independently recorded handoff digest outside the manifest.
5. Compute the declared pixel-stability metric from the original images. A prior static-scene profile used 4x4 block RGB mean absolute difference of at most 0.5 on the 0–255 scale for both adjacent pairs. Do not promote that threshold, downsampling, or profile to a universal default. Retain the metric implementation/version, full dimensions, per-pair values, and acceptance rule; inspect full-resolution images as well.
6. For moving water, wind, particles, exposure changes, or animated subjects, a static pixel-difference test may reject healthy output or miss local artifacts. Define an appropriate motion-aware contract or retain the result as diagnostic. Never freeze intended motion or suppress a failed region solely to pass a still-image threshold.
7. The reviewer checks clean imagery, required coverage, comparability, visible temporal defects, and content quality. Technical artifact verification cannot detect every overlay, prove source authenticity, or grant visual approval.

Label the manifest `native_receipt: false` and `verification_method: external_recompute`. Keep native diagnostic health captures separate and name their camera/purpose: a healthy native receipt from another camera does not authenticate the alternative images. A fallback failure remains `INVALID_EVIDENCE` or `PENDING_EVIDENCE`, never a self-approved visual pass.

## Cleanup and reuse

Track capture, verification, and cleanup outcomes independently. If images pass but PIE cleanup fails, retain the image result and report cleanup failure; audit and restore the intended Editor state. Revalidate the adapter after engine, rendering, camera, or lifecycle changes. Do not restart a completed build or duplicate Actors just because evidence transport failed.
