import asyncio
import websockets

clients = {}

async def handler(ws, path):
    try:
        # First message must be the client's unique ID
        client_id = await ws.recv()
        print(f"[CONNECTED] {client_id}")
        clients[client_id] = ws

        async for message in ws:
            if "::" in message:
                target_id, payload = message.split("::", 1)
                if target_id in clients:
                    try:
                        await clients[target_id].send(payload)
                    except:
                        print(f"[ERROR] Failed to send to {target_id}")
    except Exception as e:
        print(f"[DISCONNECTED] {client_id} - {e}")
    finally:
        if client_id in clients:
            del clients[client_id]

if __name__ == "__main__":
    print("[STARTING] Pixel Root Relay Server on port 5000...")
    start_server = websockets.serve(handler, "0.0.0.0", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
