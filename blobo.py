import time
import threading
import serial
import pygame
#you'll need to set your serial port, do ls /dev/tty.* on a mac to list 'em
#ser = serial.Serial('/dev/tty.BALL-BluetoothSerialPort', 38400, timeout=1) 
ser = serial.Serial('/dev/tty.blobo', 38400, timeout=1) 
ser.write("A")      # open comms

pressure=0
readpressure=False

def readpressure():
    while True:
  	count = 0
		while 1:
			count +=1
			packet = ser.read(size=25) #read the 25 character packet
			packetlist = [ord(c) for c in packet] #turn it into human readable hex
			P_LSB = packetlist[16] #see http://www.neuroupdate.com/blobo/blobo.xls for key to fields
			P_MSB = packetlist[17]
			global pressure
			pressure = P_LSB + P_MSB * 256 #put the number back together
			readpressure=True
			#print pressure 
			if count>500:  #Blobo needs a 'keep alive' message
				ser.write(chr(13)) 
				count=0
		time.sleep(0)

t1 = threading.Thread(target=readpressure)
t1.daemon=True
t1.start()

while not readpressure:
	time.sleep(0.5)


pygame.init() 

width = 1200
height = 440
playheight=height-40
#create the screen
window = pygame.display.set_mode((width, height)) 

maxp=17000
#minp=14000
minp=pressure
position = 0.5
trace = []
xoffset=700
while True:
	#print pressure
	time.sleep(0.0001)
	#print 'new'
	#print pressure
	if pressure > maxp:
		maxp=pressure
	if pressure < minp:
		minp=pressure		

	position = playheight -(float(pressure-minp) / float(maxp-minp) * playheight)
	#print int(position)
	window.fill((0,0,0))
	#pygame.draw.circle(window, (255,0,0), (xoffset,int(position)), (10), 0)
	trace.insert(0,int(position))

	numtraces =500
	if (len(trace) < numtraces):
		numtraces = len(trace)

	for num in range(1,numtraces):
		#pygame.draw.circle(window, (0,255-(num/2),0), ((xoffset-(num*2)),trace[num]), (10), 0)
		colvalue=255-(num/1.5)
		if (colvalue < 0):
			colvalue=0
		pygame.draw.line(window, (0,colvalue,0), (((xoffset-((num-1)*2)),trace[num-1])), (((xoffset-(num*2)),trace[num])), 5)

	pygame.draw.circle(window, (255,0,0), (xoffset,int(position)), (10), 0)
	pygame.display.update() 


	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			ser.close()
			sys.exit(0) 
		#else: 
			#print event 

	#pass
