import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from live2d.vts_client import VTSClient


async def main():
    vts = VTSClient()

    print("connecting...")
    ok = await vts.connect()
    print("connected:", ok)

    if ok:
        print("hotkey_cache:", vts.hotkey_cache)

        for name in ["Heart Eyes", "Shock Sign", "Remove Expressions", "NoSuchHotkey"]:
            result = await vts.trigger_hotkey(name)
            print(f"trigger {name}: {result}")
            await asyncio.sleep(5)

    await vts.close()


if __name__ == "__main__":
    asyncio.run(main())