[Goal]

Emotion tag system
Character-level VTS hotkey mapping
Automatic Live2D expression control
Plugin-based emotion handling
Safe fallback for non-VTS environments

[Concept]

AIキャラクター体験の価値を高める

v1.4では、開発者向けフレームワークとして以下の基盤を整える

presetで起動モードを切り替える
characterでsystem promptを切り替える
pluginで拡張可能にする
入力言語 / 出力言語を分離する
VTS接続をpresetで切り替えられるようにする

v1.5では、その基盤の上に、LLMの感情出力とLive2D / VTSの表情制御を追加する

Framework側ではVTS hotkey名を固定しない
Frameworkは抽象的なemotion keyのみ扱う
実際のhotkey名はcharacterごとの設定で解決する

[Core Features]

LLM応答にemotion tagを付与
emotion tagを本文から分離
TTS / 表示用テキストからemotion tagを除去
characterごとのVTS hotkey mapping
VTS hotkey trigger
plugin経由でemotion処理を拡張可能
VTS未接続 / hotkey未設定でも会話を継続

[Relation to v1.4]

v1.4で完了予定の基盤

RuntimeConfig
preset json
character profile / system prompt
input_language_code / output_language_code
runtimeへのconfig注入
feature flagによる STT / TTS / VTS 切替
TTS provider切替
LLM output language instruction
plugins/base.py
plugins/manager.py
plugins/builtin/console_logger.py
text_vts / voice_vts 起動bat

v1.4時点のLive2D / VTS連携は、接続確認とpresetによるON/OFF切替までを対象とする

v1.5では、VTS接続基盤の上に以下を追加する

emotion tag生成
emotion parser
character別hotkey mapping
VTS hotkey trigger
plugin-based emotion control

[Emotion Design]

Framework標準emotion key

neutral
happy
sad
angry
surprised
confused

LLM output format

[emotion:happy]
こんにちは！会えてうれしいです。

Framework behavior

emotion tagを検出
emotion keyを取り出す
本文からemotion tagを削除
characterのVTS hotkey mappingを参照
対応hotkeyがあればVTSへ送信
未設定または失敗時は何もせず会話継続

[Parser Result Design]

parse_emotion_response() は、最低限以下を返す

emotion
clean_text
raw_text

例:

raw_text:
[emotion:happy]
こんにちは！会えてうれしいです。

emotion:
happy

clean_text:
こんにちは！会えてうれしいです。

[Config Design]

preset側ではemotion機能のON/OFFを持つ

emotion_enabled
vts_emotion_enabled

emotion_enabled

LLMにemotion tagを出させ、応答からemotionを解析する
falseの場合、emotion tag instructionは追加しない

vts_emotion_enabled

解析したemotionをVTS hotkey triggerへ接続する
falseの場合、emotion tagを解析してもVTS操作は行わない

emotion_enabled=false の場合、vts_emotion_enabled=true でもVTS emotion制御は動かない

characterごとにVTS hotkey mappingを持つ

characters/default/vts_hotkeys.json

例:

{
  "neutral": null,
  "happy": "Smile",
  "sad": "Sad",
  "angry": "Angry",
  "surprised": "Surprised",
  "confused": null
}

hotkey名はpresetではなくcharacter側で定義する

[Structure Plan]

core/emotion.py
characters/default/vts_hotkeys.json
plugins/builtin/emotion_vts.py
live2d/vts_client.py
core/runtime.py
config/loader.py
presets/
README.md

[v1.5 Must]

emotion tag format追加
emotion parser追加
表示 / TTS用テキストからtag除去
characterごとのvts_hotkeys.json追加
loaderでVTS hotkey mappingを読む
RuntimeConfigまたはcharacter_profileからmappingにアクセス可能にする
VTSClientにhotkey trigger処理を追加
emotion keyからVTS hotkeyを解決
VTS未接続 / hotkey未設定時のfallback
presetによるemotion機能ON/OFF
README更新

[Daily Plan]

Day 1

