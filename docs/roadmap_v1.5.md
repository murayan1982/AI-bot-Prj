# roadmap_v1.5

## Version Theme

**v1.5.0: Emotion / VTS Expression Control**

v1.5では、v1.4で作った `preset / character / RuntimeConfig / plugin / VTS接続` の土台の上に、AI応答のemotion tagとLive2D / VTube Studioの表情制御を追加する。

v2.0全体ロードマップ上では一時的に v1.5 = Multi-LLM Base としていたが、v1.4.0時点でGemini / Grok / router / fallbackの基本構造はすでに存在するため、v1.5.0ではAIキャラクター体験の価値が直接上がるEmotion / VTS制御を優先する。

Multi-LLM Baseの本格整理は、v1.6以降へ移動する。

## v1.5 Scope Clarification

v1.5では、Emotion / VTS Expression Control を主目的とする。

実装を進める中で、`settings.py / models.py / RuntimeConfig / preset / character` の責務境界がやや見えにくくなってきたため、v1.5後半では以下の方針で安全な整理を進める。

- `RuntimeConfig` を runtime behavior の source of truth とする
- `preset` は起動モード切替に責務を限定する
- `character` はキャラ固有差分に責務を限定する
- `settings.py` は暫定的に secrets / developer defaults / legacy compatibility を持つ
- `models.py` は provider / model registry 候補として扱う
- `settings.py / models.py` の本格再配分は v1.6 以降へ送る

v1.5では、emotion / VTS の主経路を完成させた上で、責務の線引きと安全な整理までを対象とする。

---

## Goal

- LLM応答にemotion tagを付与する
- emotion tagを本文から分離する
- ユーザー表示 / TTS用テキストからemotion tagを除去する
- characterごとのVTS hotkey mappingを読む
- emotion keyからVTS hotkey名を解決する
- VTube Studioへhotkey triggerを送る
- VTS未接続 / hotkey未設定 / 不正emotionでも会話を継続する
- emotion処理を最終的にplugin経由で扱えるようにする

最終状態:

```text
[emotion:happy]
こんにちは！会えてうれしいです。
```

上記のようなLLM応答から、Frameworkは `happy` を取り出し、表示/TTSには `こんにちは！会えてうれしいです。` だけを渡す。VTSが有効で、character側に `happy -> Smile` のようなmappingがあれば、VTube Studioへ `Smile` hotkeyを送る。

---

## Relation to v1.4.0

v1.4.0で完了済み、または前提とする基盤:

- `RuntimeConfig`
- `presets/*.json`
- `characters/default/profile.json`
- `characters/default/system.txt`
- input / output language separation
- runtimeへのconfig注入
- feature flagによる STT / TTS / VTS 切替
- TTS provider切替
- LLM output language instruction
- `plugins/base.py`
- `plugins/manager.py`
- `plugins/builtin/console_logger.py`
- `text_chat / text_vts / voice_vts` 起動bat
- VTS接続ON/OFF

v1.4.0時点のLive2D / VTS連携は、接続確認とpresetによるON/OFF切替までを対象とする。

v1.5.0では、その上に以下を追加する:

- emotion tag generation
- emotion parser
- character-level VTS hotkey mapping
- VTS hotkey trigger
- plugin-based emotion handling
- safe fallback

---

## Design Principles

- Framework側ではVTS hotkey名を固定しない
- Frameworkは抽象的なemotion keyのみ扱う
- 実際のhotkey名はcharacterごとの設定で解決する
- emotion tagはユーザー表示 / TTSから必ず除去する
- VTS制御に失敗しても会話は継続する
- まずruntime直結MVPで動かし、後からpluginへ移す
- text_vtsで先に確認し、voice_vtsは後で確認する
- 1日1時間 / 1日1責務 / 1日1コミットで進める
- RuntimeConfig を runtime behavior の source of truth とする
- Framework側は emotion key まで責任を持ち、VTS hotkey名は character 側で解決する
- settings.py に残る旧global flagや alias は legacy compatibility として扱う
- settings/models の整理は、主経路を壊さない安全な範囲に限定する

---

## Standard Emotion Keys

Framework標準emotion key:

```text
neutral
happy
sad
angry
surprised
confused
```

不正なemotion、未対応emotion、tagなしの場合は `neutral` として扱う。

---

## LLM Output Format

