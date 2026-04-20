# Day1 設定責務棚卸し

## 目的

このドキュメントは、設定まわりの現状の責務配置を確認し、
v1.6 において各要素が本来どこに属するべきかを整理するためのものです。

Day1 の目的は、まだ大きくコードを移動することではありません。

まずは、

- いま何がどこにあるか
- 何が混在しているか
- 本来どこに置くべきか
- v1.6 のどこで分離するか

を見える化することを目的とします。

---

## 責務カテゴリ

棚卸しでは、各要素を以下のカテゴリで分類します。

- secrets
- developer defaults
- runtime source of truth
- registry
- legacy compatibility
- helper / derived / glue

必要であれば Day1 の作業中に補助カテゴリを追加してもよいですが、
基本はこの6分類を基準とします。

---

## 対象ファイル

Day1 の主対象:

- `config/settings.py`
- `config/models.py`

参照対象:

- `config/loader.py`
- `core/runtime.py`
- `llm/builder.py`
- `tts/voice_engine.py`
- `stt/stt_engine.py`

---

## 各カテゴリの意味

### secrets

APIキーなど、環境変数や秘密情報に属するもの。

想定配置先:

- `config/secrets.py`

### developer defaults

開発者向けの既定値や初期選択値。

例:

- `SELECT_*`
- 開発時の既定 provider / model / voice index
- debug 用の既定挙動

想定配置先:

- `config/defaults.py`

### runtime source of truth

実行時の挙動を最終的に支配する値。  
本来は `RuntimeConfig` に集約されるべきもの。

想定配置先:

- `RuntimeConfig`
- `config/loader.py` による組み立て経路

### registry

LLM / TTS / provider の定義表、ルーティング定義、メタデータ表など。  
設定値というより「定義テーブル」に近いもの。

想定配置先:

- `registry/llm.py`
- `registry/tts.py`
- 必要に応じて追加される registry モジュール

### legacy compatibility

旧グローバルフラグ、別名互換、古い経路との互換のために残っているもの。

想定配置先:

- `config/legacy.py`

### helper / derived / glue

組み立て補助、変換補助、派生値、一時的なつなぎの責務。  
正本ではなく、読み込みや変換の過程で使うもの。

想定配置先:

- `config/loader.py`
- runtime helper 層
- 必要に応じた小さな utility モジュール

---

## 棚卸し表

| 項目 | 現在の場所 | 現在の役割 | 混在/問題点 | 責務カテゴリ | 本来の配置先 | v1.6での対応 |
|------|------------|------------|--------------|--------------|--------------|---------------|
| 例: `GOOGLE_API_KEY` | `config/settings.py` | 外部APIキーの読み込み | secrets が settings に混在 | secrets | `config/secrets.py` | 後日分離 |
| 例: `SELECT_VOICE_INDEX` | `config/settings.py` | 開発用の既定選択 | defaults が runtime/config と混在 | developer defaults | `config/defaults.py` | 後日分離 |
| 例: `LLM_CATALOG` | `config/settings.py` | LLM定義表 | registry が settings に混在 | registry | `registry/llm.py` | 後日分離 |
| 例: `TTS_MODEL_MASTER` | `config/models.py` | TTSモデル定義表 | registry が models に混在 | registry | `registry/tts.py` | 後日分離 |

---

## settings.py 棚卸し

### secrets 候補

- 

### developer defaults 候補

- 

### runtime source of truth 候補

- 

### registry 候補

- 

### legacy compatibility 候補

- 

### helper / derived / glue 候補

- 

---

## models.py 棚卸し

### registry 候補

- 

### developer defaults 候補

- 

### secrets / env連動 候補

- 

### legacy compatibility 候補

- 

### helper / derived / glue 候補

- 

---

## 整理後に目指す境界

### `config/settings.py`
責務混在ファイルのまま残さない。  
少なくとも、secrets / defaults / registry / legacy を全部抱える場所ではなくす。

### `config/models.py`
provider / model の定義表と、env連動の voice 設定責務を分離する。

### `RuntimeConfig`
実行時挙動の正本として扱う。

### `config/loader.py`
分離された source から `RuntimeConfig` を組み立てる責務に寄せる。

---

## Day1 で先に決めること

### 先に分けやすいもの

- 明らかな secrets
- 明らかな developer defaults
- 明らかな registry 定義表

### 慎重に扱うもの

- 複数モジュールから参照されている旧フラグ
- config と derived value の境界が曖昧なもの
- 言語設定のように複数レイヤーへ影響するもの

### Day1 では無理にやらないこと

- 大規模 rewrite
- 広範囲 rename
- 挙動変更を伴う整理

---

## Day1 の完了条件

Day1 は、以下を満たせば完了とする。

- 現状の責務混在が見える化されている
- 各主要項目に「本来の責務」と「本来の配置先」が付いている
- Day2 以降の分離対象が明確になっている
- まだ挙動変更を伴う移動は行っていない

---

## 推奨コミット

```bash
git commit -m "docs(config): define configuration responsibility boundaries"
```
