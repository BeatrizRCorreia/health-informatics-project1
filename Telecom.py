class Telecom:

	def __init__(self, contact_db_id, system, value, use, rank, period):
		self.contact_db_id = contact_db_id
		self.system = system
		self.value = value
		self.use = use
		self.rank = rank
		self.period = period

	def get_contact_db_id(self):
		return self.contact_db_id

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