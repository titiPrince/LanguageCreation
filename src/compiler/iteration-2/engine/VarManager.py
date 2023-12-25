class VarType:
	INTEGER = 0
	STRING = 1
	BOOLEAN = 2


class Variable:
	def __init__(self, _name: str, _shortname: str, _type: int | None):
		self.name = _name
		self.short = _shortname
		self.type = _type

	def __str__(self):
		_type = "null" if self.type is None else ("int", "str", "bool")[self.type]

		return f"{self.name} -> {self.short}:{_type}"

	def setType(self, _type: int):
		self.type = _type


class VarManager:
	"""
	Keep the variable references in memory and give a short name of this reference
	to the transpiler.

	To add a new variable, you can use the ``create`` method, but it's better to use the ``createOrGet`` method
	to avoid **None** returns and always get an id.

	If you directly want to generate a new name from an existing or not variable, you can use the ``generateFromName``
	method.
	This will automatically store a new variable if it doesn't exist and then generate
	and return the short name.

	Can manage scopes by using the ``startScope`` and ``endScope`` methods.
	The ``startScope`` method will create a new table containing the previous scope variables.
	Where the ``endScope`` will just forget the current scope and come back in the previous one.
	"""
	ALPHABET = "abcdefghijklmnopqrstuvwxyz"

	def __init__(self):
		self.vars = [[]]
		self.count = 0
		self.scope = 0

	def __str__(self):
		"""
		Will generate a string view of the current scope memory.
		"""
		return "\n".join([f"Var {i}: {t} = {self.generateFromId(i)}" for i, t in enumerate(self.vars[self.scope])])

	def exists(self, name: str) -> bool:
		"""
		Check if the variable **name** exists or not in the current scope memory.
		:param name: The name of the variable to check.
		:return: **True** if the variable exists in the current scope. **False** if not.
		"""
		for var in self.vars[self.scope]:
			if var.name == name: return True
		return False

	def create(self, name: str, _type: int = None) -> int:
		"""
		Create a new variable in the current scope memory with the given variable name.

		**Prefer using the** ``createOrGet`` **method than this one!**
		:param _type:
		:param name: The variable's name.
		:return: The new variable's int **id** or **None** if the variable already exists in the current scope.
		"""
		if self.exists(name):
			return -1

		self.vars[self.scope].append(Variable(name, self.generateFromId(self.count), _type))
		self.count += 1

		return self.count - 1

	def getIdByName(self, name: str) -> int:
		for i, var in enumerate(self.vars[self.scope]):
			if var.name == name: return i
		return -1

	def getVarById(self, id: int) -> Variable | None:
		return self.vars[self.scope][id] if id < self.count else None

	def createOrGet(self, name: str, _type: int = None) -> int:
		"""
		Will look if the variable exists and then return its id, but will create a new one if it doesn't exist.
		:param name: The name of the variable to create or get.
		:return: Return the `int` **id** of the variable in any case.
		"""
		for i, var in enumerate(self.vars[self.scope]):
			if var.name == name: return i

		self.vars[self.scope].append(Variable(name, self.generateFromId(self.count), _type))
		self.count += 1

		return self.count - 1

	def generateFromId(self, _id: int) -> str:
		result = ""

		while _id >= 0:
			result = VarManager.ALPHABET[_id % 26] + result
			_id = _id // 26 - 1

		return result

	def generateFromName(self, name: str) -> str:
		"""
		Directly give a unique short name depending on the variable name
		:param name: The name of the variable.
		:return: Return the short name from the given variable's name.
		"""
		return self.generateFromId(self.createOrGet(name))

	def startScope(self):
		"""
		Create a new scope of variables. Will copy the previous scope to this new one.
		"""
		oldScope = self.vars[self.scope].copy()
		self.scope += 1
		self.vars.insert(self.scope, oldScope)

	def endScope(self):
		"""
		Forget the current scope and go back in the previous scope.
		"""
		if self.scope >= 1:
			del self.vars[self.scope]
			self.scope -= 1


# Usages example
if __name__ == "__main__":
	# Create an instance of the VarManager.
	vm = VarManager()

	# Create a new variable in the current scope.
	varId = vm.createOrGet("usage")

	# Get the name of the variable from its id => "usage".
	var1 = vm.getVarById(varId)

	# Show that if you try to create a variable who already exists, it will return the same id.

	if varId == vm.createOrGet("usage"):
		print(f"The var '{var1.name}' already exist in this scope")

	# Starting a new scope
	vm.startScope()

	# Create a specific variable in this new scope
	varIdInScope = vm.createOrGet("scopeUsage")
	var2 = vm.getVarById(varIdInScope)

	# Show that the scopes keep the previous variables in their memory
	if varId == vm.createOrGet("usage"):
		print(f"The var '{var1.name}' always exist in this new scope")

	# Terminate this current scope
	vm.endScope()

	# Show that the variables previously created in a different scope don't exist anymore
	if varIdInScope != vm.createOrGet("scopeUsage"):
		print(f"The var '{var2.name}' doesn't exist in this scope")

	# Get the short name of the variable
	print(var1.short)
