class Animal:

	def __init__(self, species, breed, genderStatus):
		self.species = species
		self.breed = breed
		self.genderStatus = genderStatus

	def get_species(self):
		return self.species

	def get_breed(self):
		return self.breed

	def get_genderStatus(self):
		return self.genderStatus