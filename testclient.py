try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
	import tkinter as tk
	
import tkMessageBox
import ttk
import tkFont as font
from Tkinter import *
from tkFileDialog   import askopenfilename
import Tkconstants 

from MyQueue import node
from MyQueue import queue

import socket
import os
import threading
import shutil
import zipfile

LARGE_FONT= ("Verdana", 12)

s = socket.socket()

def Bind():
	host = '127.0.0.1'
	port = 6200
	
	global s
	s.connect((host, port))
	
	
def walk_dir(root_dir):
    """
    walks the specified directory root and all its subdirectories
    and returns a list of tuples containing all files with extension ext
    and their associated directory
    """
    file_list = []
    towalk = [root_dir]
    while towalk:
        root_dir = towalk.pop()
        for path in os.listdir(root_dir):
            full_path = os.path.join(root_dir, path).lower()
            if os.path.isfile(full_path) and (full_path.endswith(extension) or full_path.endswith(extension2) or full_path.endswith(extension3) or full_path.endswith(extension4) or full_path.endswith(extension5) or  full_path.endswith(extension6) or full_path.endswith(extension7)):
                # create list of (filename, dir) tuples
                file_list.append((path.lower(), root_dir))
            elif os.path.isdir(full_path):
                towalk.append(full_path)
    return file_list
def get_list(event):
    """
    function to read the listbox selection(s)
    (mutliple lines can be selected with ctrl/shift mouse clicks)
    and put the result(s) in a label
    """
    try:
        global selpath
        # tuple of line index(es)
        sel = listbox1.curselection()
        # get the text, might be multi-line
        selpath = [file_list[int(x)] for x in sel]
    except:
        info_label.config(text="Please select a file on the list")
def add_file():
    """
    add selected file(s) from listbox1 to listbox2
    keep track of the (filename, dir) tuple too
    """
    try:
        for path_tuple in selpath:
            listbox2.insert(END, path_tuple[0])
            # this list exists parallel to the listbox2
            # and contains the associated directory info
            fullpath_list.append(path_tuple)
        #print ">>>", fullpath_list  #test
    except NameError:
        info_label.config(text="Please select a file on the list")

def quit():
	global app
	app.destroy()
	#s.send('N')
	s.close()

