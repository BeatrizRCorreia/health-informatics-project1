import sqlite3
from sqlite3 import Error
import json

from Patient import Patient
from Animal import Animal
from Link import Link
from Contact import Contact
from Communication import Communication
from Address import Address
from Identifier import Identifier
from Name import Name
from Telecom import Telecom

# MORE JSON FILES CAN BE ADDED HERE TO BE PARSED AND GET ITS CONTENTS ADDED TO THE DATABASE
# ONLY "resourceType": "Patient" RESOURCES WILL BE ACCEPTED TO THE DATABASE
# json_files = ['patient-example.json', 'patient-example-2.json']
json_files = ['patient-example.json']

patients_sql = """CREATE TABLE IF NOT EXISTS patient (
    patient_db_id integer PRIMARY KEY,
    active integer,
    gender text,
    birthDate text,
    deceasedBoolean integer,
    managingOrganization text,
    maritalStatus text,
    multipleBirthBoolean integer,
    multipleBirthInteger integer,
    photo blob,
    generalPractitioner text,
    CONSTRAINT check_gender CHECK (gender IN ('male', 'female', 'other', 'unknown')));"""

animals_sql = """CREATE TABLE IF NOT EXISTS animal (
    patient_db_id integer,
    species text,
    breed text,
    genderStatus text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

links_sql = """CREATE TABLE IF NOT EXISTS link (
    patient_db_id integer,
    other text,
    type text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_type CHECK (type IN ('replaced-by', 'replaces', 'refer', 'seealso')));"""

contacts_sql = """CREATE TABLE IF NOT EXISTS contact (
    patient_db_id integer,
    contact_db_id integer PRIMARY KEY,
    relationship text,
    gender text,
    organization text,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_gender CHECK (gender IN ('male', 'female', 'other', 'unknown')));"""

communications_sql = """CREATE TABLE IF NOT EXISTS communication (
    patient_db_id integer,
    language text,
    preferred integer,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

addresses_sql = """CREATE TABLE IF NOT EXISTS address (
    patient_db_id integer,
    contact_db_id integer,
    use text,
    type text,
    textt text,
    line text,
    city text,
    district text,
    state text,
    postalCode integer,
    country text,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(contact_db_id) REFERENCES contact(contact_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_use CHECK (use IN ('home', 'work', 'temp', 'old')),
    CONSTRAINT check_type CHECK (type IN ('postal', 'physical', 'both')));"""

identifiers_sql = """CREATE TABLE IF NOT EXISTS identifier (
    patient_db_id integer,
    use text,
    type text,
    system text,
    value integer,
    period text,
    assigner text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_use CHECK (use IN ('usual', 'official', 'temp', 'secondary')));"""

names_sql = """CREATE TABLE IF NOT EXISTS name (
    patient_db_id integer,
    contact_db_id integer,
    use text,
    textt text,
    family text,
    given text,
    period text,
    prefix text,
    suffix text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(contact_db_id) REFERENCES contact(contact_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_use CHECK (use IN ('usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden')));"""

telecoms_sql = """CREATE TABLE IF NOT EXISTS telecom (
    patient_db_id integer,
    contact_db_id integer,
    system text,
    value text,
    use text,
    rank integer,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(contact_db_id) REFERENCES contact(contact_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_system CHECK (system IN ('phone', 'fax', 'email', 'pager', 'url', 'sms', 'other')),
    CONSTRAINT check_use CHECK (use IN ('home', 'work', 'temp', 'old', 'mobile')));"""


drop_patients_sql = """DROP TABLE IF EXISTS patient;"""

drop_animals_sql = """DROP TABLE IF EXISTS animal;"""

drop_links_sql = """DROP TABLE IF EXISTS link;"""

drop_contacts_sql = """DROP TABLE IF EXISTS contact;"""

drop_communications_sql = """DROP TABLE IF EXISTS communication;"""

drop_addresses_sql = """DROP TABLE IF EXISTS address;"""

drop_identifiers_sql = """DROP TABLE IF EXISTS identifier;"""

drop_names_sql = """DROP TABLE IF EXISTS name;"""

drop_telecoms_sql = """DROP TABLE IF EXISTS telecom;"""


def create_connection(db_file):
    # SET DATABASE
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("""PRAGMA foreign_keys = ON;""")
        return conn
    except Error as e:
        print(e)

    return conn


def parser():
    # PARSE JSON CONTENT TO OBJECTS
    patients = []
    patient_db_id = 0
    contact_db_id = 0

    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_content_dict = json.load(f)

        if (json_content_dict.get('resourceType') == 'Patient'):

            patient_db_id += 1

            if 'animal' in json_content_dict.keys():
                animal = Animal(json_content_dict.get('animal').get('species'), json_content_dict.get('animal').get('breed'), json_content_dict.get('animal').get('genderStatus'))
            else:
                animal = None

            patient = Patient(patient_db_id, json_content_dict.get('active'), json_content_dict.get('gender'), json_content_dict.get('birthDate'), json_content_dict.get('deceasedBoolean'), json_content_dict.get('managingOrganization'), json_content_dict.get('maritalStatus'), json_content_dict.get('multipleBirthBoolean'), json_content_dict.get('multipleBirthInteger'), json_content_dict.get('photo'), json_content_dict.get('generalPractioner'), animal)

            for a in json_content_dict.get('name'):
                name = Name(None, a.get('use'), a.get('text'), a.get('family'), a.get('given'), a.get('period'), a.get('prefix'), a.get('suffix'))
                patient.names.append(name)

            for b in json_content_dict.get('identifier'):
                identifier = Identifier(b.get('use'), b.get('type'), b.get('system'), b.get('value'), b.get('period'), b.get('assigner'))
                patient.identifiers.append(identifier)

            for c in json_content_dict.get('telecom'):
                telecom = Telecom(None, c.get('system'), c.get('value'), c.get('use'), c.get('rank'), c.get('period'))
                patient.telecoms.append(telecom)

            for d in json_content_dict.get('address'):
                address = Address(None, d.get('use'), d.get('type'), d.get('text'), d.get('line'), d.get('city'), d.get('district'), d.get('state'), d.get('postalCode'), d.get('country'), d.get('period'))
                patient.addresses.append(address)

            if 'contact' in json_content_dict.keys():
                for e in json_content_dict.get('contact'):
                    contact_db_id += 1
                    name = Name(contact_db_id, e.get('name').get('use'), e.get('name').get('text'), e.get('name').get('family'), e.get('name').get('given'), e.get('name').get('period'), e.get('name').get('prefix'), e.get('name').get('suffix'))
                    address = Address(contact_db_id, e.get('address').get('use'), e.get('address').get('type'), e.get('address').get('text'), e.get('address').get('line'), e.get('address').get('city'), e.get('address').get('district'), e.get('address').get('state'), e.get('address').get('postalCode'), e.get('address').get('country'), e.get('address').get('period'))
                    contact = Contact(contact_db_id, e.get('relationship'), name, address, e.get('gender'), e.get('organization'), e.get('period'))
                    for f in e.get('telecom'):
                        telecom = Telecom(contact_db_id, f.get('system'), f.get('value'), f.get('use'), f.get('rank'), f.get('period'))
                        contact.telecoms.append(telecom)
                    patient.contacts.append(contact)
            
            if 'link' in json_content_dict.keys():
                for g in json_content_dict.get('link'):
                    link = Link(g.get('other'), g.get('type'))
                    patient.links.append(link)

            if 'communication' in json_content_dict.keys():
                for h in json_content_dict.get('communication'):
                    communication = Communication(h.get('language'), h.get('preferred'))
                    patient.communications.append(communication)

            patients.append(patient)

    return patients


def populate_db(patients, database):
    # POPULATE TABLES
    print('Populating the db...')

    for patient in patients:
        
        patient_data = (patient.get_patient_db_id(), patient.get_active(), str(patient.get_gender()), str(patient.get_birthDate()), patient.get_deceasedBoolean(), str(patient.get_managingOrganization()), str(patient.get_maritalStatus()), patient.get_multipleBirthBoolean(), patient.get_multipleBirthInteger(), str(patient.get_photo()), str(patient.get_generalPractitioner())) 
        list_patient_data = list(patient_data)
        for i in range(0, len(list_patient_data)):
            if (list_patient_data[i] == 'None'):
                list_patient_data[i] = None
        tuple_patient_data = tuple(list_patient_data)
        database.execute('INSERT INTO patient(patient_db_id, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner) VALUES (?,?,?,?,?,?,?,?,?,?,?);', tuple_patient_data)

        if (patient.get_Animal() != None):
            animal_data = (patient.get_patient_db_id(), str(patient.get_Animal().get_species()), str(patient.get_Animal().get_breed()), str(patient.get_Animal().get_genderStatus()))
            list_animal_data = list(animal_data)
            for i in range(0, len(list_animal_data)):
                if (list_animal_data[i] == 'None'):
                    list_animal_data[i] = None
            tuple_animal_data = tuple(list_animal_data)
            database.execute('INSERT INTO animal(patient_db_id, species, breed, genderStatus) VALUES (?,?,?,?);', tuple_animal_data)

        for link in patient.links:
            link_data = (patient.get_patient_db_id(), str(link.get_other()), str(link.get_type()))
            list_link_data = list(link_data)
            for i in range(0, len(list_link_data)):
                if (list_link_data[i] == 'None'):
                    list_link_data[i] = None
            tuple_link_data = tuple(list_link_data)
            database.execute('INSERT INTO link(patient_db_id, other, type) VALUES (?,?,?);', tuple_link_data)

        for contact in patient.contacts:
            contact_data = (patient.get_patient_db_id(), contact.get_contact_db_id(), str(contact.get_relationship()), str(contact.get_gender()), str(contact.get_organization()), str(contact.get_period()))
            list_contact_data = list(contact_data)
            for i in range(0, len(list_contact_data)):
                if (list_contact_data[i] == 'None'):
                    list_contact_data[i] = None
            tuple_contact_data = tuple(list_contact_data)
            database.execute('INSERT INTO contact(patient_db_id, contact_db_id, relationship, gender, organization, period) VALUES (?,?,?,?,?,?);', tuple_contact_data)
            if (contact.get_Address() != None):
                address_data = (patient.get_patient_db_id(), contact.get_contact_db_id(), str(contact.get_Address().get_use()), str(contact.get_Address().get_type()), str(contact.get_Address().get_text()), str(contact.get_Address().get_line()), str(contact.get_Address().get_city()), str(contact.get_Address().get_district()), str(contact.get_Address().get_state()), contact.get_Address().get_postalCode(), str(contact.get_Address().get_country()), str(contact.get_Address().get_period()))
                list_address_data = list(address_data)
                for i in range(0, len(list_address_data)):
                    if (list_address_data[i] == 'None'):
                        list_address_data[i] = None
                tuple_address_data = tuple(list_address_data)
                database.execute('INSERT INTO address(patient_db_id, contact_db_id, use, type, textt, line, city, district, state, postalCode, country, period) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', tuple_address_data)
            if (contact.get_Name() != None):
                name_data = (patient.get_patient_db_id(), contact.get_contact_db_id(), str(contact.get_Name().get_use()), str(contact.get_Name().get_text()), str(contact.get_Name().get_family()), str(contact.get_Name().get_given()), str(contact.get_Name().get_period()), str(contact.get_Name().get_prefix()), str(contact.get_Name().get_suffix()))
                list_name_data = list(name_data)
                for i in range(0, len(list_name_data)):
                    if (list_name_data[i] == 'None'):
                        list_name_data[i] = None
                tuple_name_data = tuple(list_name_data)      
                database.execute('INSERT INTO name(patient_db_id, contact_db_id, use, textt, family, given, period, prefix, suffix) VALUES (?,?,?,?,?,?,?,?,?);', tuple_name_data)
            for telecom in contact.telecoms:
                telecom_data = (patient.get_patient_db_id(), contact.get_contact_db_id(), str(telecom.get_system()), str(telecom.get_value()), str(telecom.get_use()), telecom.get_rank(), str(telecom.get_period()))
                list_telecom_data = list(telecom_data)
                for i in range(0, len(list_telecom_data)):
                    if (list_telecom_data[i] == 'None'):
                        list_telecom_data[i] = None
                tuple_telecom_data = tuple(list_telecom_data)
                database.execute('INSERT INTO telecom(patient_db_id, contact_db_id, system, value, use, rank, period) VALUES (?,?,?,?,?,?,?);', tuple_telecom_data)

        for communication in patient.communications:
            communication_data = (patient.get_patient_db_id(), str(communication.get_language()), communication.get_preferred())
            list_communication_data = list(communication_data)
            for i in range(0, len(list_communication_data)):
                if (list_communication_data[i] == 'None'):
                    list_communication_data[i] = None
            tuple_communication_data = tuple(list_communication_data)
            database.execute('INSERT INTO communication(patient_db_id, language, preferred) VALUES (?,?,?);', tuple_communication_data)

        for address in patient.addresses:
            address_data = (patient.get_patient_db_id(), address.get_contact_db_id(), str(address.get_use()), str(address.get_type()), str(address.get_text()), str(address.get_line()), str(address.get_city()), str(address.get_district()), str(address.get_state()), address.get_postalCode(), str(address.get_country()), str(address.get_period()))
            list_address_data = list(address_data)
            for i in range(0, len(list_address_data)):
                if (list_address_data[i] == 'None'):
                    list_address_data[i] = None
            tuple_address_data = tuple(list_address_data)
            database.execute('INSERT INTO address(patient_db_id, contact_db_id, use, type, textt, line, city, district, state, postalCode, country, period) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', tuple_address_data)

        for identifier in patient.identifiers:
            identifier_data = (patient.get_patient_db_id(), str(identifier.get_use()), str(identifier.get_type()), str(identifier.get_system()), identifier.get_value(), str(identifier.get_period()), str(identifier.get_assigner()))
            list_identifier_data = list(identifier_data)
            for i in range(0, len(list_identifier_data)):
                if (list_identifier_data[i] == 'None'):
                    list_identifier_data[i] = None
            tuple_identifier_data = tuple(list_identifier_data)
            database.execute('INSERT INTO identifier(patient_db_id, use, type, system, value, period, assigner) VALUES (?,?,?,?,?,?,?);', tuple_identifier_data)

        for name in patient.names:
            name_data = (patient.get_patient_db_id(), name.get_contact_db_id(), str(name.get_use()), str(name.get_text()), str(name.get_family()), str(name.get_given()), str(name.get_period()), str(name.get_prefix()), str(name.get_suffix()))
            list_name_data = list(name_data)
            for i in range(0, len(list_name_data)):
                if (list_name_data[i] == 'None'):
                    list_name_data[i] = None
            tuple_name_data = tuple(list_name_data)
            database.execute('INSERT INTO name(patient_db_id, contact_db_id, use, textt, family, given, period, prefix, suffix) VALUES (?,?,?,?,?,?,?,?,?);', tuple_name_data)

        for telecom in patient.telecoms:
            telecom_data = (patient.get_patient_db_id(), telecom.get_contact_db_id(), str(telecom.get_system()), str(telecom.get_value()), str(telecom.get_use()), telecom.get_rank(), str(telecom.get_period()))
            list_telecom_data = list(telecom_data)
            for i in range(0, len(list_telecom_data)):
                if (list_telecom_data[i] == 'None'):
                    list_telecom_data[i] = None
            tuple_telecom_data = tuple(list_telecom_data)
            database.execute('INSERT INTO telecom(patient_db_id, contact_db_id, system, value, use, rank, period) VALUES (?,?,?,?,?,?,?);', tuple_telecom_data)

    # database.execute('DELETE FROM patient WHERE patient_db_id = 1;') # THE DELETE CASCADE WORKS WELL
    # database.execute('DELETE FROM contact WHERE contact_db_id = 1;') # THE DELETE CASCADE WORKS WELL
    # database.execute('DELETE FROM contact WHERE contact_db_id = 2;') # THE DELETE CASCADE WORKS WELL

    print('\n')
    print('CONTENT IN \'patient\' TABLE:')
    print('(patient_db_id, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner)')
    for row in database.execute('SELECT * FROM patient'):
        print(row)

    print('\n')
    print('CONTENT IN \'animal\' TABLE:')
    print('(patient_db_id, species, breed, genderStatus)')
    for row in database.execute('SELECT * FROM animal'):
        print(row)

    print('\n')
    print('CONTENT IN \'link\' TABLE:')
    print('(patient_db_id, other, type)')
    for row in database.execute('SELECT * FROM link'):
        print(row)

    print('\n')
    print('CONTENT IN \'contact\' TABLE:')
    print('(patient_db_id, contact_db_id, relationship, gender, organization, period)')
    for row in database.execute('SELECT * FROM contact'):
        print(row)

    print('\n')
    print('CONTENT IN \'communication\' TABLE:')
    print('(patient_db_id, language, preferred)')
    for row in database.execute('SELECT * FROM communication'):
        print(row)

    print('\n')
    print('CONTENT IN \'address\' TABLE:')
    print('(patient_db_id, contact_db_id, use, type, textt, line, city, district, state, postalCode, country, period)')
    for row in database.execute('SELECT * FROM address'):
        print(row)

    print('\n')
    print('CONTENT IN \'identifier\' TABLE:')
    print('(patient_db_id, use, type, system, value, period, assigner)')
    for row in database.execute('SELECT * FROM identifier'):
        print(row)

    print('\n')
    print('CONTENT IN \'name\' TABLE:')
    print('(patient_db_id, contact_db_id, use, textt, family, given, period, prefix, suffix)')
    for row in database.execute('SELECT * FROM name'):
        print(row)

    print('\n')
    print('CONTENT IN \'telecom\' TABLE:')
    print('(patient_db_id, contact_db_id, system, value, use, rank, period)')
    for row in database.execute('SELECT * FROM telecom'):
        print(row)

    database.commit()

    return


if __name__ == '__main__':

    # SET DATABASE (NEEDS ADJUSTMENT IF THIS IS RUN IN ANOTHER COMPUTER)
    connection = create_connection(r"/home/beatriz/Documents/TIS/health_informatics_project1/database/my-database.db")

    # PARSE JSON CONTENT TO OBJECTS
    patients = parser()

    if connection is not None:

        # DROP TABLES
        connection.execute(drop_patients_sql)
        connection.execute(drop_animals_sql)
        connection.execute(drop_links_sql)
        connection.execute(drop_communications_sql)
        connection.execute(drop_addresses_sql)
        connection.execute(drop_identifiers_sql)
        connection.execute(drop_names_sql)
        connection.execute(drop_telecoms_sql)
        connection.execute(drop_contacts_sql)

        # CREATE TABLES
        connection.execute(patients_sql)
        connection.execute(animals_sql)
        connection.execute(links_sql)
        connection.execute(contacts_sql)
        connection.execute(communications_sql)
        connection.execute(addresses_sql)
        connection.execute(identifiers_sql)
        connection.execute(names_sql)
        connection.execute(telecoms_sql)

        connection.commit()

        # POPULATE TABLES
        populate_db(patients, connection)

        # CLOSE DATABASE
        connection.close()

    else:
        print("Error! cannot create the database connection.")