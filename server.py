import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Accept connections from any IP
PORT = 5555
clients = {}  # Dictionary to store client sockets and usernames
chat_history_file = "chat_history.txt"  # File to store chat history

# Function to Load Chat History
def load_chat_history():
    try:
        with open(chat_history_file, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

# Function to Save Message to History
def save_chat_history(message):
    with open(chat_history_file, "a") as file:
        file.write(message + "\n")

# Function to Broadcast Messages to All Clients
def broadcast(message, sender_socket=None):
    print(message)  # Print to server console
    save_chat_history(message)  # Save to history file
    for client in clients:
        if client != sender_socket:  # Don't send the message to the sender
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]

# Function to Handle Each Client
def handle_client(client_socket, addr):
    try:
        # Ask for a username
        client_socket.send("Enter your userusernamename: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        clients[client_socket] = username
        broadcast(f"{username} has joined the chat!", client_socket)

        # Send chat history to new user
        chat_history = load_chat_history()
        for line in chat_history:
            client_socket.send(line.encode('utf-8'))

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{username}: {message}", client_socket)
    
    except:
        pass

    # Remove client when they disconnect
    print(f"{clients[client_socket]} disconnected.")
    broadcast(f"{clients[client_socket]} has left the chat.")
    del clients[client_socket]
    client_socket.close()

# Function to Start the Server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
