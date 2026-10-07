# Environment Requirements Dialogue Execution

Korean review counterpart: [requirements-dialogue.ko.md](requirements-dialogue.ko.md).

Use this reference when an environment execution request needs help expressing consequential intent or choosing a direction. With the Handbook available, follow Chapter 04's Collaborative requirements dialogue and Chapter 15's Requirements elicitation and direction-setting. This reference implements their conversational handoff; it does not introduce another design gate. Without the Handbook, apply it to the parent Skill's minimum fallback contract.

## Prepare the next decision

1. Read the existing request, accepted brief, references, current stage, prior answers, and relevant retained evidence. Reuse confirmed decisions and existing authorization. For a clear local edit, inspect only its unresolved scope and postcondition; do not launch a full concept questionnaire.
2. Identify the unknown with the largest effect on this stage's result or cost. Distinguish a user preference from a fact the agent can inspect. Resolve inspectable facts through authorized read-only discovery instead of asking the user to supply tool names, asset paths, camera properties, or existing setup. Use `unreal-mcp` for any live Editor inspection.
3. Summarize what is understood and why the remaining choice matters. When imagery helps, point to the actual reference or current diagnostic view and name the visible difference; do not claim to have seen inaccessible media or use a diagnostic view as approval evidence.

## Ask and suggest in understandable terms

- Use the available user-input interface or ordinary conversation in the user's language. Present a small batch of consequential questions, not a checklist of every possible field. Omit questions already answered and allow a free-text answer.
- Offer a small set of concrete, comparable alternatives when a direction is open. Put the recommended alternative first and explain its visible or playable result, reason, main trade-off, and uncertainty. Do not disguise an unverified asset, ownership claim, or feature capability as a feasible solution.
- Ask about image and experience decisions before implementation numbers: landmark prominence before mesh scale, route enclosure before scatter density, surface character before texture parameters, and maintainable authored exceptions before choosing a packing or instancing mechanism.
- If the user does not know how to choose, propose a baseline tied to their references and constraints and explain the observation that would test it. If they delegate a routine choice, make it within existing authority. A preselected option or no reply is not a submitted choice or approval.
- Keep dependent work pending when an answer is required; continue independent authorized work. For optional preferences, use stated reversible assumptions where appropriate without weakening the applicable stage gates.

## Example questions, selected by context

These are adaptable examples, not a mandatory sequence or a request to repeat established decisions.

| Current ambiguity | Question or direction to present |
| --- | --- |
| "Make a beautiful forest," with tone still open | "Should arrival feel calm and inviting, sheltered and mysterious, or exposed and tense? I recommend the direction that best matches the primary reference; the choice changes visibility and route rhythm." Name the actual reference basis rather than inventing one. |
| Calm tone is known, but composition is open | "Should the landmark remain visible through an open grove, or appear gradually through dense foreground groups? The open grove gives immediate orientation; the gradual reveal asks for stronger route guidance." Recommend from the accepted intent and inspected context. |
| "More natural," without a named defect | "Is the main problem equal spacing, isolated plants, abrupt path edges, or weak contact around rocks? From the current view, I propose repairing the observed problem first and comparing the same camera." Identify a problem only when the image supports it. |
| Focal shape differs from available assets | "Is this exact silhouette essential, or may we adapt the design to the available kit? A custom assembly preserves the silhouette but adds authoring and validation; adaptation may reduce integration work." Mark uninspected availability and costs as estimates. |
| "Finish it," with deliverable still open | "Is this pass aimed at a playable blockout, a representative visual slice, or wider production dressing? Here is what each relevant scope would deliver and require." Reuse the scope if already specified. |
| Existing named Actor should move two metres | Inherit the accepted design and define the transform, protected scope, and relevant checks. Ask only if direction, ownership, or a plan-owned relationship is materially ambiguous. |

## Record and hand off the answer

Update the existing brief or iteration record with the selected direction, source reference or prior decision, affected zone and view, priority, preserved requirements, observable target, unresolved assumptions, and required evidence. Keep confirmed intent distinct from proposed alternatives and assumptions. Do not create one file per answer or impose a new universal schema.

Translate conversational intent into the current stage's plan and acceptance criteria before choosing tools, graph parameters, transforms, materials, or lighting values. For example, a readable landmark becomes a focal silhouette and reveal requirement in the relevant views; natural ground cover becomes clustered strata, contact transitions, and explicit route openings. Derive numerical ranges from inspected scale and representative tests, not unsupported defaults.

Carry the decision into the existing plan, translation, readiness, and mutation contracts as applicable. Reopen only decisions whose assumptions changed. A direction choice does not authorize acquisition, broad reconstruction, or independent visual promotion. Preserve accepted systems and compare repairs from the agreed cameras. Apply all existing evidence-integrity and independent-review rules at their relevant gates.

The handoff is ready when the user can recognize their intent, the next bounded action and its authority are clear, and missing evidence is still labelled. More detailed questions alone are not a claim that the level or workflow has been validated.
