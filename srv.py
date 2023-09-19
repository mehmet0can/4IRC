import socket
import threading
import sys

with open("banner.txt", "r") as f:
    banner = f.read()
print(banner)

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
host = '127.0.0.1'
port = 12345

# Bind to the port
s.bind((host, port))

# Put the socket into listening mode
s.listen(5)

# A list of connected clients
clients = []

# A function to broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# A function to handle each client connection
def handle_client(c):
    # Get the name of the client from the first message
    name = c.recv(1024).decode()
    # Broadcast the name to other clients
    broadcast(("\033[94m[ #" + name + " ] has joined the chat\033[0m").encode())
    while True:
        try:
            # Receive data from the client
            data = c.recv(1024)
            if not data:
                break
            # Broadcast the data to other clients
            broadcast(data)
        except:
            # Remove the client from the list and close the connection
            clients.remove(c)
            c.close()
            broadcast(("\033[91m[ #" + name + " ] has left the chat\033[0m").encode())
            break

print("Server is listening...")

while True:
    try:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)
        # Add the client to the list
        clients.append(c)
        # Start a new thread to handle the client
        t = threading.Thread(target=handle_client, args=(c,))
        t.start()
    except KeyboardInterrupt:
        # Close the socket and exit the program
        print("Server is shutting down...")
        broadcast("Server is shutting down...".encode())
        s.close()
        sys.exit(0)