# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		errors.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		9th December 2018
#		Purpose :	Error classes
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#								Compiler Error
# ***************************************************************************************

class CompilerException(Exception):
	def __init__(self,message):
		self.message = message
	def get(self):
		return "{0} ({1}:{2})".format(self.message,CompilerException.FILENAME,CompilerException.LINENUMBER)

CompilerException.FILENAME = "test"
CompilerException.LINENUMBER = 42

if __name__ == "__main__":
	ex = CompilerException("Division by 42 error")
	print(ex.get())
	raise ex
	