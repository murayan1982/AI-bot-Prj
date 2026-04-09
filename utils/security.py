import os
import speech_recognition as sr

class SecurityManager:
    """プロジェクトの安全性を確保するクラス"""
    @staticmethod
    def ensure_safe_environment():
        # 1. フォルダ作成
        os.makedirs("config/tokens", exist_ok=True)
        
        # 2. .gitignore の確認と追記
        ignore_content = "\n# VTube Studio Tokens\n**/tokens/*.json\n"
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write(ignore_content)
        else:
            with open(".gitignore", "r") as f:
                if "**/tokens/*.json" not in f.read():
                    with open(".gitignore", "a") as f:
                        f.write(ignore_content)

class STTEngine:
    """音声入力（耳）を担当するクラス"""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    async def listen(self):
        # VSCodeのターミナルを汚さないようにステータスを表示
        # (以前作成した ANSIクリーナー等のロジックをここに適用)
        print("\r[Status] Listening...", end="", flush=True)
        
        with self.microphone as source:
            # 周囲の雑音に合わせて調整
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            print("\r[Status] Recognizing...", end="", flush=True)
            text = self.recognizer.recognize_google(audio, language="ja-JP")
            print(f"\rUser (Voice): {text}")
            return text
        except sr.UnknownValueError:
            print("\r[Status] Could not understand audio.")
            return None
        except sr.RequestError:
            print("\r[Status] Could not request results from STT service.")
            return None