---
name: create-toolset
description: Create or extend Unreal Engine ToolsetRegistry toolsets exposed through unreal-mcp. Trigger when adding, exposing, or registering an AI-callable static method; creating a C++ or Python toolset; editing Toolsets folders; using UToolsetDefinition, AICallable, toolset_registry.tool_call, or ToolsetRegistry registration; designing tool schemas and tests; or filling a missing Landscape creation, heightmap, weightmap, material, statistics, or save API. Do not trigger when merely invoking existing tools, authoring an Unreal Agent Skill, or performing an unrelated refactor.
---

# Create an Unreal toolset

Design a small, typed, composable API for agents rather than mirroring Unreal's full internal API.

## Decide before editing

1. Search live toolsets with `list_toolsets` and `describe_toolset`, or inspect existing `Toolsets` source when the Editor is unavailable. Stop if the capability already exists.
2. Determine whether the request is an instance of a broader cross-domain operation. Put generic asset behavior in a generic asset toolset instead of duplicating it in a domain toolset.
3. Extend an existing domain toolset when one exists. Create a new toolset only for a distinct domain.
4. Place a new toolset in the closest existing plugin unless the domain warrants a separate plugin.
5. Compare Python and C++ support and let the user choose when both are viable:
   - Prefer Python when the required APIs exist in `Intermediate/PythonStub/unreal.py`.
   - Use C++ when Python coverage is insufficient.
   - Stop and report the gap when neither surface exposes the required API.
6. For Landscape creation, import, reimport, validation, or persistence, read [references/landscape-toolset.md](references/landscape-toolset.md). Keep environment art direction and quality gates in the environment-level-design skill; keep typed Editor mutations in the Unreal toolset.
7. This Codex skills repository does not own a runtime Unreal extension. If the missing capability needs new C++ or Python runtime code, record the verified gap and update [../../docs/UNREAL_TOOLSETS_EXTENSION_HANDOFF.md](../../docs/UNREAL_TOOLSETS_EXTENSION_HANDOFF.md); implement it only in the separately assigned runtime project.

Search the Python stub narrowly; do not load the whole generated file. Recommend enabling Python Developer Mode when the stub is missing.

## Enforce shared contracts

- Keep full CRUD symmetry where mutation is meaningful.
- Reuse existing generic tools such as `ObjectTools` property access.
- Use actual typed parameters and return values. Never hide structured data in JSON-formatted strings.
- Return data normally on success and raise on failure. Do not return status booleans or error strings.
- Make every exposed method static.
- Document toolsets, tools, parameters, return values, units, ranges, and non-obvious empty-result semantics.
- Remove documentation that merely restates signatures, types, defaults, or obvious call sequences.
- Cover every success path and each raised error condition with tests.

## Implement the selected language

- For C++, read [references/cpp-toolsets.md](references/cpp-toolsets.md).
- For Python, read [references/python-toolsets.md](references/python-toolsets.md).
- For compilation, automation tests, and final review, read [references/testing.md](references/testing.md).

## Review the complete API

Before handing off, check for duplicate tools, repeated boilerplate, incomplete error tests, inconsistent names or types, undocumented semantics, and excessive documentation. Fix the findings and rerun tests.
