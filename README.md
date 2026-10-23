# Application de Chat Chiffré AES (Client / Serveur)

##Description de mon projet
Cette application est un système de chat en temps réel reposant sur une architecture Client/Serveur via des WebSockets. 
Toutes les communications entre le client et le serveur sont chiffrées de bout en bout (ou du client au serveur) grâce à l'algorithme de chiffrement symétrique **AES-256-CBC**.

### Fonctionnalités :
- Choix du pseudonyme à l'initialisation du client.
- Envoi et réception de messages en temps réel.
- Chiffrement AES-256 de tous les messages avant transmission réseau.
- Prise en charge de la commande `/quit` pour une déconnexion propre.
- Notifications temps réel lors de l'arrivée ou du départ d'un utilisateur (`X a rejoint / quitté le salon`).


## Outils installés Installés
python3 -m venv venv
source venv/bin/active
pip install websockets cryptographie
lancement des codes: server.py et client.py en local sur deux terminaux differents
