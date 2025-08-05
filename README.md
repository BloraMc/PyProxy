# PyProxy – Lightweight Python Self-Hosted Messaging App

**PyProxy** is a simple, lightweight messaging platform written in Python.  
It’s designed to be easy to run — no accounts, no databases, just messaging via unique 6-digit IDs.

**PyProxy** is fully self-hosted; there are no official **PyProxy** servers.

---

## Features

- Simple & minimalistic codebase  
- Private messaging between PyProxy users (note: the server can intercept messages, so host it on a **private** machine)  
- 6-digit ID system to connect users  

---

## Files

- `server.py` – Run this on a Python server to host your PyProxy instance  
- `client.py` – Connects to the server and uses IDs to message other PyProxy users on the same server  

---

## How It Works

1. Run `server.py` on your Python hosting platform (no external dependencies)  
   → You’ll see a connection address like `perso.lystech.org:24865`  
   → Remember the IP/domain (`perso.lystech.org`) and the port (`24865`)  

2. Open `client.py` in an IDE like VSCode and update the server IP and port at the top of the code  

3. Run `client.py` on your PC (no dependencies needed)  

4. Share your PyProxy ID with friends who also run the client configured for your server — use the ID to send messages  

> Make sure you're using **Python 3.x**

---

_Created by BloraMc in France_
