class Name:

	def __init__(self, use, text, family, given, period, prefix, suffix):
		self.use = use
		self.text = text
		self.family = family
		self.given = given
		self.period = period
		self.prefix = prefix
		self.suffix = suffix

	def get_use(self):
		return self.use

	def get_text(self):
		return self.text

	def get_family(self):
		return self.family

	def get_given(self):
		return self.given

	def get_period(self):
		return self.period

	def get_prefix(self):
		return self.prefix

	def get_suffix(self):
		return self.suffix