import os
import shlex
import subprocess

def execute_command(command):
    try:
        # Split the command into parts
        parts = shlex.split(command)
        
        # Handle piping
        if '|' in parts:
            commands = [part.strip() for part in command.split('|')]
            processes = []
            for i, cmd in enumerate(commands):
                parts = shlex.split(cmd)
                if i == 0:
                    # First command
                    p = subprocess.Popen(parts, stdout=subprocess.PIPE)
                else:
                    # Subsequent commands
                    p = subprocess.Popen(parts, stdin=processes[-1].stdout, stdout=subprocess.PIPE)
                processes.append(p)
            output, error = processes[-1].communicate()
            return output.decode(), error
        else:
            # Handle input redirection
            if '<' in parts:
                input_index = parts.index('<')
                input_file = parts[input_index + 1]
                with open(input_file, 'r') as file:
                    input_data = file.read()
                parts = parts[:input_index]
                p = subprocess.Popen(parts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = p.communicate(input=input_data.encode())
            # Handle output redirection
            elif '>' in parts:
                output_index = parts.index('>')
                output_file = parts[output_index + 1]
                parts = parts[:output_index]
                with open(output_file, 'w') as file:
                    p = subprocess.Popen(parts, stdout=file, stderr=subprocess.PIPE)
                    _, error = p.communicate()
                output = ""
            else:
                p = subprocess.Popen(parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = p.communicate()
            
            return output.decode(), error.decode()
    except Exception as e:
        return "", str(e)

def main():
    while True:
        command = input("shell> ")
        if command.lower() in ['exit', 'quit']:
            break
        output, error = execute_command(command)
        if output:
            print(output, end='')
        if error:
            print(error, end='')

if __name__ == "__main__":
    main()
