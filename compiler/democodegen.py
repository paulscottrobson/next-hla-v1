# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		democodegenerator.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		11th December 2018
#		Purpose :	Imaginary language code generator.
#
# ***************************************************************************************
# ***************************************************************************************

class DemoCodeGenerator(object):
	def __init__(self):
		self.addr = 0x1000
		self.strAddr = 0x2000
		self.opNames = {}
		for op in "+add;-sub;*mult;/div;%mod;&and;|or;^xor;>grt;=equ;<less;#neq".split(";"):
			self.opNames[op[0]] = op[1:]

	def stringConstant(self,str):
		print("{0:04x} : db    '{1}',0".format(self.strAddr,str))
		strAddr = self.strAddr
		self.strAddr = self.strAddr + len(str) + 1
		return strAddr

	def loadARegister(self,isConstant,value):
		if isConstant:
			print("{0:04x} : ldr   a,#${1:04x}".format(self.strAddr,value))
		else:
			print("{0:04x} : ldr   a,[${1:04x}]".format(self.strAddr,value))
		self.strAddr += 1

	def binaryOperation(self,operator,isConstant,value):
		if operator == "!" or operator == "?":
			self.binaryOperation("+",isConstant,value)
			print("{0:04x} : ldr.{1} a,[a]".format(self.strAddr,"w" if operator == "!" else "b"))
			self.strAddr += 1
			return

		operator = self.opNames[operator]
		if isConstant:
			print("{0:04x} : {1:4}  a,#${2:04x}".format(self.strAddr,operator,value))
		else:
			print("{0:04x} : {1:4}  a,[${2:04x}]".format(self.strAddr,operator,value))
		self.strAddr += 1
