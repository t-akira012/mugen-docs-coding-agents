# CNS core invariants for coding agents

Source seed: <https://www.elecbyte.com/mugendocs/cns.html>

This file is a short operational index, not a replacement for the generated official corpus.

## Syntax

- CNS is organized into bracketed groups such as `[Statedef 200]` and `[State 200, 1]`.
- `;` starts a comment.
- Engine identifiers are generally case-insensitive, but do not normalize identifiers unnecessarily when editing existing code.

## State execution

- A `StateDef` defines the state context; its `State` blocks are controllers.
- Controller order is semantic: controllers are evaluated in source order.
- A state change can terminate processing of the remaining controllers in the state being processed.
- Special states and the current state are separate execution contexts; do not merge or reorder them as if they were ordinary configuration blocks.

## Trigger grouping

Conceptually:

```text
triggerall AND ((all trigger1) OR (all trigger2) OR (all trigger3) ...)
```

Repeated `triggerN` lines are an AND-group. Different trigger numbers are alternatives. Missing trigger numbers can affect which later trigger groups are considered, so renumbering is a behavioral edit.

## State controller safety

Before changing a controller, resolve its exact entry from `generated/index.json` and check its required parameters, optional parameters, defaults, expression rules, and target context.
