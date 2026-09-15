# Coding Agents 向け WinMUGEN ドキュメント

[English](README.md)

Elecbyte M.U.G.E.N のキャラクターコーディング仕様を、Coding Agent が参照しやすい形へ変換・索引化するためのドキュメント基盤です。

このリポジトリは、公式 HTML をそのまま複製するものではありません。Coding Agent 向けに以下を提供します。

- 固定された公式ソース一覧
- 決定的な HTML → Markdown 正規化
- セクション単位で分割された参照ファイル
- JSON 形式のセクション索引
- エンジン互換性に関する明示的な規則
- `AGENTS.md` / `AGENTS.ja.md` による Agent 向け運用指示

## すべて実行する

操作窓口はルートの `Makefile` に統一します。

```bash
make run
```

`make run` だけで、依存関係の同期、全ドキュメントの clean build、生成された index の検証まで完了します。

補助 target:

```bash
make cns
make core
make clean
```

- `make cns`: CNS ドキュメントのみ生成する。
- `make core`: CNS、State Controller、Trigger の主要資料を生成する。
- `make clean`: 生成物を削除する。

Makefile 内での Python 依存関係管理と実行には `uv` のみを使用します。

## 生成物

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

`generated/index.json` には、分割された各見出しと対応する Markdown ファイル、および Elecbyte 公式 URL の対応関係が記録されます。Coding Agent は Controller や Trigger の仕様を推測する前に、この索引を検索してください。

## リポジトリ構成

```text
Makefile                  ローカル・CI 共通の操作窓口
AGENTS.md                 Agent の動作・コーディング規則
AGENTS.ja.md              上記の日本語版
README.md                 英語版 README
README.ja.md              日本語版 README
llms.txt                  LLM 向け簡易エントリポイント
sources.json              公式ソース一覧
docs/CNS_CORE.md          CNS の実行・Trigger に関する中核不変条件
docs/COMPATIBILITY.md     WinMUGEN と M.U.G.E.N 1.0 の互換性境界
scripts/build_docs.py     取得・正規化・分割・索引生成スクリプト
pyproject.toml            ビルダーの依存関係
```

## 互換性に関する注意

このリポジトリで使用する Elecbyte の CNS ページは **M.U.G.E.N 1.0 documentation (2009)** として公開されています。このリポジトリは WinMUGEN のキャラクターコーディング支援を目的としますが、M.U.G.E.N 1.0 の文書に記載されているという事実だけでは、その機能が旧 WinMUGEN に存在する証明にはなりません。

Agent は `docs/COMPATIBILITY.md` に従い、M.U.G.E.N 1.1 や Ikemen GO の挙動を暗黙に持ち込んではいけません。

## 参照対象ドキュメント

初期コーパスは `sources.json` で定義されており、現在は以下を含みます。

- CNS format
- State Controller Reference
- Trigger Reference
- AIR format

公式ドキュメント本文はベンダーコピーとしてリポジトリへ直接コミットせず、ビルド時に Elecbyte から取得します。
