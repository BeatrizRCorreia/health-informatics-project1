class Address:

	def __init__(self, contact_db_id, use, type, text, line, city, district, state, postalCode, country, period):
		self.contact_db_id = contact_db_id
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

	def get_contact_db_id(self):
		return self.contact_db_id

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