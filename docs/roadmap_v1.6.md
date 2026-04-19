# roadmap_v1.6

## Version Theme

**v1.6.0: Configuration Responsibility Cleanup / Developer Experience Foundation**

v1.6では、v1.5で完成した Emotion / VTS の主経路を土台にして、
Framework全体の設定責務と構成を整理する。

v1.5で確認できた主経路:

```text
User input
-> LLM raw response
-> parse_emotion_response()
-> emotion + clean_text
-> display clean_text
-> TTS clean_text
-> resolve_emotion_hotkey()
-> VTS trigger_hotkey()
```

この主経路自体は v1.5 で成立したため、v1.6 では新機能の大量追加よりも、
以下を優先する。

- settings.py / models.py の責務整理
- RuntimeConfig を source of truth とする構成の明確化
- preset / character / runtime / registry の境界整理
- developer-facing configuration の見通し改善
- plugin / hook の扱いやすさ向上

v1.6は、**Frameworkとして長く育てやすい構成へ寄せるバージョン** とする。

---

## Goal

- RuntimeConfig を runtime behavior の正本として扱う
- settings.py の神ファイル化を防ぐ
- models.py の registry責務を明確化する
- secrets / developer defaults / runtime config / legacy compatibility を切り分ける
- preset / character / runtime / provider registry の責務境界を整理する
- plugin / hook を追加しやすい形に整える
- README / docs で開発者向け設定フローを明確化する

---

## Current Problem Statement

v1.5時点では機能は動いているが、設定責務が一部混在している。

主な混在ポイント:

- settings.py に secrets / defaults / route / legacy / derived values が混在
- models.py に registry と env由来の voice 情報が混在
- preset と settings の意味が開発者視点で分かりづらい箇所がある
- tts_provider の表示名と実装実態にズレがある
- old global flags が一部 legacy として残っている
- plugin / hook は動くが、拡張規約としてはまだ最小構成

v1.6では、これらを**壊さず段階的に整理**する。

---

## Design Principles

- RuntimeConfig を runtime behavior の source of truth とする
- preset は「起動モード」の責務に限定する
- character は「キャラ固有差分」の責務に限定する
- provider/model registry は settings.py から分離する
- secrets は env-based config に寄せる
- legacy compatibility は main flow から分離する
- plugin / hook の整理は小さく進める
- 動いている主経路は壊さない
- v1.6でも text_chat を安全な開発デフォルトとする
- 1日1責務 / 1日1コミットを維持する

---

## Responsibility Target Model

v1.6で目指す責務の分離:

```text
config/
  runtime_config.py     -> RuntimeConfig definition
  loader.py             -> preset / character / defaults から RuntimeConfig を組み立てる
  secrets.py            -> API key / env secrets
  defaults.py           -> developer-facing default selections
  legacy.py             -> old flags / alias compatibility

registry/
  llm.py                -> LLM model registry
  tts.py                -> TTS model registry
  providers.py          -> provider capability / metadata (必要なら)

presets/
  *.json                -> 起動モード定義

characters/
  */profile.json
  */system.txt
  */vts_hotkeys.json    -> キャラ固有差分

core/
  pipeline.py           -> parse + routing of response output
  emotion.py            -> emotion logic
```

これは v1.6 の目標構成であり、
v1.6の中では「完全移行」ではなく「安全な分離開始」まででよい。

---

## v1.6 Must

- RuntimeConfig を runtime behavior の正本として明文化
- settings.py の責務を comments / docs だけでなく構成上も整理開始
- LLM registry を独立化
- TTS registry を独立化
- secrets 読み込み層を分離
- developer defaults を分離
- legacy flags / alias の配置を整理
- README に developer configuration flow を追加
- docs に v1.6 architecture note を追加
- 既存 preset が壊れていないことを確認

---

## Daily Plan

### Day 0: v1.5.0 release snapshot and safety baseline

目的:

v1.6 作業前に、v1.5.0 の安定状態を固定する。

作業:

- v1.5.0 tag / main の状態を確認
- README / roadmap / release zip の最終状態を記録
- known issue を整理
- v1.6 で触らない主経路を明文化

終了条件:

```text
v1.5.0 の安定主経路と known issue が明文化されている
```

コミット例:

```bash
git commit -m "docs: record v1.5.0 baseline for v1.6"
```

---

### Day 1: define configuration responsibility boundaries

目的:

どの設定がどこに属するかを先に決める。

作業:

- settings.py 内の要素を分類
  - secrets
  - developer defaults
  - registry
  - legacy
  - runtime-derived
- models.py 内の要素を分類
- docs に責務表を追加
- RuntimeConfig を source of truth と明文化

終了条件:

```text
settings/models の責務境界が一覧化されている
```

コミット例:

```bash
git commit -m "docs(config): define configuration responsibility boundaries"
```

---

### Day 2: extract LLM registry

目的:

LLM 定義を settings.py から外へ出す。

作業:

- registry/llm.py を追加
- LLM_CATALOG を移動
- LLM_ROUTES を必要に応じて routing 側へ整理
- import path を修正
- 既存挙動確認

終了条件:

```text
LLM registry が settings.py から分離されている
```

コミット例:

```bash
git commit -m "refactor(config): extract llm registry"
```

---

### Day 3: extract TTS registry

目的:

TTS model 定義を settings.py / models.py から整理する。

作業:

- registry/tts.py を追加
- TTS_MODEL_MASTER を移動
- tts provider の表記と実装実態を整理
- import path を修正
- 既存挙動確認

