import getpass
import os
import re
import socket
import argparse


username = getpass.getuser()
hostname = socket.gethostname()

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, help="Path to physical VFS")
parser.add_argument("--script", type=str, help="Path to start script")
args = parser.parse_args()

print("Path to VHS:", args.path)
print("Path to start script:", args.script)

def substitute_env_vars(s):
  # Создаёт захватывающую группу с именем переменной находя знак $ и буквы после него
  pattern = r'\$(\w+)'

  # Функция для обработки каждого совпадения
  def replace_match(match):
    var_name = match.group(1) # Содержимое группы (имя переменной)
    return os.environ.get(var_name, match.group(0))  # Получить значение, или если не получилось, вернуть название

  # Обработка регулярным выражением
  return re.sub(pattern, replace_match, s)

if (args.script):
    try:
        with open(args.script) as file:
            for line in file:
                line = line.strip()
                if (line == "exit"):
                    break
                elif (line == ""):
                    continue
                line = substitute_env_vars(line)
                if (line == "ls"):
                    print("ls")
                elif (line == "cd"):
                    print("cd")
                elif (line == "read"):
                    input()
                else:
                    print("Error: unknown command")
                    break
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    else:
        print("Error: unknown command")
        break