LLMには、応答冒頭にemotion tagを1つだけ出させる。

```text
[emotion:happy]
こんにちは！会えてうれしいです。
```

ルール:

- tagは応答冒頭に1つだけ
- 許可されたemotion keyのみ使う
- 複数emotionは扱わない
- tagの後に通常本文を書く

---

## Parser Result Design

`parse_emotion_response()` は最低限以下を返す。

```text
emotion
clean_text
raw_text
```

例:

```text
raw_text:
[emotion:happy]
こんにちは！会えてうれしいです。

emotion:
happy

clean_text:
こんにちは！会えてうれしいです。
```

実装候補:

```python
@dataclass
class EmotionResult:
    emotion: str
    clean_text: str
    raw_text: str
```

---

## Config Design

preset側でemotion機能のON/OFFを持つ。

```json
{
  "emotion_enabled": true,
  "vts_emotion_enabled": true
}
```

### emotion_enabled

`true` の場合:

- LLMにemotion tag instructionを追加する
- LLM応答からemotion tagを解析する
- 表示 / TTSからemotion tagを除去する

`false` の場合:

- emotion tag instructionを追加しない
- 原則emotion処理を行わない
- ただし安全のため、tagが混ざった場合の除去処理は残してもよい

### vts_emotion_enabled

`true` の場合:

- 解析したemotionをVTS hotkey triggerへ接続する

`false` の場合:

- emotionを解析してもVTS操作は行わない

### dependency

`emotion_enabled=false` の場合、`vts_emotion_enabled=true` でもVTS emotion制御は動かない。

---

## Character Hotkey Mapping

characterごとにVTS hotkey mappingを持つ。

例:

`characters/default/vts_hotkeys.json`

```json
{
  "neutral": null,
  "happy": "Smile",
  "sad": "Sad",
  "angry": "Angry",
  "surprised": "Surprised",
  "confused": null
}
```

ルール:

- hotkey名はpresetではなくcharacter側で定義する
- mapping値が `null` の場合は何もしない
- 未定義emotionは `neutral` として扱う
- VTube Studio側に存在しないhotkey名だった場合も会話は継続する

---

## Target Files

主な変更対象:

```text
core/emotion.py
core/runtime.py
core/pipeline.py
config/loader.py
config/settings.py または RuntimeConfig定義ファイル
characters/default/vts_hotkeys.json
live2d/vts_client.py
plugins/builtin/emotion_vts.py
plugins/builtin/__init__.py
presets/*.json
README.md
docs/roadmap_v1.5.md
```

---

## v1.5 Must

- emotion tag format追加
- emotion_enabled / vts_emotion_enabled 追加
- LLM runtime instructionにemotion出力ルールを追加
- `core/emotion.py` 追加
- `parse_emotion_response()` 追加
- 表示 / TTS用テキストからemotion tag除去
- `characters/default/vts_hotkeys.json` 追加
- loaderでVTS hotkey mappingを読む
- `RuntimeConfig` からhotkey mappingにアクセス可能にする
- `VTSClient.trigger_hotkey()` 追加
- emotion keyからcharacter hotkeyを解決
- VTS未接続 / hotkey未設定 / 不正emotion時のfallback
- presetによるemotion機能ON/OFF
- `plugins/builtin/emotion_vts.py` 追加
- README更新
- text_vts / voice_vts実機確認
- 主経路（LLM response -> parse_emotion_response -> clean_text / resolve_emotion_hotkey -> trigger_hotkey）を明文化
- legacy path（change_expression / VTS_EMOTION_ALIAS / old global flags）を明示
- settings/models 再配分方針をメモ化

---

## Daily Plan

### Day 0: v1.4.0 release consistency cleanup

目的:

v1.5実装に入る前に、v1.4.0リリースzipとドキュメントのズレを減らす。

作業:

- READMEの `Features (v1.3.0)` 表記を `Features (v1.4.0)` に更新
- Runtime Configuration説明を `APP_PRESET + presets/*.json` 中心に修正
- v2.0ロードマップ側の v1.5 = Multi-LLM Base とのズレをメモする
- v1.5.0はEmotion / VTS Expression Controlとして進める方針を明記

終了条件:

```text
READMEとroadmapがv1.4.0 zipの実装状態と大きく矛盾していない
```

コミット例:

```bash
git commit -m "docs: align README and roadmap for v1.4.0 release"
```

