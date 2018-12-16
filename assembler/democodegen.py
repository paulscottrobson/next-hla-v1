# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		democodegenerator.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		16th December 2018
#		Purpose :	Imaginary language code generator.
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#
#					Code generator for an imaginary CPU, for testing
#
# ***************************************************************************************

class DemoCodeGenerator(object):
	def __init__(self,optimise = False):
		self.addr = 0x1000
		self.strAddr = 0x2000
		self.opNames = {}
		for op in "+add;-sub;*mult;/div;%mod;&and;|or;^xor;>grt;=equ;<less;#neq".split(";"):
			self.opNames[op[0]] = op[1:]
	#
	#		Place an ASCIIZ string constant ... somewhere .... return its address
	#
	def stringConstant(self,str):
		print("${0:06x} : db    '{1}',0".format(self.strAddr,str))
		strAddr = self.strAddr
		self.strAddr = self.strAddr + len(str) + 1
		return strAddr
	#
	#		Load Accumulator with constant or term.
	#
	def loadARegister(self,term):
		if term[0]:
			print("${0:06x} : ldr   a,[${1:04x}]".format(self.strAddr,term[1]))
		else:
			print("${0:06x} : ldr   a,#${1:04x}".format(self.strAddr,term[1]))
		self.strAddr += 1
	#
	#		Perform a binary operation with a constant/term on the accumulator.
	#
	def binaryOperation(self,operator,term):
		if operator == "!" or operator == "?":
			self.binaryOperation("+",term)
			print("${0:06x} : ldr.{1} a,[a]".format(self.strAddr,"w" if operator == "!" else "b"))
			self.strAddr += 1
			return
		operator = self.opNames[operator]
		if term[0]:
			print("${0:06x} : {1:4}  a,[${2:04x}]".format(self.strAddr,operator,term[1]))
		else:
			print("${0:06x} : {1:4}  a,#${2:04x}".format(self.strAddr,operator,term[1]))
		self.strAddr += 1
	#
	#		Save A at the address given
	#
	def saveDirect(self,address):
		print("${0:06x} : str   a,[${1:04x}]".format(self.strAddr,address))
		self.strAddr += 1
	#
	#		Save A indirect through X
	#
	def saveIndirect(self,isWord):
		print("${0:06x} : str.{1} a,[x]".format(self.strAddr,"w" if isWord else "b"))
		self.strAddr += 1
	#
	#		Copy A to the Index register, A value unknown after this.	
	#
	def copyToIndex(self):
		print("${0:06x} : tax".format(self.strAddr))
		self.strAddr += 1
	#
	#		Compile a call to a procedure
	#
	def compileCall(self,address):
		print("${0:06x} : call  ${1:06x}".format(self.strAddr,address))