終了条件:

```text
TTS registry が独立し、settings/models の責務が軽くなる
```

コミット例:

```bash
git commit -m "refactor(config): extract tts registry"
```

---

### Day 4: separate secrets from developer defaults

目的:

env secrets と開発者向け既定値を分離する。

作業:

- config/secrets.py を追加
- config/defaults.py を追加
- API key 読み込みを移動
- SELECT_VOICE_INDEX などを defaults 側へ整理
- 既存初期化確認

終了条件:

```text
secrets と developer defaults が settings.py から分かれている
```

コミット例:

```bash
git commit -m "refactor(config): separate secrets and defaults"
```

---

### Day 5: isolate legacy compatibility

目的:

old global flags と alias を main flow から切り離す。

作業:

- legacy flags / alias に明示コメント追加
- 必要なら config/legacy.py を追加
- change_expression() などの互換経路を整理
- README / docs に legacy path を明記

終了条件:

```text
legacy compatibility が main flow と区別されている
```

コミット例:

```bash
git commit -m "refactor(config): isolate legacy compatibility"
```

---

### Day 6: simplify runtime loader flow

目的:

loader / runtime の設定組み立てを見通しよくする。

作業:

- loader の読み込み順を整理
- preset -> character -> defaults -> RuntimeConfig の流れを明確化
- derived value の位置を見直す
- RuntimeConfig 表示内容を見直す

終了条件:

```text
runtime initialization flow が読みやすく整理されている
```

コミット例:

```bash
git commit -m "refactor(runtime): simplify config loading flow"
```

---

### Day 7: clarify preset behavior and naming

目的:

preset の意味が README なしでも分かる状態にする。

作業:

- preset の説明文を整理
- tts_provider の命名見直し
- text_chat を safe default として明示
- text_vts / voice_vts の目的を再確認
- bilingual_ja_en の役割を明確化

終了条件:

```text
preset の役割と命名が分かりやすくなる
```

コミット例:

```bash
git commit -m "refactor(presets): clarify preset behavior and naming"
```

---

### Day 8: plugin / hook contract cleanup

目的:

plugin を追加しやすい形に整理する。

作業:

- hook 一覧を docs 化
- plugin setup / event contract を整理
- EmotionVTSPlugin をサンプル実装として整える
- 新規 plugin 追加手順を明文化

終了条件:

```text
plugin / hook contract が docs 付きで理解しやすい
```

コミット例:

```bash
git commit -m "docs(plugin): clarify plugin and hook contracts"
```

---

### Day 9: developer configuration guide

目的:

開発者がどこを触ればよいか迷わない状態にする。

作業:

- README に configuration flow を追加
- docs/developer_configuration.md を追加
- preset / character / registry / defaults / secrets の関係を整理
- examples を追加

終了条件:

```text
開発者向け設定フローが README / docs にまとまっている
```

コミット例:

```bash
git commit -m "docs: add developer configuration guide"
```

---

### Day 10: verify behavior after reallocation

目的:

設定再配分後に既存動作が壊れていないか確認する。

作業:

- text_chat
- text_vts
- voice_vts
- bilingual_ja_en
- emotion / VTS / TTS / language control の再確認

終了条件:

```text
既存 preset の主要挙動が維持されている
```

コミット例:

```bash
git commit -m "test(config): verify behavior after config cleanup"
```

---

### Day 11: cleanup and consistency pass

目的:

不要コードや表記のズレを減らす。

作業:

- 不要 import 整理
- debug log 見直し
- settings / registry / docs の表記統一
- known issue 更新

終了条件:

```text
v1.6 時点の構成と表記が概ね揃っている
```

コミット例:

```bash
git commit -m "chore: cleanup config and docs consistency"
```

---

### Day 12: release check for v1.6.0

目的:

v1.6.0 として一区切り付ける。

作業:

- preset 最終確認
- README / docs 最終確認
- known issue 記載確認
- zip 用不要ファイル確認
- release commit
- tag

終了条件:

```text
v1.6.0 として配布できる状態になっている
```

コミット例:

```bash
git commit -m "chore: prepare v1.6.0 release"
git tag v1.6.0
```

---

## Non-goals

v1.6では以下をやらない。

- GUI launcher の本格実装
- local LLM の本格対応
- plugin system の全面再設計
- memory / affection / long-term state system
- 高度な streaming renderer
- advanced motion control
- character editor UI
- 配信向け overlay / OBS integration の本格実装

---

## Operating Rules

- 1日1時間
- 1日1責務まで
- 1日1コミット
- 主経路を壊さない
- 先に責務を言語化してから移動する
- 大きく分ける前に小さく安全に分ける
- text_chat を safe default とする
- 既知軽微事項は release blocker にしない
- 迷ったら RuntimeConfig を source of truth として判断する

---

## Known Issues at v1.5.0 Baseline

- 長文時に TTS wait warning が出ることがある
- tts_provider 表示名と実装実態にズレがある
- voice_vts の入力 UX は今後さらに改善余地がある

---

## Recommended Schedule

```text
Day 0  baseline / known issue 整理
Day 1  責務境界定義
Day 2  LLM registry 分離
Day 3  TTS registry 分離
Day 4  secrets / defaults 分離
Day 5  legacy compatibility 整理
Day 6  loader / runtime flow 整理
Day 7  preset 命名と役割整理
Day 8  plugin / hook contract 整理
Day 9  developer configuration guide
Day 10 preset 再検証
Day 11 cleanup / consistency
Day 12 release check / v1.6.0
```