---

### Day 1: add emotion feature flags

目的:

presetでemotion機能をON/OFFできる入口を作る。

作業:

- `RuntimeConfig` に `emotion_enabled: bool = False` を追加
- `RuntimeConfig` に `vts_emotion_enabled: bool = False` を追加
- `config/loader.py` でpresetから読み込む
- `presets/text_chat.json` では原則無効
- `presets/text_vts.json` では有効
- `presets/voice_vts.json` では有効
- 起動時のconfig表示に追加

終了条件:

```text
起動時のRuntimeConfig表示に emotion_enabled / vts_emotion_enabled が出る
```

コミット例:

```bash
git commit -m "feat(config): add emotion feature flags"
```

---

### Day 2: add emotion instruction to runtime

目的:

LLMに `[emotion:xxx]` を出させる。

作業:

- `core/runtime.py` のsystem instruction生成部分にemotion instructionを追加
- `emotion_enabled=True` のときだけ追加
- 許可emotion keyを明記
- tagは応答冒頭に1個だけ、というルールにする

instruction候補:

```text
At the beginning of every assistant response, output exactly one emotion tag:
[emotion:neutral], [emotion:happy], [emotion:sad], [emotion:angry], [emotion:surprised], or [emotion:confused].
After the tag, write the normal response text.
Do not output multiple emotion tags.
```

終了条件:

```text
text_vtsでAI応答の先頭に [emotion:happy] などが付く
```

コミット例:

```bash
git commit -m "feat(runtime): add emotion tag instruction"
```

---

### Day 3: add core emotion parser

目的:

emotion tag解析をLLM engineから分離する。

作業:

- `core/emotion.py` を追加
- `EmotionResult` dataclassを作る
- `parse_emotion_response(raw_text: str)` を作る
- `[emotion:happy]` 形式を検出する
- 不正値は `neutral` にする
- tagなしも `neutral` にする
- `clean_text` からtagを除去する

終了条件:

```text
parse_emotion_response("[emotion:happy]\nこんにちは") で emotion=happy / clean_text=こんにちは が取れる
```

コミット例:

```bash
git commit -m "feat(core): add emotion response parser"
```

---

### Day 4: strip emotion tag from display and TTS

目的:

ユーザー表示と読み上げにemotion tagが混ざらないようにする。

作業:

- `core/pipeline.py` で `parse_emotion_response()` を使う
- 表示には `clean_text` を使う
- TTSにも `clean_text` を渡す
- 既存の簡易tag除去処理があれば整理する
- streaming中の完全対応はv1.7寄りなので、v1.5では先頭tag除去のMVPを優先する

終了条件:

```text
AI内部応答に [emotion:xxx] があっても、画面表示とTTSには出ない
```

コミット例:

```bash
git commit -m "feat(pipeline): strip emotion tags from display and tts"
```

---

### Day 5: load character VTS hotkey mapping

目的:

Framework側からhotkey名を固定しない構造にする。

作業:

- `characters/default/vts_hotkeys.json` を作る
- `config/loader.py` で読み込む
- `RuntimeConfig.vts_hotkeys` に入れる
- ファイルがない場合は空dictで継続
- JSON不正時は安全にfallbackする

終了条件:

```text
runtimeから config.vts_hotkeys["happy"] にアクセスできる
```

コミット例:

```bash
git commit -m "feat(character): load vts hotkey mapping"
```

---

### Day 6: add VTS hotkey trigger method

目的:

emotionではなく、hotkey名を直接送れるメソッドを作る。

作業:

- `live2d/vts_client.py` に `trigger_hotkey(hotkey_name: str)` を追加
- VTube Studio APIのhotkey一覧から対象hotkeyを探す
- 見つかったらtriggerする
- 見つからない場合は落とさない
- 未接続時も落とさない
- 失敗時はdebug log中心にする

終了条件:

```text
await vts.trigger_hotkey("Smile") でVTS hotkeyが発火できる
未接続 / 未設定でも会話が落ちない
```

コミット例:

```bash
git commit -m "feat(vts): add safe hotkey trigger method"
```

---

### Day 7: resolve emotion key to character hotkey

目的:

`[emotion:happy]` からcharacter側の `Smile` などに変換する。

作業:

