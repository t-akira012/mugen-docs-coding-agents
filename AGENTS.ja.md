# AGENTS.ja.md

## 目的

このリポジトリは、Elecbyte M.U.G.E.N のキャラクターコーディング仕様を、Coding Agent が機械的に参照できる形へ整備するためのリファレンスコーパスです。
主用途は、WinMUGEN 向けキャラクターの CNS / CMD / AIR コードを Coding Agent で編集することです。

## 情報源の優先順位

1. `sources.json` に列挙された Elecbyte 公式ドキュメント
2. `generated/` 配下の正規化済み生成ドキュメント
3. `docs/` 配下の手書きノート
4. 既存キャラクターコード。これはプロジェクト固有規約の根拠としてのみ扱い、エンジン仕様の証明には使用しない

複数の情報源が矛盾する場合、黙って一方を採用してはいけません。矛盾を明示し、上記で優先順位が高い情報源を優先してください。

## ツール規則: Makefile を操作窓口とし、uv のみ使用

リポジトリ操作は、ルートの `Makefile` を経由して実行します。

- `make run` を標準の全実行コマンドとする。依存関係の同期、全ドキュメントの clean build、生成物の検証まで完了させる。
- 既存の Make target がある処理は、内部コマンドを直接実行せず Make target を使用する。
- 繰り返し使用する新しいリポジトリ操作が必要になった場合は、場当たり的な shell コマンドを文書化せず Make target を追加する。
- Makefile 内での Python 依存関係管理および Python 実行には、必ず `uv` のみを使用する。
- `pip` を使用しない。
- `python -m pip` および `python3 -m pip` を使用しない。
- ドキュメント、スクリプト、CI 設定、Agent 向け指示、Make target に `pip` による依存関係インストール手順を追加しない。
- CI でもローカルと同じ Make target を呼び出し、ビルド処理を重複記述しない。

## 互換性規則

このリポジトリの起点となる公式 CNS ページは M.U.G.E.N 1.0 documentation (2009) です。そこに記載されているすべての機能が、旧 WinMUGEN に存在すると推論してはいけません。

WinMUGEN 厳密互換で作業する場合:

- M.U.G.E.N 1.1 または Ikemen GO の拡張機能を使用しない。
- ある機能を WinMUGEN 互換と扱うのは、適切な情報源または対象キャラクター／対象ランタイムによって互換性が確認できた場合のみとする。
- 確認できない場合は推測せず、互換性を `unverified` とする。

詳細は `docs/COMPATIBILITY.md` を参照してください。

## コーディング規則

- State Controller の順序を維持する。State Controller はソース上の順番で評価されるため、並べ替えによって挙動が変わり得る。
- 同一番号の `triggerN` を維持する。同じ番号の `triggerN` は AND グループを構成し、異なる番号のグループ同士は代替条件になる。
- 意味を理解せず、欠番をまたいで trigger 番号を振り直さない。
- `StateDef`、`ChangeState`、`HitDef`、`AnimElem`、`Time`、`triggerall`、`persistent`、`ignorehitpause` などのエンジン識別子を翻訳しない。
- State Controller のパラメータ、trigger 名、既定値、戻り値を捏造しない。
- コメントと実行可能な CNS 構文を区別する。`;` 以降はコメントである。
- State -3、-2、-1、および現在 State を別々の実行コンテキストとして扱う。
- Helper の実行規則と Root Player の実行規則を分離して扱う。
- 不明な場合は、コードを編集する前に `generated/index.json` から該当する Controller / Trigger セクションを特定する。

## ドキュメント生成手順

ローカル環境の準備、全生成、検証をまとめて実行する場合は、以下のみを実行します。

```bash
make run
```

これを通常の入口とします。Makefile 内で `uv` による依存関係同期、公式ドキュメントコーパスの clean build、生成された index の検証まで完了します。

CNS のみ、主要コア資料のみ、生成物削除などの補助操作も Make target として定義します。直接 Python コマンドを実行せず、`Makefile` を参照してください。

取得元のベンダーテキストそのものは意図的にコミットしません。

特定項目を参照する場合は、まず `generated/index.json` を検索し、その後に対応する Markdown セクションを開いてください。

## キャラクターコード編集手順

Controller または Trigger を変更する前に、以下を行います。

1. 対象となるエンジン構文を正確に特定する。
2. 対応するリファレンス項目を特定する。
3. 必須・任意パラメータと既定値を確認する。
4. 実行コンテキストと Trigger の評価タイミングを確認する。
5. 要求を満たす最小限のコード変更のみを行う。

動作変更と無関係な整形や State Controller の並べ替えを同時に行ってはいけません。
