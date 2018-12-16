# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		identifiers.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		9th December 2018
#		Purpose :	Identifier classes
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#								Root identifier class
# ***************************************************************************************

class Identifier(object):
	def __init__(self,name,value,isGlobal = True):
		self.name = name.strip().lower()
		self.value = value
		self.isGlobalIdentifier = isGlobal
	#
	def getName(self):
		return self.name
	def getValue(self):
		return self.value
	def isGlobal(self):
		return self.isGlobalIdentifier
	#
	def toString(self):
		return "{0} @ ${1:06x} '{3}' {2}".format(self.getName(),self.getValue(),	\
							"global" if self.isGlobal else "local",self.getTypeName())

# ***************************************************************************************
#					Identifier representing a constant value
# ***************************************************************************************

class ConstantIdentifier(Identifier):
	def __init__(self,name,value):
		Identifier.__init__(self,name,value,True)
	def getTypeName(self):
		return "ConstantIdentifier"

# ***************************************************************************************
#					Identifier representing an address
# ***************************************************************************************

class AddressIdentifier(Identifier):
	def getTypeName(self):
		return "AddressIdentifier"

# ***************************************************************************************
#						Identifier representing a variable
# ***************************************************************************************

class VariableIdentifier(AddressIdentifier):
	def getTypeName(self):
		return "VariableIdentifier"

# ***************************************************************************************
#					  Identifier representing a procedure
# ***************************************************************************************

class ProcedureIdentifier(AddressIdentifier):
	def __init__(self,name,address,isExternal = False):
		AddressIdentifier.__init__(self,name,address,True)
		self.isProcExternal = isExternal
		self.paramAddresses = []
	def getTypeName(self):
		return "ProcedureIdentifier"
	def isExternal(self):
		return self.isExternal
	def addParameter(self,paramAddress):
		self.paramAddresses.append(paramAddress)
	def getParameterCount(self):
		return len(self.paramAddresses)
	def getParameter(self,n):
		return self.paramAddresses(n)
	def toString(self):
		s = AddressIdentifier.toString(self)
		if self.isExternal():
			s = s + " external"
		s = s +" ["+",".join("${0:04x}".format(x) for x in self.paramAddresses)+"]"
		return s

if __name__ == "__main__":
	w = ProcedureIdentifier("hello",0x123456,True)
	w.addParameter(0x8011)
	w.addParameter(0x8013)
	print(w.toString())

