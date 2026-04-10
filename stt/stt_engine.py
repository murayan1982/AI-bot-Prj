# stt/stt_engine.py

import speech_recognition as sr
import asyncio
from config.settings import STT_LANGUAGE, INPUT_VOICE_ENABLED

class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # Sensitivity adjustment for silence
        self.recognizer.pause_threshold = 1.0 

    async def listen(self):
        # Return None immediately if voice input is disabled
        if not INPUT_VOICE_ENABLED:
            return None
        
        with self.microphone as source:
            # 1. Calibrate for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("\r[STT/Text Waiting...] ", end="", flush=True)
            try:
                # 2. Capture audio data (Strict timeout for start of speech)
                audio = await asyncio.to_thread(
                    self.recognizer.listen, 
                    source, 
                    timeout=5,           # Wait max 5s for user to start speaking
                    phrase_time_limit=8  # Max 8s for the phrase duration
                )
                
                print("\r[STT] Recognizing...          ", end="", flush=True)

                # 3. Recognition with a hard timeout using asyncio.wait_for
                # Prevents freezing if the Google server doesn't respond
                text = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.recognizer.recognize_google, 
                        audio, 
                        language=STT_LANGUAGE
                    ),
                    timeout=7.0
                )

                if text:
                    print(f"\nUser (Voice): {text}")
                    return text

            except asyncio.TimeoutError:
                print("\r[STT] Recognition timed out.       ", end="", flush=True)
                return ""
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                # Silent or unrecognized audio
                return ""
            except Exception as e:
                # Log error and continue to avoid crashing the main loop
                print(f"\n[STT Error]: {type(e).__name__}: {e}")
                return ""
        
        return ""