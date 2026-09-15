# WinMUGEN docs for Coding Agents

Agent-readable documentation infrastructure for Elecbyte M.U.G.E.N character coding.

The repository does **not** blindly mirror the upstream HTML. It gives coding agents:

- a fixed source manifest;
- deterministic HTML -> Markdown normalization;
- one-file-per-section lookup material;
- a JSON section index;
- explicit engine-compatibility rules;
- operational instructions in `AGENTS.md`.

## Build the local corpus

```bash
python3 -m pip install -e .
python3 scripts/build_docs.py
```

For CNS only:

```bash
python3 scripts/build_docs.py --only cns
```

For the main character-coding references:

```bash
python3 scripts/build_docs.py --only cns,sctrls,trigger
```

A clean rebuild:

```bash
python3 scripts/build_docs.py --clean
```

## Output

```text
generated/
├── index.json
├── full/
│   ├── cns.md
│   ├── sctrls.md
│   ├── trigger.md
│   └── air.md
└── sections/
    ├── cns/
    ├── sctrls/
    ├── trigger/
    └── air/
```

`generated/index.json` maps each split heading to its Markdown file and original Elecbyte URL. Coding agents should search this index before guessing controller or trigger semantics.

## Repository map

```text
AGENTS.md                 Agent behavior and coding rules
llms.txt                  Compact LLM entry-point index
sources.json              Official source manifest
docs/CNS_CORE.md          Short CNS execution/trigger invariants
docs/COMPATIBILITY.md     WinMUGEN vs M.U.G.E.N 1.0 boundary
scripts/build_docs.py     Fetch/normalize/split/index builder
pyproject.toml            Builder dependencies
```

## Compatibility warning

The Elecbyte CNS page used here identifies itself as **M.U.G.E.N 1.0 documentation (2009)**. This repository is intended to support WinMUGEN coding, but 1.0 documentation is not by itself proof that a feature exists in an older WinMUGEN runtime.

Agents must follow `docs/COMPATIBILITY.md` and avoid silently importing M.U.G.E.N 1.1 or Ikemen GO behavior.

## Source documents

The initial corpus is defined in `sources.json` and currently includes:

- CNS format
- State Controller Reference
- Trigger Reference
- AIR format

The authoritative upstream text is fetched from Elecbyte at build time rather than committed as a vendor copy.
