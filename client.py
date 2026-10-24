import asyncio
import sys
import websockets
from crypto_utils import encrypt_message, decrypt_message

async def receive_messages(websocket):
    try:
        async for message in websocket:
            decrypted = decrypt_message(message)
            msg_type, pseudo, content = decrypted.split('|', 2)
            
            if msg_type == "NOTIFICATION":
                print(f"\n{content}")
            elif msg_type == "CHAT":
                print(f"\n[{pseudo}] : {content}")
            print("> ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\n[!] Déconnecté du serveur.")

async def send_messages(websocket, pseudo):
    loop = asyncio.get_event_loop()
    while True:
        # Lecture non-bloquante de la console
        msg = await loop.run_in_executor(None, input, "> ")
        if not msg.strip():
            continue
            
        payload = f"CHAT|{pseudo}|{msg}"
        encrypted = encrypt_message(payload)
        await websocket.send(encrypted)
        
        if msg.strip() == "/quit":
            print("[+] Déconnexion en cours...")
            await websocket.close()
            break

async def main():
    server_url = input("Entrez l'URL WebSocket du serveur").strip()
    pseudo = input("Choisissez votre pseudo : ").strip()
    
    while not pseudo:
        pseudo = input("Le pseudo ne peut pas être vide : ").strip()

    try:
        async with websockets.connect(server_url) as websocket:
            # Envoi du pseudo au serveur
            init_payload = f"INIT|{pseudo}|hello"
            await websocket.send(encrypt_message(init_payload))
            print(f"✅ Connecté au salon sous le pseudo '{pseudo}'. Tapez '/quit' pour quitter.")

            # Exécution simultanée de l'écoute et de l'envoi
            await asyncio.gather(
                receive_messages(websocket),
                send_messages(websocket, pseudo)
            )
    except Exception as e:
        print(f"\n[!] Erreur de connexion : {e}")

if __name__ == "__main__":
    asyncio.run(main())
