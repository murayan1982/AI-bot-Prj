import asyncio
from core.runtime import initialize_components, shutdown_components
from core.session import ChatSession
from config.loader import load_runtime_config

async def main():
    runtime = None
    try:
        runtime = await initialize_components()

        session = ChatSession(runtime)
        await session.run()

    except KeyboardInterrupt:
        print("\nSystem shutting down...")
    except Exception as e:
        print(f"\n[Fatal Error] {e}")
    finally:
        if runtime:
            try:
                await shutdown_components(runtime)
            except Exception as e:
                print(f"[Cleanup Error] {e}")

def main() -> None:
    config = load_runtime_config()

    print("[Config] Loaded in main.py")
    print(config)
    print(config.system_prompt)

    # Day5でここを使う
    # runtime = initialize_components(config)


if __name__ == "__main__":
    main()