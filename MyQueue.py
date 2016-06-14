class node:
	
	# Node constructor
	def __init__(self, data = None, next_node = None):
		self.data = data
		self.next_node = next_node
	
	def GetData(self):
		return self.data
	
	def GetNext(self):
		return self.next_node
	
	def SetNext(self, new_node):
		self.next_node = new_node

class queue:
		
	def __init__(self, front = None, rear = None):
		self.front = front
		self.rear = rear
	
	def Enqueue(self, val):
		newnode = node(val)
		
		if self.front == None and self.rear == None:
			self.front = newnode
			self.rear = newnode
		else:
			self.rear.SetNext(newnode)
			self.rear = self.rear.GetNext()
			
	def Dequeue(self):
		delnode = self.front
		self.front = self.front.GetNext()
		delnode.SetNext(None)
		return delnode.GetData()
	
	def Count(self):
		now = self.front
		count = 0
		while now:
			count += 1
			now = now.GetNext()
		return count

'''	
cqueue = queue()
squeue = queue()

f1 = file("abc.docx", "rb")
print "Loading file into queue"
byte = f1.read(1024)
while byte != "":
	cqueue.Enqueue(byte)
	byte = f1.read(1024)

print "Transferring between queues"	
for x in range(0, cqueue.Count()):
	squeue.Enqueue(cqueue.Dequeue())

f2 = file("new_abc.docx", "wb")

print "Loading new file from queue"
for x in range(0, squeue.Count()):
	f2.write(squeue.Dequeue())
'''