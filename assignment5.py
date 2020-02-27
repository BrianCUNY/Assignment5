#! /usr/bin/env python3

#IS211 Assignment 5

import argparse
import urllib.request
import urllib.error
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='Input a URL for a CSV file.')
parser.add_argument('-s', '--servers', help='Input numver of servers.')
args = parser.parse_args()

def downloadData(url):
#Opens the url link that is supplied
	datafile = urllib.request.urlopen(url)
	return datafile

class Queue:
	#Stores data as a queue abstract
	def __init__(self):
		self.items = []
		
	def is_empty(self):
		return self.items == []
		
	def enqueue(self):
		self.items.insert(0, item)
		
	def dequeue(self):
		return self.items.pop()
		
	def size(self):
		return len(self.items)
		
class Server(object):
	#A class for a computer server
	def __init__(self):
		self.current_task = None
		self.time_remaining = 0
	
	def tick(self):
		if self.current_task != None:
			self.time_remaining = self.time_remaining - 1
			if self.time_remaining <= 0:
				self.current_task = None
	
	def busy(self):
		if self.current_task != None:
			return True
		else:
			return False
	
	def start_next(self, new_task):
		self.current_task = new_task
		self.time_remaining = new_task.get_time()
		
class Request(object):
	#A class for a request that sends to the server via objects from SimulateOneServer
	def __init__(self, req_sec, process_time):
		self.timestamp = req_sec
		self.process_time - process_time
	
	def get_stamp(self):
		return self.timestamp
	
	def get_time(self):
		return self.process_time
		
	def wait_time(self, current_time):
		return current_time - self.timestamp
	
def simulateOneServer(datafile):
	#Operates a list of requests from the csv file by each row
	#Adds process time back into queue based on time left in process
	readfile = csv.reader(datafile)
	lab_server = Server()
	server_queue = Queue()
	waiting_times = []
	
	for line in readfile:
		req_sec = int(line[0])
		process_time = int(line[2])
		task = Request(req_sec, process_time)
		server_queue.enqueue(task)
		
		if (not lab_server.busy()) and (not server_queue.is_empty()):
			next_task = server_queue.dequeue()
			waiting_times.append(next_task.wait_time(req_sec))
			lab_server.start_next(next_task)
	
		lab_server.tick()
	average_wait = sum(waiting_times) / len(waiting_times)
	
	print('Average wait %6.2f secs %3d tasks remaining.' % 
	(average_wait, server_queue.size()))
	
def main():
	#Combines the above programs into one
	if not args.url:
		raise SystemExit
	try:
		datafile = downloadData(args.url)
	except urllib.URLError:
		print('Enter a valid link')
		raise
	else:
		if not args.servers:
			simulateOneServer(datafile)

if __name__ == '__main__':
	main()
