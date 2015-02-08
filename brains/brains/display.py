#!/usr/bin/env python

import dot3k.lcd as lcd
import backlight as backlight
import socket
import fcntl
import struct
import time, datetime
import math
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

myIP = get_ip_address('eth0')
myIP = " " * (15 - len(myIP)) + myIP

#pacman = [
#	[0x0e,0x1f,0x1d,0x1f,0x18,0x1f,0x1f,0x0e],
#	[0x0e,0x1d,0x1e,0x1c,0x18,0x1c,0x1e,0x0f]
#]

heart = [
	[0x00,0x0a,0x1f,0x1f,0x1f,0x0e,0x04,0x00],
	[0x00,0x00,0x0a,0x0e,0x0e,0x04,0x00,0x00],
	[0x00,0x00,0x00,0x0e,0x04,0x00,0x00,0x00],
	[0x00,0x00,0x0a,0x0e,0x0e,0x04,0x00,0x00]
	]

def getAnimFrame(char,fps):
	return char[ int(round(time.time()*fps) % len(char)) ]

class Light:
	def __init__(self):
		self.count = 0
		self.increment = 1
	
	def animate(self):
		self.set_light(self.count)
		self.count = self.count + self.increment
	
		if self.count == 6:
			self.increment = -1
		elif self.count == 0:
			self.increment = 1
			
	def set_light(self, index):
		top1 = 0
		top2 = 0
		top3 = 0
	
		if index < 7:
			top1 = index
			top2 = index + 1
			top3 = index + 2
		else:
			top1 = index - 2
			top2 = index - 1
			top3 = index

		for i in range(top1):
			backlight.set(9 + i, 0)
	
		backlight.set(9 + top1, 150)
		backlight.set(9 + top2, 150)
		backlight.set(9 + top3, 150)
		
		for i in range(top3 + 1, 9):
			backlight.set(9 + i, 0)
			
class Colour:
	def __init__(self):
		self.hue = 0.0

	def animate(self):
		self.hue += 0.008
		backlight.sweep(self.hue)
		if self.hue > 1.0:
			self.hue = 0.0
			
class Message:
	def __init__(self, line):
		self.display_width = 16
		self.line = line
		self.message_position = 0
		# Set slower text speed
		self.progress = True
		self.message = "Nada nuevo"
		self.last_check = 0
		self.get_messages()
		
	def get_db_connection(self):
		client = None
		try:
			client = MongoClient()
		except ConnectionFailure, e:
			return None
		return client

	def decorate_error(self, error, count):
		return "Error %i: %s " % (count, error) 
	
	def decorate_warning(self, warning, count):
		return "Warning %i: %s " % (count, warning)

	def get_db_messages(self):
		self.last_check = time.time()
		
		client = self.get_db_connection()
	
		if client is None:
			return self.decorate_error("No es posible conectarse a la base de datos")
			return 
		
		db = client.messages
	
		errors = db.errors.find()
		warnings = db.warnings.find()
	
		messages = ""
		
		count = 1
		
		for error in errors:
			messages += self.decorate_error(error["text"], count)
			count = count + 1
		
		for warning in warnings:
			messages += self.decorate_warning(warning["text"], count)
			count = count + 1
		
		return messages
		
	def get_messages(self):
		now = time.time()
		difference = int(now - self.last_check)
		
		if difference < 60:
			return
			
		db_messages = self.get_db_messages()
		
		if db_messages != self.message:
			self.message = db_messages
			self.message_position = 0
		
	def animate(self):	
		self.get_messages()
		
		message_portion = self.message[self.message_position : self.message_position + self.display_width]
		message_portion = message_portion + " " * (self.display_width - len(message_portion))
		lcd.set_cursor_position(0, self.line)
		lcd.write(message_portion)
	
		if self.progress:
			self.message_position = self.message_position + 1
		
		self.progress = not self.progress
	
		if self.message_position >= len(self.message):
			self.message_position = 0
			
class Time:
	def __init__(self, line):
		self.line = line
		clock = [
			[0xff,0x0a,0x0a,0x04,0x04,0x0a,0xee,0xff]
		]
		lcd.create_char(1, getAnimFrame(clock, 3))
		
	def show(self):
		lcd.set_cursor_position(0, self.line)
		t = datetime.datetime.now().strftime(" %d/%m %H:%M:%S")
		lcd.write(chr(1) + t)

lcd.clear()
lcd.write(chr(0) + myIP)

colour = Colour()
light = Light()
message = Message(line = 2)
_time = Time(line = 1)

while True:
	lcd.create_char(0, getAnimFrame(heart, 4))
	
	_time.show()
	colour.animate()
	light.animate()
	message.animate()
	
	time.sleep(0.1)