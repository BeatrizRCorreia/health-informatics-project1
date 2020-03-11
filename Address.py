class Address:

	def __init__(self, p_or_c, use, type, text, line, city, district, state, postalCode, country, period):
		self.p_or_c = p_or_c
		self.use = use
		self.type = type
		self.text = text
		self.line = line
		self.city = city
		self.district = district
		self.state = state
		self.postalCode = postalCode
		self.country = country
		self.period = period

	def get_p_or_c(self):
		return self.p_or_c

	def get_use(self):
		return self.use

	def get_type(self):
		return self.type

	def get_text(self):
		return self.text

	def get_line(self):
		return self.line

	def get_city(self):
		return self.city

	def get_district(self):
		return self.district

	def get_state(self):
		return self.state

	def get_postalCode(self):
		return self.postalCode

	def get_country(self):
		return self.country

	def get_period(self):
		return self.period