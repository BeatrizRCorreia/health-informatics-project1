class Telecom:

	def __init__(self, p_or_c, system, value, use, rank, period):
		self.p_or_c = p_or_c
		self.system = system
		self.value = value
		self.use = use
		self.rank = rank
		self.period = period

	def get_p_or_c(self):
		return self.p_or_c

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