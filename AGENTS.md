# AGENTS.md

## Purpose

This repository provides a pre-generated local reference corpus for Elecbyte M.U.G.E.N character coding.
The intended use is to help coding agents edit WinMUGEN character CNS / CMD / AIR code by consulting the generated local documentation.

This file describes how to **use the generated corpus**. It does not describe how to build, regenerate, install, or maintain the corpus.

## Required lookup workflow

When engine behavior, controller syntax, trigger semantics, defaults, timing, or execution context must be checked:

1. Search `generated/index.json` first.
2. Locate the exact controller, trigger, CNS heading, or AIR heading.
3. Open the Markdown file referenced by the matching index entry.
4. Read only the relevant generated section and any directly related sections required to resolve the task.
5. Use `docs/` only for hand-written operational notes and compatibility boundaries.
6. Use existing character code only to learn project-local conventions, never as proof of engine semantics.

Do not skip `generated/index.json` and guess from memory when the local corpus contains the relevant specification.

## Local-only documentation rule

Use the documentation already present in this repository.

- Do not fetch Elecbyte documentation from the web during character-coding work.
- Do not run the documentation generator.
- Do not install or synchronize dependencies for the purpose of reading the corpus.
- Do not treat repository build or maintenance procedures as part of the character-coding task.

If the required behavior cannot be established from the local corpus, report it as unresolved or `unverified` instead of silently importing external behavior.

## Compatibility rule

The generated corpus includes material derived from M.U.G.E.N 1.0 documentation. Do **not** infer that every documented 1.0 feature exists in older WinMUGEN builds.

For strict WinMUGEN work:

- do not use M.U.G.E.N 1.1 or Ikemen GO extensions;
- treat a feature as WinMUGEN-compatible only when compatibility is established by the local corpus, `docs/COMPATIBILITY.md`, or the target runtime / character evidence;
- otherwise mark compatibility as `unverified`.

## Coding rules

- Preserve State Controller order. Reordering controllers can change behavior.
- Preserve repeated `triggerN` lines. Repeated lines with the same number form an AND-group; different numbered groups are alternatives.
- Do not renumber triggers across gaps without first establishing the semantics.
- Do not translate engine identifiers such as `StateDef`, `ChangeState`, `HitDef`, `AnimElem`, `Time`, `triggerall`, `persistent`, or `ignorehitpause`.
- Do not invent controller parameters, trigger names, defaults, or return values.
- Keep comments separate from executable CNS syntax. `;` begins a comment.
- Treat State -3, -2, -1 and the current state as distinct execution contexts.
- Treat Helper execution rules separately from Root Player rules.

## Editing character code

Before changing a controller or trigger:

1. identify the exact engine construct;
2. find it through `generated/index.json`;
3. verify required and optional parameters, defaults, and legal values;
4. verify execution context and trigger timing;
5. verify WinMUGEN compatibility when the behavior is version-sensitive;
6. make the smallest code change that satisfies the request.

Do not perform unrelated formatting, controller reordering, or broad cleanup together with a behavioral change.
