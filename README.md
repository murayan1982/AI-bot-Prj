# My AI Bot Prot
A prototype AI agent that integrates with VTube Studio to enjoy conversations with emotionally expressive AI characters.
VTube Studio と連携し、感情豊かな AI キャラクターとの対話を楽しめる AI エージェントのプロトタイプです。

## Key Features
- **Gemini 2.0 Flash Integration: Achieves high-speed, advanced dialogue and context maintenance.
- **Emotion Sync System: Automatically changes Live2D model expressions by extracting emotion tags from AI responses.
- **Auto Memory Refresh: Summarizes the "atmosphere" of the conversation every 10 turns and resets history to maintain performance.
- **Voice Interaction Mode: Supports voice output via ElevenLabs (TTS) integration using the --voice flag.

- **Gemini 2.0 Flash 連携**: 高速かつ高度な対話、文脈維持を実現。
- **感情連動システム**: AI の返答から感情タグを抽出し、Live2D モデルの表情を自動変更。
- **自動メモリリフレッシュ**: 10 ターンごとに会話の「空気感」を要約して引き継ぎつつ、履歴をリセットしてパフォーマンスを維持。
- **音声対話モード**: ElevenLabs (TTS) と連携した音声出力に対応 (`--voice` フラグ)。

## Setup(セットアップ)
1. Clone the Repository(リポジトリのクローン)
   ```git clone [https://github.com/murayan1982/my-ai-bot-prot.git](https://github.com/murayan1982/my-ai-bot-prot.git)
   cd my-ai-bot-prot```
2. Install Dependencies(ライブラリのインストール)
    ```pip install -r requirements.txt```
3. Configure API Keys(APIキーの設定)
    Create a .env file in the project root and enter your keys:
    プロジェクト直下に .env ファイルを作成し、以下を記入してください。
    ```GEMINI_API_KEY=your google api key```
    ```ELEVENLABS_API_KEY=your elevenLabs api key```

## How to Run(実行方法)
1. Text Mode(テキストモード)
    ```python main.py```
2. Voice Mode(音声対話モード)
    ```python main.py --voice```

## License & Notes(注意事項)
・Before running, start VTube Studio and enable "Allow API access" in the settings.
・Never upload your .env file to GitHub.

・実行前に VTube Studio を起動し、設定から「API を利用する」を有効にしてください。
・API キーは .env ファイルで管理し、GitHub には絶対にアップロードしないでください。

