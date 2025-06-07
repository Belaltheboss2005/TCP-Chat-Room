# ##########################################################33


import socket
import threading
import datetime
import tkinter as tk
from tkinter import messagebox

# Function to get the current timestamp
def get_current_timestamp():
    return (datetime.datetime.now().time()).strftime("%H:%M:%S")

def show_error_message(nickname):
    message = "Someone else is using this username ({}). Please restart the program and choose another one.".format(nickname)
    messagebox.showerror("Username Error", message)

def check_message(message, nickname, client, root):
    if message == "NICKRENICK":
        show_error_message(nickname)
        client.close()
        root.destroy()
        exit()

# Function to handle leaving the chat
def leave_chat():
    client.send("/leave".encode('utf-8'))
    root.destroy()  # Close the window
    exit()  # Exit the program

# Function to handle receiving messages from the server
# Function to handle receiving messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('NICKLIST'):
                update_user_list(message[8:])
            elif message == 'NICK':
                client.send(nickname.encode('utf-8'))
                message = client.recv(1024).decode("utf-8")
                if message == "NICKRENICK":
                    check_message(message, nickname, client, root)
            else:
                chat_box.config(state=tk.NORMAL)  # Enable chat box for inserting messages
                chat_box.insert(tk.END, message + '\n')  # Insert the message into the chat box
                chat_box.config(state=tk.DISABLED)  # Disable chat box after inserting message
        except ConnectionResetError:
            chat_box.config(state=tk.NORMAL)  # Enable chat box for inserting messages
            chat_box.insert(tk.END, "Disconnected from server.\n")
            chat_box.config(state=tk.DISABLED)  # Disable chat box after inserting message
            messagebox.showerror("Connection Error", "Disconnected from server.")
            root.destroy()  # Close the window
            exit()  # Exit the program
            break
        except:
            break


# Function to update the user list
def update_user_list(user_list):
    online_users.delete(0, tk.END)
    users = user_list.split(',')
    for user in users:
        online_users.insert(tk.END, user)

# Function to handle sending messages to the server
def write(event=None):
    message_text = message_entry.get()
    if message_text == "/leave":
        client.send("/leave".encode('utf-8'))
        root.destroy()  # Close the window
        exit()  # Exit the program
    else:
        timestamp = get_current_timestamp()
        message = '{} {}: {}'.format(timestamp, nickname, message_text)
        client.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)  # Clear the message entry field after sending

# Function to handle username entry and open the main chat window
def enter_username(event=None):
    global nickname
    nickname = username_entry.get()
    if nickname:
        username_window.destroy()
        open_chat_window()

# Function to open the main chat window
def open_chat_window():
    global client, chat_box, message_entry, online_users, receive_thread
    # Set up the socket connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 55555))  # Connect to the server IP entered by the user

    # Create the GUI window
    global root
    root = tk.Tk()
    root.title("Chat Client")

    # Create a frame to contain the message entry field, send button, and online users list
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Create and configure the chat display area with scrollbar
    chat_frame = tk.Frame(right_frame)
    chat_frame.pack(side=tk.LEFT, fill=tk.Y)

    chat_box = tk.Text(chat_frame, height=root.winfo_screenheight() // 20, width=50)
    chat_box.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    chat_box.config(state=tk.DISABLED)  # Make the chat box read-only

    scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_box.config(yscrollcommand=scrollbar.set)

    # Create and configure the online users listbox
    online_users_label = tk.Label(right_frame, text="Online Users")
    online_users_label.pack()
    online_users = tk.Listbox(right_frame, height=10, width=20)
    online_users.pack(padx=10, pady=5)

    # Create and configure the message entry field
    message_entry = tk.Entry(right_frame, width=50)  # Adjust width as needed
    message_entry.pack(padx=10, pady=5)
    message_entry.bind("<Return>", write)  # Bind the Enter key to the write function

    # Create and configure the send button
    send_button = tk.Button(right_frame, text="Send", command=write)  # Remove state=tk.DISABLED
    send_button.pack(padx=10, pady=5)

    # Create and configure the leave button
    leave_button = tk.Button(right_frame, text="Leave", command=leave_chat)
    leave_button.pack(padx=10, pady=5)

    # Label to display username
    username_label = tk.Label(root, text=f"Username: {nickname}")
    username_label.pack(side=tk.TOP, padx=10, pady=10)

    # Start the receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Start the Tkinter event loop
    root.mainloop()

# Function to handle server IP entry and open the username entry window
def enter_server_ip(event=None):
    global server_ip
    server_ip = server_ip_entry.get()
    if server_ip:
        server_ip_window.destroy()
        open_username_window()

# Function to open the server IP entry window
def open_server_ip_window():
    global server_ip_window, server_ip_entry
    server_ip_window = tk.Tk()
    server_ip.title("Chat Client")#first commit
    server_ip_window.title("Enter Server IP")

    server_ip_label = tk.Label(server_ip_window, text="Enter the server IP:")
    server_ip_label.pack(padx=10, pady=10)

    server_ip_entry = tk.Entry(server_ip_window, width=30)
    server_ip_entry.pack(padx=10, pady=5)
    server_ip_entry.bind("<Return>", enter_server_ip)  # Bind the Enter key to the enter_server_ip function

    server_ip_button = tk.Button(server_ip_window, text="Connect", command=enter_server_ip)
    server_ip_button.pack(padx=10, pady=10)

    # Calculate the position of the window to place it in the middle of the screen
    screen_width = server_ip_window.winfo_screenwidth()
    screen_height = server_ip_window.winfo_screenheight()
    window_width = 300
    window_height = 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    server_ip_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start the Tkinter event loop for the server IP entry window
    server_ip_window.mainloop()

# Function to open the username entry window
def open_username_window():
    global username_window, username_entry
    username_window = tk.Tk()
    username_window.title("Enter Username")

    username_label = tk.Label(username_window, text="Enter your username:")
    username_label.pack(padx=10, pady=10)

    username_entry = tk.Entry(username_window, width=30)
    username_entry.pack(padx=10, pady=5)
    username_entry.bind("<Return>", enter_username)  # Bind the Enter key to the enter_username function

    username_button = tk.Button(username_window, text="Enter", command=enter_username)
    username_button.pack(padx=10, pady=10)

    # Calculate the position of the window to place it in the middle of the screen
    screen_width = username_window.winfo_screenwidth()
    screen_height = username_window.winfo_screenheight()
    window_width = 300
    window_height = 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    username_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start the Tkinter event loop for the username entry window
    username_window.mainloop()

# Open the server IP entry window first
open_server_ip_window()
