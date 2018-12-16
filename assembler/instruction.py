# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		instruction.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		16th December 2018
#		Purpose :	Assemble a single instruction or instruction group.
#
# ***************************************************************************************
# ***************************************************************************************

from errors import *
from streams import *
from elements import *
from dictionary import *
from democodegen import *
from expression import *
from term import *

# ***************************************************************************************
#
#						Compile one instruction or instruction group
#
# ***************************************************************************************

class InstructionCompiler(object):
	def __init__(self,parser,codeGenerator,dictionary):
		self.parser = parser
		self.codeGenerator = codeGenerator
		self.dictionary = dictionary
		self.termCompiler = TermExtractor(parser,codeGenerator,dictionary)
		self.expressionCompiler = ExpressionCompiler(parser,codeGenerator,dictionary)
	#
	#		Compile a single instruction or instruction group.
	#
	def compile(self):
		element = self.parser.get()
		#
		#		TODO: IF WHILE FOR code. VAR
		#

		#
		#		Empty instruction
		#
		if element == ";":
			return
		#
		#		Instruction set grouped with {}
		#
		if element == "{":
			nextElement = self.parser.get()
			while nextElement != "}":
				self.parser.put(nextElement)
				self.compile()
				nextElement = self.parser.get()				
			return
		#
		#		Check for assignment/procedure call.
		#
		if element[0] < 'a' or element[0] > 'z':
			raise AssemblerException("Syntax error "+element)
		#
		# 		Get the thing after the element and decide what to do based on it.
		#
		nextElement = self.parser.get()
		self.parser.put(nextElement)
		self.parser.put(element)
		if nextElement == "!" or nextElement == "?":
			self.indirectAssignment()
		elif nextElement == "=":
			self.directAssignment()
		elif nextElement == "(":
			self.procedureCall()
		else:
			raise AssemblerException("Syntax error "+element)		
	#
	#		Compile a direct assignment
	#
	def directAssignment(self):
		lExprName = self.parser.get()
		lExpr = self.dictionary.find(lExprName)
		if lExpr is None or not isinstance(lExpr,AddressIdentifier):
			raise AssemblerException("Cannot assign to "+lExprName)
		self.parser.expect("=")
		self.expressionCompiler.compile()
		self.parser.expect(";")
		self.codeGenerator.saveDirect(lExpr.getValue())
	#
	#		Compile an indirect assignment.
	#
	def indirectAssignment(self):
		lExprName = self.parser.get()
		lExpr = self.dictionary.find(lExprName)
		if lExpr is None or not isinstance(lExpr,AddressIdentifier):
			raise AssemblerException("Cannot assign to "+lExprName)
		operator = self.parser.get()
		rTerm = self.termCompiler.extract()
		self.codeGenerator.loadARegister([True,lExpr.getValue()])
		self.codeGenerator.binaryOperation("+",rTerm)
		self.codeGenerator.copyToIndex()
		self.parser.expect("=")
		self.expressionCompiler.compile()
		self.parser.expect(";")
		self.codeGenerator.saveIndirect(operator == "!")
	#
	#		Compile a procedure call
	#
	def procedureCall(self):
		procName = self.parser.get()
		proc = self.dictionary.find(procName)
		if proc is  None or not isinstance(proc,AddressIdentifier):
			raise AssemblerException("Cannot call "+procName)
		self.parser.expect("(")
		for i in range(0,proc.getParameterCount()):
			self.expressionCompiler.compile()
			self.codeGenerator.saveDirect(proc.getParameterBaseAddress()+i*2)
			if i < proc.getParameterCount()-1:
				self.parser.expect(",")
		self.parser.expect(")")
		self.parser.expect(";")
		self.codeGenerator.compileCall(proc.getValue())

if __name__ == "__main__":
	tas = TextArrayStream("""
		{ locvar = 1;;; glbvar = const1; }
		glbvar = locvar + 4;
		locvar!4 = 2;
		locvar?glbvar = 3;
		hello(3,locvar!4,const1);
	""".split("\n"))

	tx = InstructionCompiler(ElementParser(tas),DemoCodeGenerator(),TestDictionary())
	tx.compile()
	print("================================")
	tx.compile()
	print("================================")
	tx.compile()
	print("================================")
	tx.compile()
	print("================================")
	tx.compile()