- `core/emotion.py` に `resolve_emotion_hotkey()` を追加
- emotionが未定義なら `neutral`
- mappingが `null` なら何もしない
- Framework側では `Smile` などのhotkey名を固定しない

終了条件:

```text
happy -> Smile
confused -> None
unknown -> neutral mapping
```

コミット例:

```bash
git commit -m "feat(core): resolve emotion to character hotkey"
```

---

### Day 8: connect emotion to VTS in runtime MVP

目的:

plugin化前に、まずruntime直結で動くMVPを作る。

作業:

- `core/pipeline.py` でemotion検出後にVTS制御を呼ぶ
- `emotion_enabled` と `vts_emotion_enabled` を確認
- `runtime["vts"]` または該当するVTS client参照を確認
- hotkeyがあれば `trigger_hotkey()` を呼ぶ
- hotkey未設定なら何もしない

終了条件:

```text
text_vtsで [emotion:happy] を受けたときに、対応hotkeyが呼ばれる
```

コミット例:

```bash
git commit -m "feat(pipeline): trigger vts hotkey from emotion"
```

---

### Day 9: organize fallback and logs

目的:

VTS未起動やhotkey未設定でも、通常会話として成立させる。

作業:

- VTS未接続時は無言スキップ、またはdebug logのみ
- hotkey未設定時も無言スキップ、またはdebug logのみ
- emotion不正値は `neutral`
- `VTS_DEBUG=False` では詳細ログを出しすぎない
- エラー表示でユーザー体験を壊さない

終了条件:

```text
VTS未起動でも text_vts が通常チャットとして継続する
hotkey未設定でもエラーにならない
```

コミット例:

```bash
git commit -m "fix(emotion): make vts emotion fallback safe"
```

## Current Progress (as of Day 9)

完了済み:

- Day 0: v1.4.0 release consistency cleanup
- Day 1: emotion feature flags 追加
- Day 2: runtime instruction に emotion tag 出力ルール追加
- Day 3: core emotion parser 追加
- Day 4: 表示 / TTS から emotion tag 除去
- Day 5: character VTS hotkey mapping 読み込み
- Day 6: safe hotkey trigger 追加
- Day 7: emotion key -> character hotkey 解決追加
- Day 8: pipeline から emotion -> VTS hotkey を接続
- Day 9: fallback / logs / legacy path の安全整理

現時点の主経路:

User input
-> LLM raw response
-> parse_emotion_response()
-> emotion + clean_text
-> display clean_text
-> TTS clean_text
-> resolve_emotion_hotkey()
-> VTS trigger_hotkey()

現時点の legacy path:

- change_expression()
- VTS_EMOTION_ALIAS
- old global flags in settings.py

メモ:

- emotion / VTS の主経路は runtime直結MVPとして成立した
- plugin化は Day 10 以降で行う
- settings/models の本格再配分は v1.6 以降へ送る
- v1.5では責務の線引きと安全な整理までを対象とする


---

### Day 10: move emotion VTS handling to plugin

目的:

runtime直結MVPをbuiltin plugin側へ移す。

作業:

- `plugins/builtin/emotion_vts.py` を追加
- `EmotionVTSPlugin` を作る
- runtime / config / vts clientへアクセスできる形にする
- Day 8までのVTS emotion処理をplugin側へ寄せる
- `plugins/builtin/__init__.py` に追加
- plugin登録処理を整理する

注意:

この日にplugin hook設計を大改造しない。v1.5では builtin plugin として動けばよい。

また、この日に settings.py / models.py の本格再配分は行わない。まずは主経路を plugin へ寄せることを優先する。

終了条件:

```text
emotion VTS制御が plugins/builtin/emotion_vts.py 経由で動く
```

コミット例:

```bash
git commit -m "feat(plugin): add emotion vts plugin"
```

---

### Day 11: verify preset behavior

目的:

presetごとにemotion機能のON/OFFが切り替わることを確認する。

作業:

- `text_chat` 確認
  - emotion tag instructionが入らない
  - tagが混ざっても表示に出ないならなおよい
- `text_vts` 確認
  - emotion tagあり
  - VTS hotkey発火
- `voice_vts` 確認
  - emotion tagが音声に混ざらない
- `bilingual_ja_en` 確認
  - 言語制御が壊れていない

終了条件:

```text
presetごとに emotion_enabled / vts_emotion_enabled の切替が効く
```

コミット例:

