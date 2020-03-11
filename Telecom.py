class Telecom:

	def __init__(self, system, value, use, rank, period):
		self.system = system
		self.value = value
		self.use = use
		self.rank = rank
		self.period = period

	def get_system(self):
		return self.system

	def get_value(self):
		return self.value

	def get_use(self):
		return self.use

	def get_rank(self):
		return self.rank

	def get_period(self):
		return self.period