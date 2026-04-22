[v1.7] UX & Streaming

Goal:
「速くて使いやすい」と感じる体験に近づける。
LLMの逐次応答・表示・音声出力・エラー時の挙動を整理し、
体感レスポンスと初回導線を改善する。

---

[Day1] Streaming UX Responsibility Split

- core/pipeline.py の streaming 処理責務を整理する
- 「表示用 chunk」と「TTS投入用 segment」の役割を分ける
- streaming UX 向け helper / utility の導入方針を決める
- 現行フローを壊さずに分離できる最小構成へ寄せる
- text_chat で基本動作確認を行う

Goal:
v1.7 の改善を安全に進めるための責務境界を作る

---

[Day2] Incremental Text Display Improvement

- LLM streaming 応答の途中表示を改善する
- 初回 chunk 到着前の待機表示を整理する
- first chunk 到着後の表示遷移を自然にする
- console 出力の改行 / prefix / flush 挙動を見直す
- text_chat / bilingual_ja_en で表示確認を行う

Goal:
「返ってきている感」が早く伝わる表示体験にする

---

[Day3] TTS Segmenting Cleanup

- TTS逐次再生用の segment 切り出し条件を整理する
- 日本語句読点だけでなく英語 punctuation も考慮する
- 短すぎる segment / 不自然な切れ方を減らす
- flush 時の残りテキスト処理を見直す
- voice 出力あり構成で基本確認を行う

Goal:
逐次読み上げが不自然になりにくい土台を作る

---

[Day4] Voice Response Perceived Latency Improvement

- first chunk 到着から first TTS enqueue までの流れを改善する
- 音声会話時の待機状態が分かる表示を追加 / 整理する
- voice_vts で「待たされている感」を減らす調整を行う
- 必要なら TTS buffering 関連の閾値を定数 / config として整理する
- text / voice 両方で挙動差を確認する

Goal:
音声会話の体感レスポンスを改善する

---

[Day5] Error Message & Fallback UX Improvement

- VTS / TTS / LLM 各経路のエラーメッセージを見直す
- ユーザー向け表示と開発者向けログの粒度を整理する
- VTS失敗時に会話継続できることを明示する
- TTS失敗時に text only fallback へ落ちる流れを分かりやすくする
- representative な失敗ケースの表示確認を行う

Goal:
壊れても分かりやすく、使い続けやすい体験にする

---

[Day6] First-Time Setup Flow Improvement

- README の Quick Start / 初回起動導線を改善する
- safe default として text_chat の案内を強化する
- voice_vts / text_vts を optional path として整理する
- .env / preset / character の最低限必要な準備を分かりやすくする
- 初見開発者が迷いにくい構成へ整える

Goal:
初回セットアップと初回起動のハードルを下げる

---

[Day7] Cleanup & Consistency Pass

- v1.7 変更全体の cleanup を行う
- コメント / docstring を touched files ベースで補強する
- preset 動作確認を行う
  - text_chat
  - text_vts
  - voice_vts
  - bilingual_ja_en
- README / runtime behavior / logging の整合性を確認する
- v1.7.0 リリース前提の最終整理を行う

Goal:
UX改善が入った v1.7 を一貫した状態で締める

---

[Design Notes]

- v1.7 は「streaming機能の新規追加」ではなく
  「streaming体験の整理と改善」を主眼にする
- display chunk と speech segment は責務を分ける
- first token / first chunk / first audio を UX 指標として意識する
- loader に UX ロジックを寄せず、runtime / pipeline 側で扱う
- 失敗時も会話継続を優先する
- 大規模な非同期再設計は v1.7 のスコープ外とする

---

[Expected Outcome]

- テキスト応答の途中表示が分かりやすい
- 音声応答の読み始めが早く感じられる
- エラー時の挙動が理解しやすい
- 初回セットアップが入りやすい
- 「速くて使いやすい」方向の改善が見える