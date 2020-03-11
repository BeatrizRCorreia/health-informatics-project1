class Patient:

	def __init__(self, patient_db_id, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner, Animal):
		self.patient_db_id = patient_db_id
		self.active = active
		self.gender = gender
		self.birthDate = birthDate
		self.deceasedBoolean = deceasedBoolean
		self.managingOrganization = managingOrganization
		self.maritalStatus = maritalStatus
		self.multipleBirthBoolean = multipleBirthBoolean
		self.multipleBirthInteger = multipleBirthInteger
		self.photo = photo
		self.generalPractitioner = generalPractitioner
		self.Animal = Animal
		self.identifiers = []
		self.names = []
		self.telecoms = []
		self.addresses = []
		self.contacts = []
		self.links = []
		self.communications = []

	def get_patient_db_id(self):
		return self.patient_db_id

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

	def get_maritalStatus(self):
		return self.maritalStatus

	def get_multipleBirthBoolean(self):
		return self.multipleBirthBoolean

	def get_multipleBirthInteger(self):
		return self.multipleBirthInteger

	def get_photo(self):
		return self.photo

	def get_generalPractitioner(self):
		return self.generalPractitioner

	def get_Animal(self):
		return self.Animal
