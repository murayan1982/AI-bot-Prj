[Goal]

開発者向けAIフレームワーク
音声会話 + Live2D の体験基盤
構成（preset / character / plugin / LLM）で挙動を切り替えられる設計

---

[v1.4] Config Foundation

- config/loader.py の完成
- RuntimeConfig 導入
- env → preset → character → default の優先順位確立
- presets 読み込み対応
- character 読み込み対応
- input / output language 分離
- runtime に config 注入
- 最小 plugin 基盤作成
- 起動時に設定表示
- run scripts 整備
- README 最低限整備

Goal:
設定ベースで動作が切り替わる「土台」が完成する

---

[v1.5] Emotion / VTS Expression Control

- LLM応答にemotion tagを付与
- emotion tagを本文から分離
- 表示 / TTS用テキストからemotion tagを除去
- characterごとのVTS hotkey mapping
- VTS hotkey trigger
- plugin経由でemotion処理を拡張可能にする
- VTS未接続 / hotkey未設定でも会話を継続
- RuntimeConfig を main runtime flow の正本として扱う方針を明確化
- character-level hotkey mapping によって Framework abstraction と model-specific hotkey を分離
- runtime直結MVPで emotion / VTS 経路を成立させる
- legacy path（change_expression / VTS_EMOTION_ALIAS / old global flags）を明示
- settings.py / models.py の責務再配分方針を整理する

Goal:
AIキャラクターの表情制御がFramework構成で扱え、
主経路と legacy path の境界が明確になった状態にする

---

[v1.6] Config Responsibility Cleanup & Framework Readability

- settings.py / models.py の責務再配分
- LLM registry を settings.py から分離
- TTS registry を models.py から分離
- secrets / developer defaults / legacy compatibility の責務を切り分ける
- RuntimeConfig を runtime behavior の source of truth とする構成へ寄せる
- preset / character / runtime / registry の責務境界を整理する
- loader / runtime flow の可読性を改善する
- preset の役割を整理し、`text_chat` を safe default として明確化する
- default preset を廃止し、起動導線を `text_chat` 基準に揃える
- plugin / hook contract を整理する
- developer configuration guide を追加する
- plugin / hook contract documentation を追加する
- cleanup / consistency pass を行う
- config cleanup 後の preset 動作確認を行う
  - text_chat
  - text_vts
  - voice_vts
  - bilingual_ja_en

[Note]
v1.5 開発時点から継続している既知の観測事項:
`voice_vts` では、環境やタイミングにより VTS / TTS 経路に軽い不安定さが見えることがある。
v1.6 では config / responsibility cleanup を優先し、
音声経路の本格的な安定化や再設計は今後の課題として扱う。

Goal:
設定責務の境界が明確で、
RuntimeConfig / preset / character / registry を中心に読みやすく拡張しやすい
Framework 構成へ整理された状態にする

---

[v1.7] UX & Streaming

- LLM逐次応答の表示体験改善
- TTS逐次再生の整理
- 音声会話の体感レスポンス改善
- エラーメッセージ / fallback UX 改善
- 初回セットアップ導線改善

Goal:
「速くて使いやすい」と感じる体験に近づける

---

[v1.8] Plugin Expansion

- plugin APIの安定化
- plugin manager の拡張
- builtin plugin の追加
  - console logger 強化
  - simple memory
  - external API sample
- pluginのサンプル充実
- ドキュメント整備（plugin作成方法）

Goal:
「拡張できるフレームワーク」として成立する

---

[v1.9] Stabilization

- 軽いテスト整備
- preset / plugin の動作確認
- 互換性チェック
- 不要ログ削減
- エッジケース修正
- サンプルプロジェクト追加

Goal:
安定して配布できる状態にする

---

[v2.0] Framework Release

- ドキュメント全面整備
- Quick Start 完成
- サンプル構成の洗練
- 初心者でも使える導線確立
- リポジトリ構成の最終整理

Goal:
「フレームワークとして完成」と言える状態

---

[Design Principles]

- 構造 → 抽象化 → UX → 拡張 → 安定 の順で進める
- 1日1責務・壊さず終える
- preset / character / plugin を中心に拡張する
- loader は「読むだけ」、処理ロジックを持たせない
- runtime に責務を集約する
- RuntimeConfig を runtime behavior の source of truth とする
- settings.py は最終的に神ファイル化させない
- provider/model registry は runtime config から分離する
- legacy compatibility は main framework flow から分けて管理する

---

[Future Ideas (Optional)]

- 自動LLM fallback
- キャッシュ機構
- 非同期パイプライン最適化
- Web UI / 設定画面
- クラウド設定保存
- マルチセッション対応
