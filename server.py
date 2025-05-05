import asyncio
import functools
import websockets
import os

clients = {}

# 🧩 This is the handler for each client
async def handler(ws, path):
    client_id = "unknown"
    try:
        client_id = await ws.recv()
        print(f"[CONNECTED] {client_id}")
        clients[client_id] = ws

        async for message in ws:
            if "::" in message:
                target_id, payload = message.split("::", 1)
                if target_id in clients:
                    await clients[target_id].send(payload)
    except Exception as e:
        print(f"[ERROR] {client_id}: {e}")
    finally:
        if client_id in clients:
            del clients[client_id]
            print(f"[DISCONNECTED] {client_id}")

# 🚀 Properly register the handler with both ws + path
async def main():
    port = int(os.environ.get("PORT", 5000))
    print(f"[PixelRoot RELAY] Starting on port {port}...")
    async with websockets.serve(
        functools.partial(handler),
        "0.0.0.0",
        port
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
