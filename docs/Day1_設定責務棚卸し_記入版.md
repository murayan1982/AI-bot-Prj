# Day1 設定責務棚卸し（記入版）

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
| `GOOGLE_API_KEY` | `config/settings.py` | 外部APIキーの読み込み | secrets が settings に混在 | secrets | `config/secrets.py` | 後日分離 |
| `XAI_API_KEY` | `config/settings.py` | 外部APIキーの読み込み | secrets が settings に混在 | secrets | `config/secrets.py` | 後日分離 |
| `ELEVENLABS_API_KEY` | `config/settings.py` | 外部APIキーの読み込み | secrets が settings に混在 | secrets | `config/secrets.py` | 後日分離 |
| `SELECT_VOICE_INDEX` | `config/settings.py` | 開発用の既定選択 | defaults が runtime/config と混在 | developer defaults | `config/defaults.py` | 後日分離 |
| `SELECT_TTS_MODEL_INDEX` | `config/settings.py` | 開発用の既定選択 | defaults が runtime/config と混在 | developer defaults | `config/defaults.py` | 後日分離 |
| `LLM_CATALOG` | `config/settings.py` | LLM定義表 | registry が settings に混在 | registry | `registry/llm.py` | Day2候補 |
| `LLM_ROUTES` | `config/settings.py` | ルーティング定義 | registry / routing定義が settings に混在 | registry | `registry/llm.py` もしくは routing設定層 | Day2候補 |
| `TTS_MODEL_MASTER` | `config/models.py` | TTSモデル定義表 | registry が models に混在 | registry | `registry/tts.py` | Day3候補 |
| `VOICE_MASTER` | `config/models.py` | env由来の音声設定読込 | registry と env設定が混在 | helper / derived / glue | env読込層 / `config/secrets.py` 相当 | 後日分離 |
| `MODEL_MASTER` | `config/models.py` | LLM/TTS/voice を束ねた統合辞書 | registry と env設定を無理に一箇所へ集約 | helper / derived / glue | 廃止または責務分離後に再設計 | 慎重に扱う |
| `VOICE_ID` | `config/settings.py` | voice 選択結果 | defaults + env値 + registry 的情報の混合結果 | helper / derived / glue | loader / builder / engine初期化層 | 慎重に扱う |
| `TTS_MODEL_ID` | `config/settings.py` | TTS model 選択結果 | defaults + registry の混合結果 | helper / derived / glue | loader / builder / engine初期化層 | 慎重に扱う |

---

## settings.py 棚卸し

### secrets 候補

- `GOOGLE_API_KEY`
- `XAI_API_KEY`
- `ELEVENLABS_API_KEY`

### developer defaults 候補

- `DEBUG_MASTER`
- `DEBUG`
- `DEBUG_ROUTER`
- `DEBUG_FALLBACK`
- `DEBUG_VTS`
- `DEBUG_TTS`
- `DEBUG_STT`
- `SELECT_VOICE_INDEX`
- `SELECT_TTS_MODEL_INDEX`

### runtime source of truth 候補

- 現時点では多くが `RuntimeConfig` の正本ではなく、
  本来は loader 経由で `RuntimeConfig` に寄せるべき候補として存在している
- `LANGUAGE_CODE` は旧グローバル設定として残っているが、
  将来的には preset / RuntimeConfig 側へ吸収したい

### registry 候補

- `LLM_CATALOG`
- `LLM_ROUTES`
- `STRONG_CODE_KEYWORDS`
- `WEAK_CODE_KEYWORDS`
- `LANG_MAP`
- `SAFETY_SETTINGS`

### legacy compatibility 候補

- `VTS_DEBUG`
- `INPUT_VOICE_ENABLED`
- `OUTPUT_VOICE_ENABLED`
- `ENABLE_VTS`
- `STT_ENGINE`
- `TTS_ENGINE`
- `VTS_EMOTION_ALIAS`
- `LANGUAGE_CODE`（暫定的に legacy 寄り）

### helper / derived / glue 候補

- `VOICE_MASTER = MODEL_MASTER.get("voices", [])`
- `TTS_MODEL_MASTER = MODEL_MASTER.get("tts_models", [])`
- `STT_LANGUAGE = LANGUAGE_CODE`
- `TARGET_LANGUAGE = LANG_MAP.get(LANGUAGE_CODE, "English")`
- `VTS_TOKEN_PATH`
- `DEFAULT_EMOTION`
- `VOICE_ID`
- `TTS_MODEL_ID`

---

## models.py 棚卸し

### registry 候補

- `GOOGLE_MODELS`
- `XAI_MODELS`
- `OPENAI_MODELS`
- `TTS_MODEL_MASTER`

### developer defaults 候補

- 現時点では該当なし

### secrets / env連動 候補

- `raw_voice_master = os.getenv("VOICE_MASTER", "[]")`
- `VOICE_MASTER = json.loads(raw_voice_master)`

### legacy compatibility 候補

- 現時点では明確な legacy 本体は少ない
- ただし `MODEL_MASTER` を前提にした古い参照経路が残っている場合は
  間接的に互換責務を持っている可能性がある

### helper / derived / glue 候補

- `MODEL_MASTER`
- `MODEL_MASTER["voices"] = VOICE_MASTER` のような統合構造

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

## Day1 で見えた整理方針

### 先に分けやすいもの

- 明らかな secrets
- 明らかな developer defaults
- `LLM_CATALOG`
- `LLM_ROUTES`
- `GOOGLE_MODELS`
- `XAI_MODELS`
- `OPENAI_MODELS`
- `TTS_MODEL_MASTER`

### 慎重に扱うもの

- `LANGUAGE_CODE`
- `LANG_MAP`
- `SAFETY_SETTINGS`
- `STT_ENGINE`
- `TTS_ENGINE`
- `VOICE_ID`
- `TTS_MODEL_ID`
- `MODEL_MASTER`

### 明確に legacy 扱いでよさそうなもの

- `VTS_DEBUG`
- `INPUT_VOICE_ENABLED`
- `OUTPUT_VOICE_ENABLED`
- `ENABLE_VTS`
- `VTS_EMOTION_ALIAS`

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
