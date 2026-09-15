# AGENTS.md

## Purpose

This repository is a machine-readable reference corpus for Elecbyte M.U.G.E.N character coding.
The immediate use case is editing WinMUGEN character CNS/CMD/AIR code with coding agents.

## Source-of-truth order

1. Official Elecbyte documentation listed in `sources.json`
2. Generated normalized documents under `generated/`
3. Hand-written notes under `docs/`
4. Existing character code, only as evidence of project conventions — never as proof of engine semantics

If two sources conflict, do not silently choose one. Report the conflict and prefer the higher source in the order above.

## Tooling rule: Makefile entry point, uv only

Repository operations must be exposed through the root `Makefile`.

- `make run` is the canonical full-run command. It must complete dependency synchronization, a full clean documentation build, and validation.
- Prefer existing Make targets over invoking underlying commands directly.
- If a new recurring repository operation is needed, add a Make target for it instead of documenting an ad-hoc shell command.
- Python dependency management and Python command execution inside the Makefile must use `uv` exclusively.
- Do not use `pip`.
- Do not use `python -m pip` or `python3 -m pip`.
- Do not add documentation, scripts, CI configuration, agent instructions, or Make targets that install dependencies with `pip`.
- CI should call the same Make targets used locally rather than duplicating build commands.

## Compatibility rule

The official CNS page used to seed this repository identifies itself as M.U.G.E.N 1.0 documentation (2009). Do **not** infer that every documented 1.0 feature exists in older WinMUGEN builds.

For strict WinMUGEN work:

- do not use M.U.G.E.N 1.1 or Ikemen GO extensions;
- treat a feature as WinMUGEN-compatible only when compatibility is established by an appropriate source or by the target character/runtime;
- otherwise mark compatibility as `unverified` instead of inventing an answer.

See `docs/COMPATIBILITY.md`.

## Coding rules

- Preserve controller order. State controllers are evaluated in source order and reordering can change behavior.
- Preserve repeated trigger numbers. Repeated `triggerN` lines form an AND-group; different `N` groups form alternatives.
- Do not renumber triggers across gaps without understanding the semantics.
- Do not translate engine identifiers such as `StateDef`, `ChangeState`, `HitDef`, `AnimElem`, `Time`, `triggerall`, `persistent`, or `ignorehitpause`.
- Do not invent controller parameters, trigger names, defaults, or return values.
- Keep comments separate from executable CNS syntax. `;` begins a comment.
- Treat State -3, -2, -1 and the current state as distinct execution contexts.
- Treat helper execution rules separately from root-player rules.
- When uncertain, locate the exact controller/trigger section in `generated/index.json` before editing code.

## Documentation workflow

For a complete local setup, build, and validation, run:

```bash
make run
```

This is the normal entry point. The Makefile synchronizes dependencies with `uv`, performs a clean build of the official documentation corpus, and validates the generated index.

Other supported operations are also exposed as Make targets, such as focused CNS/core builds and cleanup. Inspect `Makefile` rather than bypassing it with direct Python commands.

Generated vendor text is intentionally not committed.

For a focused lookup, search `generated/index.json` first, then open the referenced Markdown section.

## Editing character code

Before changing a controller or trigger:

1. identify the exact engine construct;
2. locate its reference entry;
3. verify required/optional parameters and defaults;
4. verify execution context and trigger timing;
5. make the smallest code change that satisfies the request.

Do not perform unrelated formatting or controller reordering while making a behavioral change.
