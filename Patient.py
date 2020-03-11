class Patient:

	def __init__(self, active, gender, birthDate, deceasedBoolean, managingOrganization):
		self.active = active
		self.gender = gender
		self.birthDate = birthDate
		self.deceasedBoolean = deceasedBoolean
		self.managingOrganization = managingOrganization
		self.identifiers = []
		self.names = []
		self.telecoms = []
		self.addresses = []
		self.contacts = []

	def get_active(self):
		return self.active

	def get_gender(self):
		return self.gender

	def get_birthDate(self):
		return self.birthDate

	def get_deceasedBoolean(self):
		return self.deceasedBoolean

	def get_managingOrganization(self):
		return self.managingOrganization
