import socket
import threading
import os

# Server Configuration
HOST = '127.0.0.1'  # Change this to your server's IP if remote
PORT = 5555

username_file = "username.txt"

def get_saved_username():
    """Load the username from file if it exists."""
    if os.path.exists(username_file):
        with open(username_file, "r") as file:
            return file.read().strip()
    return None

def save_username(username):
    """Save the username to a file."""
    with open(username_file, "w") as file:
        file.write(username)

# Function to Receive Messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print("\n" + message)
        except:
            print("Disconnected from server.")
            break

# Function to Start the Client
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Check if we already have a saved username
    username = get_saved_username()
    if not username:
        username = input("Enter your username: ")
        save_username(username)
    else:
        print(f"Using saved username: {username}")
    
    # Send the username to the server
    client.send(username.encode('utf-8'))

    # Start thread to receive messages
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    # Send messages
    while True:
        try:
            message = input("")
            if message.lower() == "exit":
                break
            client.send(message.encode('utf-8'))
        except:
            break

    client.close()

if __name__ == "__main__":
    start_client()