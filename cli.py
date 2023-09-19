import socket
import threading
import sys
import datetime

with open("banner.txt", "r") as f:
    banner = f.read()
print(banner)

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
host = '127.0.0.1'
port = 12345

# Connect to the server on local computer
s.connect((host, port))

# Get the name of the client from the command line argument
name = sys.argv[1]

# Send the name to the server as the first message
s.send(name.encode())

# A function to receive messages from the server
def receive():
    while True:
        try:
            # Receive data from the server
            data = s.recv(1024)
            if not data:
                break
            # Print the data as a string
            print(data.decode())
        except:
            # Close the connection
            s.close()
            break

# Start a new thread to receive messages from the server
t = threading.Thread(target=receive)
t.start()

while True:
    # Get the input message from the user
    message = input()
    if message == "!quit":
        break
    # Get the current date and time
    now = datetime.datetime.now()
    # Send the message to the server with the name and date and time of the client
    s.send(("\033[92m[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] " + "[ #" + name + " ]\033[0m:" + message).encode())

# Close the connection
s.close()