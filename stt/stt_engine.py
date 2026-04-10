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
        if not INPUT_VOICE_ENABLED:
            return None
        
        with self.microphone as source:
            # 1. Calibrate for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("\r[STT/Text Waiting...] ", end="", flush=True)
            try:
                # 2. Capture voice data (Strict timeout to avoid long hangs)
                audio = await asyncio.to_thread(
                    self.recognizer.listen, 
                    source, 
                    timeout=5,           # Wait max 5s for speech to start
                    phrase_time_limit=8  # Max 8s per phrase
                )
                
                print("\r[STT] Recognizing...          ", end="", flush=True)

                # 3. Recognition with a hard timeout using asyncio.wait_for
                # If Google doesn't respond in 7s, force-quit this task
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
                # Triggered when Google API hangs too long
                print("\r[STT] Recognition timed out.       ", end="", flush=True)
                return ""
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                # No speech detected or not understood
                return ""
            except Exception as e:
                # Catch-all for other errors to keep the loop running
                print(f"\n[STT Error]: {type(e).__name__}: {e}")
                return ""
        
        return ""