import getpass
import os
import socket


username = getpass.getuser()
hostname = socket.gethostname()

while True:
    line = input(username + "@" + hostname + "$")
    if (line == "exit"):
        break
    elif (line == ""):
        continue
    elif (line == "ls"):
        print("ls")
    elif (line == "cd"):
        print("cd")
    elif (line[0] == "$"):
        var = os.getenv(line[1:])
        print(var)
