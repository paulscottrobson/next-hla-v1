# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		elements.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		9th December 2018
#		Purpose :	Element parsing classe
#
# ***************************************************************************************
# ***************************************************************************************

from errors import *
from streams import *
import os,re

# ***************************************************************************************
#									Element parser
# ***************************************************************************************

class ElementParser(object):
	def __init__(self,stream):
		self.stream = stream
		self.elementHeld = None
	#
	#		Get the next element
	#
	def get(self):
		if self.elementHeld is not None:
			element = self.elementHeld
			self.elementHeld = None
			return element
		ch = self.stream.get().lower()
		if ch == " ":
			return self.get()
		#
		#		Quoted string
		#
		if ch == '"':
			string = ""
			ch = self.stream.get()
			while ch != '"':
				if ch == "":
					raise CompilerException("Missing closing quote for string")
				string = string + ch
				ch = self.stream.get()
			return '"'+string+'"'
		#
		#		Integer
		#
		if ch >= '0' and ch <= '9':
			n = int(ch,10)
			ch = self.stream.get()
			while ch >= "0" and ch <= "9":
				n = (n * 10 + int(ch,10)) & 0xFFFF
				ch = self.stream.get()
			self.stream.put(ch)
			return str(n)
		#
		#		Hex Integer
		#
		if ch == '$':
			word = ""
			ch = self.stream.get().lower()
			while (ch >= '0' and ch <= '9') or (ch >= 'a') and (ch <= 'f'):
				word = word + ch
				ch = self.stream.get().lower()
			self.stream.put(ch)
			return str(int(word,16) & 0xFFFF)
		#
		#		Identifier
		#
		if (ch >= 'a' and ch <= 'z') or ch == '_':
			ident = ch
			ch = self.stream.get().lower()
			while (ch >= 'a' and ch <= 'z') or (ch >= '0' and ch <= '9') or ch == '.' or ch == '_':
				ident = ident + ch
				ch = self.stream.get().lower()
			self.stream.put(ch)
			return ident
		#
		#		Quoted string
		#
		if ch == "'":
			char = self.stream.get()
			ch = self.stream.get()
			if ch != "'":
				raise CompilerException("")
			return str(ord(char))
		return ch	

	#
	#		Put the next element back
	#
	def put(self,element):
		assert self.elementHeld is None, "Put two elements back"
		self.elementHeld = element 

if __name__ == "__main__":
	tas = TextArrayStream("""
		$7FFE
		locvar + 4 ;
		"hello" 123 var.ident_1 >+< 'x' // comment
		"world" $2A
	
	""".split("\n"))

	#tas = FileStream("errors.py")

	pars = ElementParser(tas)
	c = pars.get()
	while c != "":
		print(c)
		c = pars.get()
