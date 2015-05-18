###############################################################################################
# Author:	Anastasios Monachos (secuid0) - [anastasiosm(at)gmail(dot)com]
# Usage: 	python portsense.py -t 192.168.2.100 -f /tmp/ports
# Purpose: 	Simple script to quickly connect to server with excessive number of open ports.
# Warning:	Dont rely, only, at the results of this script.
# Version: 	0.1
###############################################################################################
import socket
import sys 
import argparse
from threading import Thread

sys.tracebacklimit = 0
thread_counter = 0

parser = argparse.ArgumentParser(description='[i] Feed it with an ip/domain and a file with ports numbers (one port per line) to connect to, send a command eg "HELP" and give you back the response')
parser.add_argument('-t', metavar='target', help='Target IP or Domain', required=True)
parser.add_argument('-f', metavar='file', help='Filename with port numbers to connect to', required=True)
try:
	results = parser.parse_args()
	host_to_connect_to = results.t
	file_to_open = results.f
except IOError, msg:
	parser.error(str(msg))

commands = ['HELP\r\n', 'GET\r\n']

f = open(file_to_open,'r')

def connect_and_fetch(port, command):
	try:
 		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 		s.settimeout(5) #5 seconds
	except (socket.error, socket.timeout):
   		print "[-] Socket creation failed while in IP:%s port:%s command:%s " %(host_ip,port,command)
	
	try:
	    host_ip = socket.gethostbyname(host_to_connect_to)
	except socket.gaierror:
		# could not resolve the host
		print "[-] There was an error resolving the host"
	   	sys.exit()

	s.connect((host_ip, port))
	print ("\n[+] Successfully connected to ip/hostname %s on port %s" %(host_ip, port))
	s.sendall(command);
	reply = s.recv(65565)
	print ("\n[+] Reply from ip/hostname %s on port %s with command %s" %(host_ip, port, command))
	print reply
	s.close()

for port in f.readlines():
		for i in range(len(commands)):
			thread_counter += 1
			print "Thread counter %s details: %s %s %s" %(thread_counter, host_to_connect_to, int(port), commands[i])
			t = Thread(target=connect_and_fetch, args=(int(port),commands[i]),)
			t.start()

f.close()