```bash
git commit -m "test(presets): verify emotion feature flags"
```

---

### Day 12: verify text_vts with VTube Studio

目的:

軽い構成でVTS表情制御を完成させる。

作業:

- VTube Studio起動
- `text_vts` 起動
- happy / sad / surprised が出そうな入力を試す
- 対応hotkeyが動くか確認
- VTSを落とした状態でも起動確認

終了条件:

```text
text_vtsでemotion表情制御が動く
VTS未起動でも会話が落ちない
```

コミット例:

```bash
git commit -m "test(vts): verify emotion control in text_vts"
```

---

### Day 13: verify voice_vts flow

目的:

STT / LLM / TTS / VTS の一連の流れで破綻しないか確認する。

作業:

- `voice_vts` 起動
- STT入力
- LLM応答
- TTS読み上げ
- VTS hotkey発火
- emotion tagが音声に混ざらないことを確認
- TTSやVTSが詰まる場合は、原因メモまでで無理に大改修しない

終了条件:

```text
voice_vtsでemotion tagが読み上げに混ざらず、VTS表情制御も動く
```

コミット例:

```bash
git commit -m "test(vts): verify emotion control in voice_vts"
```

---

### Day 14: update README and docs

目的:

配布物として、ユーザーが自分のLive2Dモデル用hotkeyを設定できる状態にする。

作業:

- READMEにEmotion / VTS Expression Mappingを追加
- `vts_hotkeys.json` の書き方を説明
- presetでのON/OFFを説明
- VTS未接続時は安全にスキップすることを説明
- v1.4とv1.5の違いを明記
- `docs/roadmap_v1.5.md` の進捗を更新

終了条件:

```text
ユーザーが自分のモデル用hotkeyを設定できる
```

コミット例:

```bash
git commit -m "docs: add emotion and vts hotkey mapping guide"
```

---

### Day 15: release check for v1.5.0

目的:

v1.5.0として一区切りつける。

作業:

- 全presetを軽く起動確認
- READMEと実装の整合性確認
- 不要ログ削減
- 使わなくなった古いemotion変換処理を整理
- `change_expression()` を残す場合はlegacy扱いを明記
- zip化前に不要ファイル確認
- release commit
- `v1.5.0` tag

終了条件:

```text
v1.5.0として配布できる状態になっている
```

コミット例:

```bash
git commit -m "chore: prepare v1.5.0 release"
git tag v1.5.0
```

---

## Non-goals

v1.5では以下をやらない。

- OpenAI / Claude provider追加
- LLM provider抽象化の本格整理
- Multi-LLM Baseの全面実装
- 本格的なstreaming parser
- 複数emotionの同時制御
- 複雑な感情推定AI
- 高度なモーション制御
- 長期記憶 / 好感度システム
- 感情履歴の保存
- キャラクター固有の表情セットをFramework側に内蔵すること
- settings.py / models.py の全面再設計
- provider registry / secrets / defaults / legacy の完全分離
- config layer の大規模リファクタ

---

## Operating Rules

- 1日1時間
- 1日1責務まで
- 1日1コミット
- 壊さず終える
- 迷ったら小さいMVPを優先
- plugin化で詰まったらruntime直結MVPを優先
- text_vtsで先に確認し、voice_vtsは後で確認
- Framework側はemotion keyのみ扱う
- hotkey名はcharacter側で定義する
- emotion tagはユーザー表示 / TTSから必ず除去する
- VTS制御に失敗しても会話は継続する

---

## Current Status

- v1.4.0 release zip確認済み
- preset / character / language separation / plugin基盤は動作確認済み
- text_vts / voice_vts の起動bat確認済み
- VTS起動時に `Live2D: Enabled` になることを確認済み
- v1.4.0では感情タグ生成や表情自動制御は未対応
- v1.5.0ではemotion tagとVTS表情制御を追加する
- Day 0から着手可能

---

## Recommended Schedule

```text
Day 0    v1.4.0 README / roadmap整合性修正
Day 1-4  emotion tag生成・parser・表示/TTS除去
Day 5-8  character hotkey mapping・VTS trigger・runtime直結MVP
Day 9    fallback整理
Day 10   plugin化
Day 11   preset確認
Day 12   text_vts実機確認
Day 13   voice_vts実機確認
Day 14   README更新
Day 15   release check / v1.5.0 tag
```
