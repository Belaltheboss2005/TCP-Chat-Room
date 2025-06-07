# TCP-Based Chat Room Server with GUI

This project is a **TCP-based chat room server** with a graphical user interface (GUI) built using Python's `tkinter` library. Its main purpose is to allow multiple clients to connect to a central server and exchange messages in real time.

## Key Features and Functionality

- The server can be started with a selectable IP address:
  - `localhost`
  - Current local IP
  - Custom IP
- Manages multiple client connections using threads.
- Each client must provide a **unique nickname** to join.
- Messages from any client are **broadcast** to all connected clients.
- The server maintains and broadcasts a **list of online users**.
- The GUI:
  - Displays server events (connections, disconnections, etc.)
  - Provides buttons to **start or stop** the server.

## Summary

This project enables **real-time group chat** over a local network or the internet, with a simple **server-side GUI** for management.