class View(Listbox):
    def __init__(self, master):
        Listbox.__init__(self, master)		
		

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
		
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (mainpage, uploadpage,downloadpage):
		frame = F(container, self)
		frame.configure(background = "black")

		self.frames[F] = frame

		frame.grid(row=0, column=0, sticky="news")

		self.show_frame(mainpage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
		
	
	
class mainpage(tk.Frame):
	
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

		
	#font11 = font.Font(family='Helvetica', size=15, weight = 'bold')
	font12 = font.Font(family='Helvetica', size=15)
	

	label = tk.Label(self, text="Welcome to Jalebi File Transfer software.", fg = 'green', bg = 'black')
	label.place(x=50, y=20)
	
	Bind()

	button = tk.Button(self, text="Upload",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue",command=lambda: controller.show_frame(uploadpage) )
	button.place(x=200, y=80)
	button2 = tk.Button(self, text="Download",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue",command=lambda: controller.show_frame(downloadpage))
	button2.place(x=190, y=150)
	button3 = tk.Button(self, text="Quit",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue", command= quit)
	button3.place(x=215, y=220)
	font11 = font.Font(family='Helvetica', size=15, weight='bold')
	button['font'] = font11
	button2['font'] = font11
	label['font'] = font11
	button3['font'] = font11 
	



class uploadpage(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label1 = tk.Label(self, text="Select the file you want to upload", fg = 'green', bg = 'black')
		label1.place(x=100, y=60)
		font12 = font.Font(family='Helvetica', size=12)
		label1['font'] = font12
		button = tk.Button(self, text="Choose file",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue", command = self.browse)
		button.place(x=180, y=110)
		button['font'] = font12
		
		button = tk.Button(self, text="Back",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue",command=lambda: controller.show_frame(mainpage))
		button.place(x=50, y=160)
		button['font'] = font12
		button = tk.Button(self, text="Upload",  activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue",command=self.Upfile)
		button.place(x=350, y=160)
		button['font'] = font12
		
		self.listbox1 = Listbox(self, width=70, height=6, selectmode=EXTENDED)
		self.listbox1.grid(padx= 30, pady= 210)
		
		self.name = ""
		self.filesize = 0
		self.totalSent = 0
	
	
	def browse(self):
		self.name= askopenfilename()
		
		if self.name == "":
			return
		
		self.listbox1.delete(0, END)
		(head, tail) = os.path.split(self.name)
		self.filesize = str(os.path.getsize(self.name))
		self.listbox1.insert(END, "Filename: " + tail)
		self.listbox1.insert(END, "Filesize: " + self.filesize)
		
		(root, ext) = os.path.splitext(tail)
		s.send('1')
		if ext != ".zip":
			s.send(tail.replace(ext, ".zip"))
		else:	
			s.send(tail)
		
	def Upfile(self):
		(head, tail) = os.path.split(self.name)
		(root, ext) = os.path.splitext(tail)
		if ext != ".zip":
			print "Original filesize: " + self.filesize
			os.mkdir("temp")
			zip_folder = tail.replace(ext, "")
			name = tail.replace(ext, ".zip")
			file1 = open("C:\Users\M.Ali\Desktop\Project\\final\\Client\\temp\\" + str(tail), "wb")
			file2 = open(self.name, "rb")
			shutil.copyfileobj(file2, file1)
			file1.close()
			file2.close()
			shutil.make_archive(zip_folder, "zip", "temp")
			os.remove("C:\Users\M.Ali\Desktop\Project\\final\\Client\\temp\\" + str(tail))
			os.rmdir("temp")
			filesize =  str(os.path.getsize(name))
			print "Compressed filesize: " + filesize
			s.send(str(os.path.getsize(name)))
			self.filesize = os.path.getsize(name)
			file2 = open(name, "rb")
		else:
			s.send(self.filesize)
			file2 = open(self.name, "rb")
		
		self.totalSent = 0
		upqueue = queue()
		bytesToSend = file2.read(1024)
		upqueue.Enqueue(bytesToSend)
		self.totalSent = len(bytesToSend)
		while bytesToSend != "":
			bytesToSend = file2.read(1024)
			upqueue.Enqueue(bytesToSend)
			self.totalSent += len(bytesToSend)
			self.listbox1.insert(END, "{0:.2f}".format((self.totalSent/float(self.filesize)*100))+ "% Done")
			self.listbox1.yview(END)
		self.listbox1.insert(END, "Upload complete")
		self.listbox1.yview(END)
		file2.close()
		
		for x in range(0, upqueue.Count()):
			s.send(upqueue.Dequeue())

class downloadpage(tk.Frame):
	def __init__(self, parent, controller):
			tk.Frame.__init__(self, parent)
			font12 = font.Font(family='Helvetica', size=12)
			font13 = font.Font(family='Helvetica', size=14)
			label1 = tk.Label(self, text="Select the file you want to download", fg = 'green', bg = 'black')
			label1.place(x=10, y=10)
			label1['font'] = font13
			
			self.listbox1 = Listbox(self, width=60, height=14, selectmode=SINGLE)
			self.listbox1.grid(padx= 30, pady= 50)
						
			add_button = Button(self, text='Download file',activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue", command=self.DownFile)
			add_button.place(x=300, y=300)
			add_button['font'] = font12
			
			add_button = Button(self, text='Retrieve file',activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue", command=self.RetrieveFile)
			add_button.place(x=130, y=300)
			add_button['font'] = font12
			
			add_button = Button(self, text='Back',activebackground="Blue", activeforeground="yellow", fg = "red", highlightcolor = "blue", command=lambda: controller.show_frame(mainpage))
			add_button.place(x=30, y=300)
			add_button['font'] = font12
			
			self.value = ""
			
	def CurSelet(self, evt):
		self.value = str(self.listbox1.get(self.listbox1.curselection()))
		newstr = self.value.replace("\n", "")
		print newstr
		
	def RetrieveFile(self):
		s.send('2')
		RecvFile = s.recv(1024)
		
		f2 = open("files.txt", "w")
		f2.write(RecvFile)
		f2.close()
		self.listbox1.delete(0, END)
		file_list = open("files.txt").readlines()
		for file in file_list:
			self.listbox1.insert(END, file)
		
		file_num = len(file_list)
		
		self.listbox1.bind('<<ListboxSelect>>', self.CurSelet)
		
	def DownFile(self):
		newstr = self.value.replace("\n", "")
		s.send(newstr)
		fsize = s.recv(1024)
		print "Compressed filesize: " + fsize
		data = s.recv(1024)
		downqueue = queue()
		downqueue.Enqueue(data)
		totalRecv = len(data)
		self.listbox1.delete(0, END)
		while totalRecv < long(fsize):
			data = s.recv(1024)
			totalRecv += len(data)
			downqueue.Enqueue(data)
			self.listbox1.insert(END, "{0:.2f}".format((totalRecv/float(fsize))*100)+ "% Done")
			self.listbox1.yview(END)
		self.listbox1.insert(END, "Download Complete!")
		self.listbox1.yview(END)
		 
		(root, ext) = os.path.splitext(newstr)
		if ext != ".zip":
			name = newstr.replace(ext, ".zip")
			f = open(name, 'wb')
		else:	
			f = open(newstr, "wb")
			
		for x in range(0, downqueue.Count()):
			f.write(downqueue.Dequeue())
		
		f.close()
		
		zfile = zipfile.ZipFile(newstr.replace(ext, ".zip"))
		zfile.extractall()
		zfile.close()
		
		os.remove(newstr.replace(ext, ".zip"))
		
		print "Decompressed filesize: " + str(os.path.getsize(newstr))
		
		
app = SeaofBTCapp()

w = 470
h = 350
x = 100
y = 200
app.geometry("%dx%d+%d+%d" % (w, h, x, y))
app.title("Jalebi File Transfer Software")

app.mainloop()