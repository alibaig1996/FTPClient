import socket
import os
from os import listdir
from os.path import isfile, join
import threading
import shutil
import zipfile

from MyQueue import queue
from MyQueue import node

def MaintainConnection(name, conn, a): #{
	while True:
		value = conn.recv(1024)
		
		if value == 'N':
			print "Client disconnected ip:<" + str(a) + ">"
			break
			
		elif value == '1':
			t2 = threading.Thread(target=UpFile, args=("GetThread", conn, a))
			t2.start()
			t2.join()
		
		elif value == '2':
			t1 = threading.Thread(target=RetrFile, args=("RetrThread", conn, a))
			t1.start()
			t1.join()
			
	conn.close()
#}
	
def RetrFile(name, sock, a): #{
	
	if os.path.isfile("file.txt"):
		os.remove("file.txt")
	
	mypath = "C:\Users\M.Ali\Desktop\Project\\final\\Server"
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	f1 = open("C:\Users\M.Ali\Desktop\Project\\final\\Server\\file.txt", "a")
	i = 0
	for x in onlyfiles:
		f1.write(onlyfiles[i] + "\n")
		i += 1
	f1.close()
	f1 = open("C:\Users\M.Ali\Desktop\Project\\final\\Server\\file.txt", "r")
	listpage = f1.read()	
	sock.send(listpage)
	
	filename = sock.recv(1024)
	#print filename
	
	(root, ext) = os.path.splitext(filename)
	
	if ext != ".zip":
		os.mkdir("temp")
		zip_folder = filename.replace(ext, "")
		name = filename.replace(ext, ".zip")
		file1 = open("C:\Users\M.Ali\Desktop\Project\\final\\Server\\temp\\" + str(filename), "wb")
		file2 = open(filename, "rb")
		shutil.copyfileobj(file2, file1)
		file1.close()
		file2.close()
		shutil.make_archive(zip_folder, 'zip', "temp")
		os.remove("C:\Users\M.Ali\Desktop\Project\\final\\Server\\temp\\" + str(filename))
		os.rmdir("temp")
		filesize =  str(os.path.getsize(name))
		#print filesize
		sock.send(str(os.path.getsize(name)))
		file2 = open(name, "rb")
	else:
		filesize =  str(os.path.getsize(filename))
		#print filesize
		sock.send(str(os.path.getsize(filename)))
		file2 = open(filename, "rb")
	
	downqueue = queue()
	bytesToSend = file2.read(1024)
	downqueue.Enqueue(bytesToSend)
	while bytesToSend != "":
		bytesToSend = file2.read(1024)
		downqueue.Enqueue(bytesToSend)
	file2.close()
	
	if ext != ".zip":
		os.remove(filename.replace(ext, ".zip"))

	for x in range(0, downqueue.Count()):
		sock.send(downqueue.Dequeue())
	
	print "Client downloaded file ip:<" + str(a) + ">"
#}
	
def UpFile(name, sock, a): #{
	filename = sock.recv(1024)
	filesize = long(sock.recv(1024))
	upqueue = queue()
	
	data = sock.recv(1024)
	upqueue.Enqueue(data)
	totalRecv = len(data)
	
	while totalRecv < filesize:
		data = sock.recv(1024)
		totalRecv += len(data)
		upqueue.Enqueue(data)
	
	f = open(filename, "wb")
	
	for x in range(0, upqueue.Count()):
		f.write(upqueue.Dequeue())
		
	f.close()
	
	zfile = zipfile.ZipFile(filename)
	zfile.extractall()
	zfile.close()
	os.remove(filename)
	
	print "Client uploaded file ip:<" + str(a) + ">"
#}		

def Main(): #{
	s = socket.socket()
	s.bind(('', 6200))
	s.listen(5)
	print "Server started!"
	while True:
		(c, addr) = s.accept()
		print "Client connected ip:<" + str(addr) + ">"
		t = threading.Thread(target=MaintainConnection, args=("MaintainThread", c, addr))
		t.start()

	s.close()
#}

if __name__ == '__main__': #{
	Main()
#}	