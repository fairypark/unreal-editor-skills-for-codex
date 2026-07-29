# LandscapeToolset implementation contract

This repository documents the runtime contract but does not ship its Unreal Editor implementation. Runtime ownership belongs to the separately assigned, client-neutral extension project described in [../../../docs/UNREAL_TOOLSETS_EXTENSION_HANDOFF.md](../../../docs/UNREAL_TOOLSETS_EXTENSION_HANDOFF.md). Do not claim any tool is available until it is installed, enabled, registered, and discovered in a live Editor.

## Contents

- [Ownership and placement](#ownership-and-placement)
- [Typed tool surface](#typed-tool-surface)
- [Shared data contracts](#shared-data-contracts)
- [ReimportHeightmap transaction](#reimportheightmap-transaction)
- [Other operation requirements](#other-operation-requirements)
- [World Partition](#world-partition)
- [Errors and results](#errors-and-results)
- [Implementation surfaces](#implementation-surfaces)
- [Tests](#tests)
- [UI fallback](#ui-fallback)
- [Integration](#integration)

## Ownership and placement

- Put runtime behavior in a separately distributed, independent Unreal Editor plugin. `UnrealToolsetsExtension` is the current handoff name; keep the domain class named `ULandscapeExtensionToolset` to avoid collisions with a future Epic `ULandscapeToolset`.
- Depend on `ToolsetRegistry`, `Landscape`, `LandscapeEditor`, `UnrealEd`, `SourceControl`, and the smallest additional modules required by the installed engine version.
- Register `ULandscapeExtensionToolset` with `UToolsetRegistry` during module startup and unregister it during shutdown.
- Never edit `AllToolsets.uplugin`, another Epic plugin, or the installed Engine. The extension depends directly on `ToolsetRegistry` and remains independently removable.
- Use C++. Landscape creation and reliable height/weight writes require Editor APIs that are not guaranteed in the generated Python surface. Reconsider Python only when the installed `Intermediate/PythonStub/unreal.py` exposes every required operation.
- Keep artistic terrain composition, biome rules, building-pad design thresholds, and level quality gates in `environment-level-design`. This toolset owns typed inspection and mutation only.

## Typed tool surface

Expose one static `UFUNCTION(meta=(AICallable))` per operation:

```cpp
static FLandscapeInfoResult GetLandscapeInfo(ALandscapeProxy* Landscape);
static FLandscapeMutationResult CreateLandscape(const FLandscapeCreateRequest& Request);
static FLandscapeMutationResult ImportHeightmap(ALandscapeProxy* Landscape, const FLandscapeHeightmapImportRequest& Request);
static FLandscapeMutationResult ReimportHeightmap(ALandscapeProxy* Landscape, const FLandscapeHeightmapReimportRequest& Request);
static FLandscapeMutationResult ImportWeightmap(ALandscapeProxy* Landscape, ULandscapeLayerInfoObject* LayerInfo, const FLandscapeWeightmapImportRequest& Request);
static FLandscapeMutationResult SetLandscapeMaterial(ALandscapeProxy* Landscape, UMaterialInterface* Material);
static FLandscapeHeightStatistics GetHeightStatistics(ALandscapeProxy* Landscape, const FLandscapeRegion& Region);
static FLandscapeBuildingPadValidation ValidateBuildingPad(ALandscapeProxy* Landscape, const FLandscapeBuildingPadRequest& Request);
static FLandscapeSaveResult SaveLandscape(ALandscapeProxy* Landscape);
```

Resolve a streaming proxy to its canonical `ULandscapeInfo` and main Landscape actor. Reject null, stale, cross-world, PIE, and ambiguous targets. Never select a Landscape from Editor selection as an implicit fallback.

## Shared data contracts

Use reflected enums and structs rather than JSON strings.

`FLandscapeInfoResult` should include:

- canonical actor soft path and Landscape GUID;
- world soft path, actor transform, XY/Z scale, vertex extent, vertex resolution, and world-space bounds in centimeters;
- component, loaded component, and streaming-proxy counts;
- World Partition state and whether the full Landscape extent is loaded;
- edit-layer names and GUIDs, active material path, reimport source path, and dirty package paths.

`FLandscapeHeightStatistics` should include:

- sampled vertex region and sample count;
- raw uint16 minimum and maximum;
- world-space Z minimum, maximum, mean, standard deviation, and range in centimeters;
- the sample policy and whether it covered the full requested region.

`FLandscapeMutationResult` should include:

- operation name, canonical Landscape path, and recovery checkpoint description;
- modified package paths;
- before and after height statistics when height changed;
- representative before/after samples with vertex coordinates and world-space Z;
- whether collision, bounds, normals, materials, grass, navigation, and streaming state were refreshed;
- whether the post-operation save completed.

Do not add `success`, `error`, or JSON payload fields. A returned result means verified success. Raise a script error on failure.

Use explicit request fields for file path, expected width and height, Y flip, destination edit-layer GUID, region, transform policy, and save policy. For RAW input, require the caller to provide the resolution unless the sidecar metadata resolves it unambiguously.

## ReimportHeightmap transaction

Treat reimport as a guarded transaction, not a file-picker shortcut.

For a combined `.r16` heightmap and `.r8` layer-map workflow, add a separate
preflight plus atomic batch operation. A null target may auto-select only when
the Editor world contains exactly one canonical Landscape. Dry-run must resolve
the target, edit layers, `LandscapeLayerInfo` assignments, formats, resolutions,
extent, loaded World Partition coverage, source-control writability, transform,
material, Data Layers, and streaming layout without mutating or saving.
Execution must create both a durable package checkpoint and an exact raw-data backup,
preserve every non-target property, verify every imported layer and
height statistic, and roll back the entire batch on one failed postcondition.

1. Resolve the exact target.
   - Require `ALandscapeProxy* Landscape`.
   - Canonicalize through `ULandscapeInfo`.
   - Reject PIE, a different current world, a missing Landscape actor, or multiple actors sharing an unresolved label.
2. Validate the source before touching UObject state.
   - Convert to an absolute normalized path and require an existing regular file.
   - Resolve the installed heightmap handler with `ILandscapeEditorModule::GetHeightmapFormatByExtension`.
   - Use `FLandscapeImportHelper::GetHeightmapImportDescriptor` and read the selected import data.
   - Require a supported 16-bit height format. Reject 8-bit PNG, unknown RAW resolution, tiled-set gaps, and descriptor errors.
   - Compare source width and height with the requested target vertex region. Default reimport policy is exact match; never silently crop, pad, resample, or reinterpret byte order.
3. Establish a recovery point.
   - Enumerate the Landscape actor, streaming proxies, components, heightmap textures, edit-layer objects, external actor packages, and map package that can change.
   - Check source-control writability where applicable.
   - Save every dirty affected package before mutation. Abort if any required package cannot be saved.
   - Start `FScopedTransaction`, call `Modify()` on affected objects, and capture the original uint16 height data for the full write region in memory.
   - Return the saved package paths and transaction label in the success result. Do not describe an undo transaction alone as a durable source-control checkpoint.
4. Enforce World Partition coverage.
   - Compute all components and external actor packages intersecting the write region.
   - Require them to be loaded and writable, or load them through an explicit supported World Partition workflow before mutation.
   - Abort before mutation when coverage is partial. Never reinterpret `loaded only` as full-Landscape success.
5. Apply through public data APIs.
   - Prefer the installed engine version's public import and edit surfaces, including `FLandscapeImportHelper` and `FLandscapeEditDataInterface`.
   - Do not call private `FEdModeLandscape` methods or drive the Landscape panel.
   - Write to the explicit destination edit layer. Reject a missing or locked layer and never substitute the active UI layer.
   - Mark packages dirty and refresh derived Landscape state required by the installed version.
6. Verify before commit.
   - Re-read the full affected region and compute height statistics.
   - Verify raw minimum and maximum, world-space Z range, resolution, and full sample coverage.
   - Verify at least nine representative vertices: center, four corners, and four edge midpoints. Compare them with the decoded source data using an explicit raw-height tolerance, normally zero.
   - Confirm affected component bounds and collision height data were refreshed.
7. Save and report.
   - When the request requires save-on-success, save all modified packages and fail if any save fails.
   - Return `FLandscapeMutationResult` only after verification and the requested save complete.
8. Roll back on every failure after mutation begins.
   - Restore the captured uint16 data, refresh derived state, and re-read representative points.
   - If in-memory rollback verification fails, leave the pre-save packages untouched on disk, identify the affected packages in the raised error, and require an Editor reload.
   - Raise one stable error code and concise context. Never return a partially successful result.

Suggested stable failures include:

- `LANDSCAPE_TARGET_INVALID`
- `LANDSCAPE_SOURCE_NOT_FOUND`
- `LANDSCAPE_SOURCE_FORMAT_UNSUPPORTED`
- `LANDSCAPE_SOURCE_RESOLUTION_MISMATCH`
- `LANDSCAPE_WORLD_PARTITION_PARTIAL`
- `LANDSCAPE_RECOVERY_SAVE_FAILED`
- `LANDSCAPE_DESTINATION_LAYER_INVALID`
- `LANDSCAPE_MUTATION_FAILED_ROLLED_BACK`
- `LANDSCAPE_MUTATION_FAILED_RELOAD_REQUIRED`
- `LANDSCAPE_POST_VERIFY_FAILED`
- `LANDSCAPE_POST_SAVE_FAILED`

## Other operation requirements

### GetLandscapeInfo

Return facts without loading or mutating Landscape packages. An empty reimport source path is valid and documented as `not associated`.

### CreateLandscape

- Require world, actor label, location, scale, sections per component, quads per section, and component counts.
- Validate Unreal's Landscape dimension formula before spawning.
- Use `ALandscape::Import` or the installed public equivalent and initialize layer data explicitly.
- For a World Partition world, follow the installed version's streaming-proxy creation path; do not create disconnected Landscape actors to imitate partitioning.
- Delete the newly spawned actor and restore packages if initialization or verification fails.

### ImportHeightmap

Use the same source validation as reimport. Permit a non-exact transform only when the request names a transform enum and the result reports it. Do not overload this method to create a Landscape.

### ImportWeightmap

- Require a specific `ULandscapeLayerInfoObject`, destination edit-layer GUID, region, and 8-bit source.
- Validate layer ownership, no-weight-blend semantics, resolution, and transform before mutation.
- Verify representative weight values and the affected layer allocation after import.

### SetLandscapeMaterial

Validate that the material supports Landscape use, set it on the canonical Landscape, update material instances for all affected proxies, and return modified packages. Do not create or rewrite materials here.

### GetHeightStatistics

Report world-space centimeters and raw uint16 values. Use full enumeration for a bounded region. If a caller requests sampling for a very large region, require an explicit sampling policy and report incomplete coverage instead of presenting an estimate as exact.

### ValidateBuildingPad

- Accept an oriented world-space footprint, optional nine or more sample offsets, maximum height variation in centimeters, and maximum slope in degrees.
- Project each point to the target Landscape only; do not let props or other collision surfaces answer the query.
- Return each sample, min/max/range, best-fit plane slope, pass/fail threshold evaluations, and missing-sample reasons.
- This is a measurement tool. It must not flatten terrain or encode a universal design threshold.

### SaveLandscape

Resolve and save all dirty packages owned by the Landscape, streaming proxies, components, height/weight textures, edit layers, external actors, and map as required by the installed version. Return saved and unchanged package paths; raise with failed package paths.

## World Partition

Make loaded coverage an explicit part of every read and mutation result. Whole-Landscape operations require whole affected-region coverage. Region operations require every intersecting cell/component package. If the plugin cannot load the required cells through a stable API, fail before mutation and instruct the caller to load them; do not fall back to UI automation inside the tool.

Large tiled imports may warrant a `UToolCallAsyncResult` with progress and cancellation. Cancellation must use the same rollback path and may report success only after final verification.

Treat Landscape extent and streaming partitioning as independent decisions.
Reserve enough Landscape resolution for plausible expansion, but derive proxy
grid size from measured streaming need. Provide a read-only streaming proxy audit before
any rebuild. Report proxy count, grid size, components per proxy, loaded
coverage, material/Data Layer state, and a reasoned recommendation. Proxy count
is an outcome, never a quality target. A rebuild requires an exact stale-plan
guard, explicit confirmation, complete coverage, checkpoint, post-rebuild
audit, representative height checks, and a reload-required error when recovery
cannot be verified.

## Errors and results

Follow ToolsetRegistry's normal contract:

- return typed data after verified success;
- raise a script error with a stable code on failure;
- do not return status booleans, error strings, or JSON-formatted strings;
- include enough context to identify the target, source, rejected dimension, or failed package without leaking file contents;
- never label a dirty in-memory mutation as saved.

This gives callers an explicit outcome: a complete typed success result or a raised failure. Transport success alone is not operation success.

## Implementation surfaces

Verify names against the installed engine version, then prefer:

- `ILandscapeEditorModule` and `FLandscapeImportHelper` for format lookup, descriptor validation, and decoding;
- `ALandscape::Import` for creation;
- `ULandscapeInfo::GetLandscapeExtent` for exact vertex bounds;
- `FLandscapeEditDataInterface` for height and weight reads/writes;
- public Landscape refresh APIs for layers, bounds, normals, collision, grass, materials, and navigation;
- `FEditorFileUtils`, `UEditorLoadingAndSavingUtils`, and source-control helpers for package persistence;
- public World Partition Editor APIs for cell and external-actor package coverage.

Do not depend on private `FEdModeLandscape` or detail-customization classes. They are UI implementation details and make a toolset brittle across Engine revisions.

## Tests

Create Editor automation specs under a stable prefix such as `AI.LandscapeToolset`.

Cover each tool's success path, null/stale target, wrong world, PIE rejection, meaningful empty state, and every raised error. At minimum add:

- creation dimension formula and cleanup after forced failure;
- PNG16 and RAW16 import, unsupported format, missing file, wrong bit depth, and resolution mismatch;
- exact reimport with before/after min/max and nine-point equality;
- pre-save failure before mutation;
- injected write failure with verified in-memory rollback;
- injected rollback failure that identifies reload-required packages;
- World Partition partial coverage rejection and full-region success;
- weightmap layer mismatch and representative-value verification;
- material propagation to streaming proxies;
- exact and sampled statistics semantics;
- rotated building-pad sampling, missing samples, height range, and slope thresholds;
- save success, unchanged packages, source-control refusal, and failed package reporting.

Run ToolsetRegistry discovery, compile, focused tests, and result inspection using [testing.md](testing.md). A static Skill validation does not prove the C++ plugin works in a live Editor.

## UI fallback

UI automation is not part of `LandscapeToolset`. Use it only as a temporary, user-approved workaround when the live toolset is absent and no other structured API can complete the immediate task.

1. Save and establish an external recovery point.
2. Observe only the required Landscape panel subtree.
3. Perform the smallest possible UI action.
4. In finally-style cleanup, call `SlateInspectorToolset.Unobserve` with every identifier returned by `Observe`, including after errors.
5. Confirm `ListObservers` contains no observer created by the workflow.
6. Verify the target, resolution, height range, representative points, and saved state through structured tools. If structured verification is also unavailable, report the outcome as unverified.

Never promote a successful screen interaction into evidence that a reusable Landscape API exists.

## Integration

After the separate runtime project implements and distributes the Unreal plugin:

1. Copy the external extension into the target project's `Plugins` directory and enable it. Do not modify `AllToolsets.uplugin`.
2. Build the Editor target and run `AI.LandscapeToolset`.
3. Restart the Editor when module loading requires it.
4. Run `ModelContextProtocol.RefreshTools`.
5. Confirm `list_toolsets` includes `LandscapeExtensionToolset`.
6. Confirm `describe_toolset` exposes all nine typed methods.
7. Exercise `GetLandscapeInfo` and `GetHeightStatistics` read-only before any mutation.
8. Use `environment-level-design` for the level-building workflow and quality thresholds, and this toolset only for Landscape operations.
