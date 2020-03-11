class Communication:

	def __init__(self, language, preferred):
		self.language = language
		self.preferred = preferred

	def get_language(self):
		return self.language

	def get_preferred(self):
		return self.preferred
