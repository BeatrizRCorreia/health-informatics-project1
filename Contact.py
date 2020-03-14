class Contact:

	def __init__(self, contact_db_id, relationship, Name, Address, gender, organization, period):
		self.contact_db_id = contact_db_id
		self.relationship = relationship
		self.Name = Name
		self.Address = Address
		self.gender = gender
		self.organization = organization
		self.period = period
		self.telecoms = []

	def get_contact_db_id(self):
		return self.contact_db_id

	def get_relationship(self):
		return self.relationship

	def get_Name(self):
		return self.Name

	def get_Address(self):
		return self.Address

	def get_gender(self):
		return self.gender

	def get_organization(self):
		return self.organization

	def get_period(self):
		return self.period
