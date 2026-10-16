import asyncio
import json
import websockets

clients = {}
rooms = {}


async def handler(ws):
    cid = id(ws)
    clients[cid] = ws
    try:
        async for msg in ws:
            data = json.loads(msg)
            room = data.get('room', 'general')
            rooms.setdefault(room, set()).add(cid)
            for pid in list(rooms.get(room, [])):
                if pid != cid and pid in clients:
                    await clients[pid].send(data.get('text', ''))
    finally:
        clients.pop(cid, None)


async def main():
    async with websockets.serve(handler, '0.0.0.0', 8765):
        await asyncio.Future()


asyncio.run(main())
