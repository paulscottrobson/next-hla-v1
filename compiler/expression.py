# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		expression.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		12th December 2018
#		Purpose :	Expression compiler
#
# ***************************************************************************************
# ***************************************************************************************

from errors import *
from streams import *
from elements import *
from dictionary import *
from democodegen import *
from term import *

# ***************************************************************************************
#								Expression Compiler
# ***************************************************************************************

class ExpressionCompiler(object):
	def __init__(self,parser,codeGenerator,dictionary):
		self.parser = parser
		self.codeGenerator = codeGenerator
		self.dictionary = dictionary
		self.termExtractor = TermExtractor(parser,codeGenerator,dictionary)

	def compile(self):
		firstTerm = self.termExtractor.extract()
		self.codeGenerator.loadARegister(isinstance(firstTerm,ConstantTerm),firstTerm.getValue())
		operator = self.parser.get()
		while len(operator) == 1 and "+-*%!?&|^>=<#".find(operator) >= 0:
			secondTerm = self.termExtractor.extract()
			self.codeGenerator.binaryOperation(operator,isinstance(secondTerm,ConstantTerm),secondTerm.getValue())
			operator = self.parser.get()
		self.parser.put(operator)
		
if __name__ == "__main__":
	tas = TextArrayStream("""
		locvar + 4 < 7 
		glbvar!0?const1
		glbvar % locvar
	""".split("\n"))

	tx = ExpressionCompiler(ElementParser(tas),DemoCodeGenerator(),TestDictionary())
	tx.compile()
	print("===========================")
	tx.compile()
	print("===========================")
	tx.compile()
