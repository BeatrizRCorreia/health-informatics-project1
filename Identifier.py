class Identifier:

	def __init__(self, use, type, system, value, period, assigner):
		self.use = use
		self.type = type
		self.system = system
		self.value = value
		self.period = period
		self.assigner = assigner

	def get_use(self):
		return self.use

	def get_type(self):
		return self.type

	def get_system(self):
		return self.system

	def get_value(self):
		return self.value

	def get_period(self):
		return self.period

	def get_assigner(self):
		return self.assigner