emotion tag formatを決める
LLM runtime instructionにemotion tag出力ルールを追加する
emotion_enabledの設定方針を決める
終了条件: AI応答に [emotion:xxx] が付く

Day 2

core/emotion.py を作る
parse_emotion_response() を作る
emotion tagと本文を分離する
終了条件: [emotion:happy] と本文を別々に取得できる

Day 3

main loop側でemotion tagを除去した本文を使う
表示用テキストからemotion tagを消す
TTSに渡すテキストからemotion tagを消す
終了条件: ユーザー表示と読み上げにemotion tagが混ざらない

Day 4

characters/default/vts_hotkeys.json を作る
config/loader.py でcharacterのVTS hotkey mappingを読む
RuntimeConfigまたはcharacter_profileにmappingを持たせる
終了条件: runtimeからcharacter hotkey mappingにアクセスできる

Day 5

VTSClientにhotkey trigger用メソッドを追加する
指定hotkey名をVTube Studio APIへ送る
失敗時は例外で落とさずログに出す
終了条件: 任意のhotkey名をVTSへ送れる

Day 6

emotion keyからcharacter hotkeyを解決する
emotion tag検出後にVTS hotkeyを呼ぶ
hotkey未設定なら何もしない
終了条件: [emotion:happy] で対応hotkeyが呼ばれる

Day 7

VTS未接続 / hotkey未設定 / emotion不正値のfallbackを整理する
neutralやunknown時の挙動を決める
不要なログを抑制する
終了条件: emotion処理に失敗しても会話が落ちない

Day 8

plugins/builtin/emotion_vts.py を作る
Day6までのruntime直結処理をplugin側に移す
runtime初期化時にEmotionVTSPluginを登録する
終了条件: emotion処理がplugin経由で動く

Day 9

presets側にemotion_enabled / vts_emotion_enabledを追加する
text_vts / voice_vtsでemotion制御を有効化する
text_chatでは無効またはtag除去のみを確認する
終了条件: presetでemotion機能のON/OFFが切り替わる

Day 10

READMEにEmotion / VTS Expression Mappingを追加する
vts_hotkeys.jsonの書き方を説明する
v1.4とv1.5の違いを明記する
終了条件: ユーザーが自分のモデル用hotkeyを設定できる

Day 11

text_vtsで動作確認
VTube Studio起動時に表情hotkeyが動くことを確認
VTS未起動時に落ちないことを確認
終了条件: text_vtsでemotion表情制御が動く

Day 12

voice_vtsで動作確認
STT / LLM / TTS / VTS の一連の流れを確認
emotion tagが音声に混ざらないことを確認
終了条件: voice_vtsでemotion表情制御が動く

Day 13

ログ整理
debug出力の抑制
READMEと実装の整合性確認
終了条件: v1.5機能の説明と実装が一致している

Day 14

全presetの軽い動作確認
不要コード整理
小さい不具合修正
終了条件: v1.5.0として一区切りつけられる

[Non-goals]

モデルごとのhotkey名をFramework側で固定しない
複雑な感情推定AIは追加しない
複数emotionの同時制御はしない
高度なモーション制御はしない
長期記憶 / 好感度システムは扱わない
感情履歴の保存はしない
キャラクター固有の表情セットをFramework側に内蔵しない

[Operating Rules]

1日1時間
1日1責務まで
壊さず終える
1日1コミット
hotkey名はcharacter側で定義する
Framework側はemotion keyのみ扱う
emotion tagはユーザー表示 / TTSから必ず除去する
VTS制御に失敗しても会話は継続する
詰まったらplugin化を後回しにしてruntime直結MVPを優先する
text_vtsで先に確認し、voice_vtsは後で確認する

[Current Status]

v1.4 Day12まで完了
preset / character / language separation / plugin基盤は動作確認済み
text_vts / voice_vts の起動bat確認済み
VTS起動時に Live2D: Enabled になることを確認済み
v1.4では感情タグ生成や表情自動制御は未対応
v1.5ではemotion tagとVTS表情制御を追加予定
Day 1 から着手可能