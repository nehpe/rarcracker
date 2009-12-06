#!/usr/bin/python
#
# Python RAR Cracker -- Brute force recovery of passwords for .RAR files
# by Steve Gricci (deepcode.net)

import math
import subprocess
import sys
from threading import Thread
import time

#define
p_type = 'alphanumeric'
p_file = ''


class RARCrack(Thread):
	def __init__(self,offset,count):
		Thread.__init__(self)
		self.offset = offset
		self.count = count
		return

	def encrypt(self, N):
            global p_type
            if (p_type == "numeric"):
                return N
            if (p_type == "alphanumeric"):
                possible_chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
			'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
			'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
			'W', 'X', 'Y', 'Z']
            if (p_type == "alpha"):
                possible_chars = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
			'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
			'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
			'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
			'W', 'X', 'Y', 'Z']

            radix = len(possible_chars)
            encoded_text = ""
            Q = math.floor(math.fabs(N))
            remainder = "";
            while(Q != 0):
            	remainder = Q % radix
            	newDigit = possible_chars[int(remainder)]
            	encoded_text = newDigit + encoded_text
            	Q = ((Q-remainder)/radix)
            return encoded_text

	def run(self):
		global count
		global current_pwd
		global good_password
                global p_file
		i = self.count
		while(1):
			if (good_password != None):
				sys.exit()
			count += 1
			pwd = self.encrypt(i)
			current_pwd = pwd
			
			output = subprocess.Popen([r"unrar","t", "-p%s" % ( pwd ), p_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
			if (output.find("All OK") != -1):
				print 'found good password: %s' % ( pwd )
				good_password = 1
			i += self.offset 
			

		return

class Status(Thread):
	def __init__(self, quitter_thread):
		Thread.__init__(self)
		self.quitter_thread = quitter_thread
		return
	def run(self):
		global current_pwd
		global count
		global good_password
		while (1):
                    time.sleep(1)
                    if (good_password != None):
                        sys.exit()
                    print "Probing: '%s' %d/sec" % ( current_pwd, count )
                    count = 0
		return


class ExitChecker(Thread):
	def __init__(self):
		Thread.__init__(self)
		return
	def run(self):
		global good_password
		while(1):
			s = raw_input("Press 'q' then enter to quit\n")
			if (s.lower() == 'q'):
				good_password = 1
				sys.exit()

class ArgumentParser:
    def __init__(self):
        self.args = sys.argv
    def parse(self):
        global p_type
        global p_file
        del self.args[0]
        for index in range(len(self.args)):
            if (self.args[index] == "-t"):
                p_type = self.args[index+1]
            if (self.args[index].lower().find(".rar") != -1):
                p_file = self.args[index]
        return

if __name__ == "__main__":
    argp = ArgumentParser()
    argp.parse()

    count = 0
    current_pwd = "0"
    good_password = None
    quitter = ExitChecker()
    quitter.setDaemon(True)
    quitter.start()
    status = Status(quitter)
    status.start()
    crackers = []
    cracker = RARCrack(2,1)
    crackers.append(cracker)
    cracker.start()
    cracker = RARCrack(2,2)
    crackers.append(cracker)
    cracker.start()
