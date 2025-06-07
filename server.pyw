import tkinter as tk
import socket
import threading
import sys

host = ''
port = 55555

def get_local_ip():
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Socket.connect(("8.8.8.8", 80))
        local_ip = Socket.getsockname()[0]
        Socket.close()
        return local_ip
    except Exception as e:
        print("Error getting local IP:", e)
        return None

def set_host_type(host_type):
    global host
    if host_type == 'localhost':
        host = '127.0.0.1'
    elif host_type == 'current_ip':
        host = get_local_ip()
    else:
        host = custom_ip_entry.get()
    host_window.destroy()
    main()

def host_window():
    global host_window, custom_ip_entry
    host_window = tk.Tk()
    host_window.title("Server IP")
    screen_width = host_window.winfo_screenwidth()
    screen_height = host_window.winfo_screenheight()

    # Set the window dimensions
    window_width = 300
    window_height = 250

    # Calculate the position to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    host_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    localhost_button = tk.Button(host_window, text="Localhost", command=lambda: set_host_type('localhost'))
    localhost_button.pack(pady=10)

    current_ip_button = tk.Button(host_window, text="Current IP", command=lambda: set_host_type('current_ip'))
    current_ip_button.pack(pady=10)

    custom_ip_label = tk.Label(host_window, text="Custom IP:")
    custom_ip_label.pack(pady=5)

    custom_ip_entry = tk.Entry(host_window)
    custom_ip_entry.pack(pady=5)

    custom_ip_button = tk.Button(host_window, text="Use Custom IP", command=lambda: set_host_type('custom_ip'))
    custom_ip_button.pack(pady=10)

    host_window.mainloop()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            if message.decode('utf-8') == "/leave":
                index = clients.index(client)
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                if len(clients) > 0:
                    broadcast('{} left!'.format(nickname).encode('utf-8'))
                print('{} left the chat.'.format(nickname))
                broadcast_online_users()
                break
            else:
                broadcast(message)
        except ConnectionResetError:
            print('{} connection closed unexpectedly.'.format(nickname))
            clients.remove(client)
            nicknames.remove(nickname)
            if len(clients) > 0:
                broadcast('{} left!'.format(nickname).encode('utf-8'))
            print('{} left the chat.'.format(nickname))
            broadcast_online_users()
            break
        except:
            print("An error occurred!")
            break

def broadcast_online_users():
    online_users = ','.join(nicknames)
    for client in clients:
        client.send(f'NICKLIST{online_users}'.encode('utf-8'))

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        text_area.config(state=tk.NORMAL)  # Make text area writable
        text_area.insert(tk.END, "Connected with {}\n".format(str(address)))
        text_area.config(state=tk.DISABLED)  # Make text area read-only

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        if nickname in nicknames:
            client.send("NICKRENICK".encode('utf-8'))
            print("Disconnected with {} due to choosing a username that already exists".format(str(address)))
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "Disconnected with {} due to choosing a username that already exists\n".format(str(address)))
            text_area.config(state=tk.DISABLED)
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        print("Username is {}".format(nickname))
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "Username is {}\n".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        broadcast_online_users()
        text_area.config(state=tk.DISABLED)

        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

def start_server():
    server_thread = threading.Thread(target=receive)
    server_thread.start()
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, "Server started.\n")
    text_area.config(state=tk.DISABLED)
    start_button.config(state=tk.DISABLED)

def stop_server():
    global clients, nicknames
    if stop_button.cget("text") == "Stop Server & Close Program":
        for client in clients:
            try:
                client.send("SERVERCLOSED".encode('utf-8'))
                client.close()
            except:
                continue
        server.close()
        print("Server stopped.")
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "Server stopped.\n")
        text_area.config(state=tk.DISABLED)
        root.quit()
    else:
        for client in clients:
            try:
                client.send("SERVERCLOSED".encode('utf-8'))
                client.close()
            except:
                continue
        server.close()
        print("Server stopped.")
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "Server stopped.\n")
        text_area.config(state=tk.DISABLED)
        stop_button.config(text="Stop Server & Close Program")
        root.quit()

def main():
    global server, clients, nicknames, root, text_area, start_button, stop_button
    clients = []
    nicknames = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    root = tk.Tk()
    root.title("Chat Server")
    root.geometry("400x300")

    text_area = tk.Text(root, height=10, width=50)
    text_area.pack(pady=10)
    text_area.config(state=tk.DISABLED)  # Make text area read-only by default

    button_frame = tk.Frame(root)
    button_frame.pack()

    start_button = tk.Button(button_frame, text="Start Server", command=start_server)
    start_button.pack(side=tk.LEFT, padx=10, pady=5, anchor="center")

    stop_button = tk.Button(button_frame, text="Stop Server & Close Program", command=stop_server)
    stop_button.pack(side=tk.LEFT, padx=10, pady=5, anchor="center")

    root.update_idletasks()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - root_width) // 2
    y = (screen_height - root_height) // 2
    root.geometry(f"{root_width}x{root_height}+{x}+{y}")

    root.mainloop()

host_window()
