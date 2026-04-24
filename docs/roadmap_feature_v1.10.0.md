[v1.10] Character Structure & Developer Flow Cleanup

Goal:
character 周りの構造と編集導線を整理し、
「どこを触ればキャラクターを変えられるか」
「どこまでが character で、どこからが runtime / preset か」
が分かりやすい状態にする。

v1.10 では音声基盤の大改修には入らず、
character structure / loader responsibility / developer flow の整理に集中する。

---

[Day1] Character Flow Review

- 現在の character 読み込みフローを整理する
- `profile / system / vts_hotkeys` の責務を確認する
- character と preset / runtime の境界を再確認する
- 現状の editing flow がどこで分かりにくいか整理する
- 改善対象を「構造」「責務」「導線」に分けて整理する

Goal:
character customization のどこを整えるべきかを明確にする

---

[Day2] Character Loader Responsibility Cleanup

- character loader の責務を整理する
- loader が「読むだけ」で済む境界を再確認する
- runtime / loader / character data の責務分担を読みやすくする
- character data の読み込みエラー時の見え方を確認する
- source of truth が RuntimeConfig 側に揃うよう整える

Goal:
character 読み込み責務が分かりやすく、
runtime flow から見ても追いやすい状態にする

---

[Day3] Character File / Naming Cleanup

- `profile.json` / `system.txt` / `vts_hotkeys.json` の命名と役割を再確認する
- file naming と README 上の説明を一致させる
- character 関連の path / naming の揺れがないか確認する
- 1 character = 1 directory の見え方を強める
- 将来の character 追加を見据えて読みやすさを整える

Goal:
character file 構成と naming が一貫して見える状態にする

---

[Day4] Character Template / Example Flow Review

- character を追加 / 差し替えする時の流れを整理する
- default character を基準にした編集導線を確認する
- 必要なら最小テンプレートや example の置き方を検討する
- どのファイルを複製・編集すればよいか README で説明しやすくする
- character customization の最小作業単位を明確にする

Goal:
character 追加 / 差し替えの最小フローが分かりやすい状態にする

---

[Day5] Docs / README Character Guidance

- character customization の説明を README / docs に反映する
- `profile / system / vts_hotkeys` の役割を整理して説明する
- character と preset / runtime の違いをより明確にする
- 開発者が最初に触るべき character file を分かりやすくする
- first customization の導線を自然にする

Goal:
README / docs から character customization の流れが自然に伝わる状態にする

---

[Day6] Developer Flow Cleanup

- 開発者が最初に見るべき設定とファイルを整理する
- `.env` / preset / character / registry の編集導線を軽く整える
- character 変更と runtime mode 変更の境界を再確認する
- 開発時に迷いやすいポイントを README / docs と整合させる
- 小さな導線上のノイズを減らす

Goal:
開発者が「何を変えたい時にどこを触るか」を追いやすい状態にする

---

[Day7] Cleanup & Consistency Pass

- touched files ベースで comment / docstring を補強する
- character / loader / runtime / docs / README の整合性を確認する
- text_chat / text_vts / voice_vts の軽い確認を行う
- character 変更時の基本導線が崩れていないか確認する
- 一時確認コードや不要ログが残っていないか確認する
- v1.10.0 リリース前提の最終整理を行う

Goal:
character structure と developer flow の改善が一貫した状態でリリースできるようにする

---

[Scope Notes]

- v1.10 の主軸は character structure と developer flow の整理とする
- `profile / system / vts_hotkeys` の責務明確化を重視する
- 1 character = 1 directory の見え方を強める
- 音声基盤の大改修や会話デザインの本格改善には入らない
- provider abstraction や latency 改善は v2.0 以降の課題として残す
- character は「誰として振る舞うか」、preset / runtime は「どう動くか」として整理する
- README / docs と実装の整合性を重視する

---

[Expected Outcome]

- character customization の入口がより分かりやすい
- `profile / system / vts_hotkeys` の役割が明確
- character loader と runtime の責務境界が読みやすい
- character の追加 / 差し替えフローが追いやすい
- README / docs と実装が character 観点でより揃っている
- v2.0 に向けて会話UX / 音声基盤の課題を無理なく残せる