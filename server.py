import asyncio
import os
import websockets
from crypto_utils import encrypt_message, decrypt_message

CLIENTS = {}  # {websocket: pseudo}

async def broadcast(message_dict, sender_socket=None):
    if CLIENTS:
        message_str = f"{message_dict['type']}|{message_dict.get('pseudo', '')}|{message_dict.get('content', '')}"
        encrypted = encrypt_message(message_str)
        
        # Envoi à tous les clients
        await asyncio.gather(
            *[client.send(encrypted) for client in CLIENTS],
            return_exceptions=True
        )

async def handler(websocket):
    try:
        # Premier message : enregistrement du pseudo
        init_data = await websocket.recv()
        decrypted_init = decrypt_message(init_data)
        _, pseudo, _ = decrypted_init.split('|', 2)
        
        CLIENTS[websocket] = pseudo
        print(f"[+] {pseudo} a rejoint le salon.")
        
        # Notification d'arrivée
        await broadcast({"type": "NOTIFICATION", "content": f"📢 {pseudo} a rejoint le salon."})

        # Boucle de réception des messages
        async for raw_message in websocket:
            decrypted = decrypt_message(raw_message)
            msg_type, user, content = decrypted.split('|', 2)
            
            if content.strip() == "/quit":
                break
                
            await broadcast({"type": "CHAT", "pseudo": user, "content": content})

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in CLIENTS:
            user = CLIENTS.pop(websocket)
            print(f"[-] {user} a quitté le salon.")
            await broadcast({"type": "NOTIFICATION", "content": f"📢 {user} a quitté le salon."})

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Serveur WebSocket démarré sur le port {port}...")
        await asyncio.Future()  # Tourne indéfiniment

if __name__ == "__main__":
    asyncio.run(main())