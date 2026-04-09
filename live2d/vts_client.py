import asyncio
import pyvts
import os
from config.settings import VTS_TOKEN_PATH

class VTSClient:
    def __init__(self):
        self.token_path = os.path.join("config", "tokens", "vts_token.json")
        self.plugin_info = {
            "plugin_name": "MyAIBot",
            "developer": "User",
            "authentication_token_path": self.token_path
        }
        self.vts = pyvts.vts(plugin_info=self.plugin_info)
        self.is_connected = False
        self.hotkey_cache = {}
        # Mutex lock to prevent protocol errors (1002)
        self.lock = asyncio.Lock()

    async def connect(self):
        try:
            await self.vts.connect()
            token_path = self.plugin_info["authentication_token_path"]
            if os.path.exists(token_path) and os.path.getsize(token_path) > 0:
                try: await self.vts.read_token()
                except: pass 

            if not self.vts.authentic_token:
                await self.vts.request_authenticate_token()
                await self.vts.write_token()

            # Dynamic auth method selection
            auth_func = getattr(self.vts, 'request_authenticate', getattr(self.vts, 'authenticate', None))
            if auth_func:
                await auth_func()
            
            self.is_connected = True
            print("[VTS] Authenticated.")
            await self._update_hotkey_cache()
        except Exception as e:
            print(f"[VTS Error] Connection failed: {e}")

    async def _update_hotkey_cache(self):
        async with self.lock:
            try:
                msg = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "hotkey_fetch",
                    "messageType": "HotkeysInCurrentModelRequest"
                }
                res = await self.vts.request(msg)
                if res and "data" in res:
                    hotkeys = res["data"].get("availableHotkeys") or []
                    self.hotkey_cache = {hk["name"]: hk["hotkeyID"] for hk in hotkeys}
            except Exception as e:
                print(f"[VTS Error] Failed to update hotkey cache: {e}")

    async def change_expression(self, emotion: str):
        if not self.is_connected:
            return

        emotion_map = {
            "smile": "Heart Eyes",
            "sad": "Eyes Cry",
            "angry": "Angry Sign",
            "thinking": "Anim Shake"
        }

        hotkey_name = emotion_map.get(emotion.lower())
        if not hotkey_name or hotkey_name not in self.hotkey_cache:
            return

        # Ensure atomic request execution
        async with self.lock:
            try:
                msg = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "trigger_hotkey",
                    "messageType": "HotkeyTriggerRequest",
                    "data": { "hotkeyID": self.hotkey_cache[hotkey_name] }
                }
                await self.vts.request(msg)
            except Exception as e:
                if "1002" in str(e):
                    self.is_connected = False
                print(f"[VTS Error] Send failed ({emotion}): {e}")

    async def close(self):
        if self.is_connected:
            await self.vts.close()