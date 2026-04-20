# Plugin / Hook Contract

## 目的

このドキュメントは、v1.6 時点の plugin / hook 契約を明文化するためのものです。

現時点の plugin system は最小構成ですが、
以下を開発者がコードを追わなくても理解しやすい状態にすることを目的とします。

- plugin の基本責務
- lifecycle と event hook の違い
- runtime 側が plugin に渡すもの
- 利用可能な hook 一覧
- 新しい plugin を追加する基本手順

このドキュメントは「全面再設計」の仕様ではなく、
v1.6 時点で実際に動いている contract の整理メモです。

---

## 全体像

現在の plugin / hook は、次の2層で構成されています。

1. plugin lifecycle
2. runtime event hooks

### 1. plugin lifecycle

plugin は `BasePlugin` を継承し、最低限以下の lifecycle entry point を持てます。

- `setup(runtime)`
- `on_start(runtime)`
- `on_stop(runtime)`

これらは `PluginManager` が呼び出します。

### 2. runtime event hooks

より細かいイベント通知は、`runtime["hooks"]` に callback を登録し、
`emit()` から発火されます。

つまり現状の構成は、

- `PluginManager` = plugin の登録と lifecycle の管理
- `runtime["hooks"]` + `emit()` = イベント通知の管理

という分担になっています。

---

## 基本責務

### BasePlugin

`BasePlugin` は、すべての plugin の基底クラスです。

役割:

- plugin 名の共通インターフェース
- enabled フラグ
- lifecycle method の共通入口

注意点:

- `BasePlugin` 自体は event hook 登録を強制しません
- 必要な plugin は `setup()` の中で `runtime["hooks"]` へ callback を登録します

### PluginManager

`PluginManager` は最小限の manager です。

役割:

- plugin を登録する
- `setup()` を呼ぶ
- `on_start()` を呼ぶ
- `on_stop()` を呼ぶ

責務外:

- 個別 event hook の dispatch
- hook 名の定義
- runtime dict の詳細構築

### Built-in Plugin

現時点で確認できる built-in plugin は以下です。

- `ConsoleLoggerPlugin`
- `EmotionVTSPlugin`

`ConsoleLoggerPlugin` は lifecycle plugin の最小例です。  
`EmotionVTSPlugin` は event hook 登録型 plugin の代表例です。

---

## runtime dict について

plugin は `runtime: dict[str, Any]` を受け取ります。

現時点で plugin 側から参照されうる代表的なキー:

- `config`
- `hooks`
- `vts`
- `llm`
- `stt`
- `tts`
- `use_stt`
- `use_tts`
- `log_file`

ただし、すべての plugin がすべてのキーに依存してよいわけではありません。

推奨方針:

- plugin は必要最小限の key だけ読む
- 必須でない key は `get()` で参照する
- key 不在時は安全に no-op で戻る

例:

- `EmotionVTSPlugin` は `config`, `vts`, `hooks` を参照する
- `ConsoleLoggerPlugin` は主に `config` を参照する

---

## 現在使われている hook 一覧

v1.6 時点で確認できる runtime event hooks は以下です。

### `on_user_input(text)`

ユーザー入力を受け取った後に発火されます。

用途例:

- 入力ログ
- 外部通知
- セッション観測

### `on_emotion_detected(emotion)`

emotion が解決されたタイミングで発火されます。

用途例:

- VTS hotkey 発火
- emotion ログ
- 将来的なキャラ挙動拡張

### `on_llm_chunk(chunk)`

LLM の表示用 chunk が出力されるたびに発火されます。

用途例:

- streaming UI
- chunk 単位ログ
- 外部表示連携

### `on_llm_complete(response_text)`

LLM 応答が最後まで処理された後に発火されます。

用途例:

- 完了ログ
- 応答保存
- 後処理

### `on_error(error)`

セッションループ内で例外が発生したときに発火されます。

用途例:

- エラーログ
- 外部監視
- 通知

---

## lifecycle と event hook の違い

### lifecycle

lifecycle は plugin 自体の開始・終了に関わるものです。

- `setup()`
- `on_start()`
- `on_stop()`

これは plugin manager が責任を持って呼びます。

### event hook

event hook は実行中の出来事に反応するためのものです。

- `on_user_input`
- `on_emotion_detected`
- `on_llm_chunk`
- `on_llm_complete`
- `on_error`

これは `runtime["hooks"]` と `emit()` の経路で処理されます。

---

## EmotionVTSPlugin の位置づけ

`EmotionVTSPlugin` は現在の plugin / hook contract を理解する上での代表例です。

役割:

- emotion event を受け取る
- character-level hotkey mapping を解決する
- VTS client へ hotkey trigger を渡す

責務境界:

- emotion 文字列の生成は担当しない
- main runtime mode selection は担当しない
- VTS hotkey mapping の定義自体は character data 側が持つ
- plugin は「emotion event -> VTS action」の橋渡しだけを行う

この設計により、

- emotion logic
- character-specific mapping
- VTS side effect

が完全ではないにせよ、ある程度分離されています。

---

## ConsoleLoggerPlugin の位置づけ

`ConsoleLoggerPlugin` は最小 lifecycle plugin の例です。

役割:

- setup 時の情報表示
- runtime 開始/終了ログ

この plugin は event hook 登録を使わず、
lifecycle だけで成立する最小サンプルになっています。

そのため、新しい plugin を作るときの入口として分かりやすい実装です。

---

## 新しい plugin を追加する基本手順

### 1. `BasePlugin` を継承する

```python
class MyPlugin(BasePlugin):
    name = "my_plugin"
    enabled = True
```

### 2. 必要なら `setup()` で runtime を保持する

```python
def setup(self, runtime):
    self.runtime = runtime
```

### 3. 必要な event hook を登録する

```python
hooks = runtime.setdefault("hooks", {})
hooks.setdefault("on_llm_complete", []).append(self.on_llm_complete)
```

### 4. callback 側で安全に runtime を扱う

- `get()` を使う
- 必須条件がなければ即 return
- 副作用がある処理は条件チェック後に行う

### 5. register する

plugin manager へ register して lifecycle に乗せる

---

## 実装上の注意

- plugin は main runtime flow を大きく書き換えない
- plugin 側は no-op で安全に抜けられる設計を優先する
- runtime dict の暗黙依存は増やしすぎない
- event hook 名を増やす場合は docs も更新する
- plugin は「責務の追加」に使い、「責務の混在」を増やさない

---

## v1.6 時点でまだ最小構成な点

現時点の plugin / hook system は意図的に最小構成です。

まだ本格的にやっていないこと:

- hook 型の厳密定義
- runtime dict の型定義
- plugin dependency 管理
- plugin load order 制御
- plugin failure isolation の高度化
- 外部 plugin package の正式サポート

つまり、v1.6 の目的は system を大きくすることではなく、
今ある contract を読みやすく保つことにあります。

---

## Day8 の着地点

Day8 の目的は以下です。

- plugin lifecycle と event hook の違いが説明できる
- built-in plugin の役割が説明できる
- runtime hook 一覧が docs 化されている
- 新規 plugin の追加手順が最低限説明できる

この状態を v1.6 時点の plugin / hook contract として扱う。
