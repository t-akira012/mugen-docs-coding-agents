# Compatibility policy

## Target distinction

The repository is intended for WinMUGEN character coding, but the official Elecbyte CNS URL currently used as the seed corpus is explicitly labeled **M.U.G.E.N 1.0 (2009)**.

Therefore:

```text
M.U.G.E.N 1.0 documentation != automatic proof of WinMUGEN support
```

This distinction is mandatory for coding agents.

## Compatibility labels

Use these labels when recording normalized facts:

- `winmugen-confirmed` — independently established as valid for the target WinMUGEN runtime.
- `mugen-1.0-doc` — documented by the Elecbyte 1.0 corpus, but not yet established for WinMUGEN.
- `unverified` — insufficient evidence for the target runtime.

Do not upgrade `mugen-1.0-doc` to `winmugen-confirmed` by inference.

## Forbidden assumptions

Do not assume compatibility from:

- M.U.G.E.N 1.1 documentation;
- Ikemen GO documentation;
- random character code;
- a controller or trigger merely existing in the 1.0 reference;
- syntax accepted by a different MUGEN-family runtime.

When editing a strict WinMUGEN character, an unverified construct should be identified before it is introduced.

## Seed sources

See `sources.json`. The generated corpus records the source URL for every split section so the exact upstream context can be checked.
