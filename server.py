import asyncio
import websockets

clients = {}

async def handler(ws, path):
    try:
        client_id = await ws.recv()
        print(f"[CONNECTED] {client_id}")
        clients[client_id] = ws

        async for message in ws:
            if "::" in message:
                target_id, payload = message.split("::", 1)
                if target_id in clients:
                    await clients[target_id].send(payload)
    except:
        print(f"[DISCONNECTED] {client_id}")
    finally:
        if client_id in clients:
            del clients[client_id]

async def main():
    print("[STARTING] Pixel Root Relay Server on port 5000...")
    async with websockets.serve(handler, "0.0.0.0", 5000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
