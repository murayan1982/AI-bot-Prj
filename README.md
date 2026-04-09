# AI Voice Bot Framework

A modular AI bot framework that integrates **LLM (Gemini) + TTS (ElevenLabs) + Live2D**.

Build your own interactive AI character with voice and animation.

---

## ✨ Features

- 🧠 Natural conversation using Google Gemini
- 🔊 High-quality voice synthesis via ElevenLabs
- 🎭 Live2D integration support
- ⚙️ Flexible configuration (models, voice, speed, etc.)
- 🧩 Modular structure for easy customization

---

## 🚀 Quick Start

### 1. Clone repository

```
git clone https://github.com/murayan1982/AI-bot-Prj.git
cd AI-bot-Prj
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Create `.env`

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
ELEVENLABS_API_KEY=your_api_key_here
```

### 4. Run

```
python main.py
```

---

## 🎯 Who is this for?

- Developers who want to build AI-powered characters
- People interested in voice-based AI interaction
- Anyone experimenting with LLM + TTS + Live2D

---

## 🗂 Project Structure

```
my-ai-bot/
├── config/        # Settings and model configuration
├── llm/           # LLM integration (Gemini)
├── tts/           # Voice engine (ElevenLabs)
├── live2d/        # Live2D integration
├── prompts/       # System prompts
├── utils/         # Utility scripts
├── main.py        # Entry point
```

---

## ⚙️ Configuration

Main settings are located in:

```
config/settings.py
```

You can adjust:

- LLM model selection
- Voice settings
- TTS speed
- Engine switches (STT / TTS)

---

## 🧪 Example Use Cases

- AI VTuber prototype
- Voice assistant with personality
- Interactive character systems

---

## ⚠️ Notes

- `.env` is required for API keys
- FFmpeg (`ffplay`) must be installed for audio playback

---

## 📌 Roadmap

- Streaming TTS
- Improved Live2D sync
- UI for configuration

---

## 📄 License

MIT License

---

## 💡 Author

Created by murayan

