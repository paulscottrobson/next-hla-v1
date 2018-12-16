# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		term.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		9th December 2018
#		Purpose :	Extract a term from a stream
#
# ***************************************************************************************
# ***************************************************************************************

from errors import *
from streams import *
from elements import *
from dictionary import *
from democodegen import *
import os,re

# ***************************************************************************************
#									Term objects
# ***************************************************************************************

class Term(object):
	def __init__(self,value):
		self.value = value 
	def getValue(self):
		return self.value 
	def toString(self):
		return "{0} {1}/${1:04x}".format(self.typeName(),self.value)

class ConstantTerm(Term):
	def typeName(self):
		return "ConstantTerm"

class AddressTerm(Term):
	def typeName(self):
		return "AddressTerm"

# ***************************************************************************************
#								Extract a term
# ***************************************************************************************

class TermExtractor(object):
	def __init__(self,parser,codeGenerator,dictionary):
		self.parser = parser
		self.codeGenerator = codeGenerator
		self.dictionary = dictionary
	#
	#		Extract a tern
	#
	def extract(self):
		element = self.parser.get()
		#print("["+element+"]")
		#
		#		Nothing
		#
		if element == "":
			raise CompilerException("Missing term")
		#
		#		- <Constant term>
		#
		if element == "-":
			term = self.extract()
			if not isinstance(term,ConstantTerm):
				print("Can only apply unary minus to constants")
			return ConstantTerm(-term.getValue() & 0xFFFF)
		#
		#		Constant integer. Also hex and 'character', the parser handles this.
		#
		if element[0] >= '0' and element[0] <= '9':
			return ConstantTerm(int(element[0]))
		#
		#		Identifier.
		#
		if element[0] >= 'a' and element[0] <= 'z':
			dEntry = self.dictionary.find(element)
			if dEntry is None:
				raise CompilerException("Unknown identifier "+element)
			if isinstance(dEntry,ConstantIdentifier):
				return ConstantTerm(dEntry.getValue())
			if isinstance(dEntry,VariableIdentifier):
				return AddressTerm(dEntry.getValue())
			raise CompilerException("Cannot use "+element+" in expression.")
		#
		#		Identifier address.
		#
		if element[0] == '@':
			element = self.parser.get()
			dEntry = self.dictionary.find(element)
			if dEntry is None:
				raise CompilerException("Unknown identifier "+element)
			if isinstance(dEntry,VariableIdentifier):
				return ConstantTerm(dEntry.getValue() & 0xFFFF)
			raise CompilerException("Cannot use @ operator on "+element)
		#
		#		String
		#
		if element[0] == '"':
			strAddr = self.codeGenerator.stringConstant(element[1:-1])
			return ConstantTerm(strAddr)
		#
		#		Give up !
		#
		raise CompilerException("Bad term "+element)


if __name__ == "__main__":
	tas = TextArrayStream("""
		$7FFE 65321 'x' -4
		locvar glbvar const1 -const1
		"hello world"
		// String
		// @identifier (var only)

	""".split("\n"))

	tx = TermExtractor(ElementParser(tas),DemoCodeGenerator(),TestDictionary())
	while True:
		print(tx.extract().toString())