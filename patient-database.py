import sqlite3
from sqlite3 import Error
import json

from Identifier import Identifier
from Name import Name
from Patient import Patient
from Telecom import Telecom
from Address import Address
from Contact import Contact
from Animal import Animal
from Link import Link
from Communication import Communication

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
    generalPractitioner text);"""

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
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

contacts_sql = """CREATE TABLE IF NOT EXISTS contact (
    patient_db_id integer,
    relationship text,
    gender text,
    organization text,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

communications_sql = """CREATE TABLE IF NOT EXISTS communication (
    patient_db_id integer,
    language text,
    preferred integer,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

addresses_sql = """CREATE TABLE IF NOT EXISTS address (
    patient_db_id integer,
    p_or_c text NOT NULL,
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
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

identifiers_sql = """CREATE TABLE IF NOT EXISTS identifier (
    patient_db_id integer,
    use text,
    type text,
    system text,
    value integer,
    period text,
    assigner text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

names_sql = """CREATE TABLE IF NOT EXISTS name (
    patient_db_id integer,
    p_or_c text NOT NULL,
    use text,
    textt text,
    family text,
    given text,
    period text,
    prefix text,
    suffix text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""

telecoms_sql = """CREATE TABLE IF NOT EXISTS telecom (
    patient_db_id integer,
    p_or_c text NOT NULL,
    system text,
    value text,
    use text,
    rank integer,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);"""


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
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.execute("""PRAGMA foreign_keys = ON;""") #NOT WORKING PROPERLY
        return conn
    except Error as e:
        print(e)

    return conn


def parser():

    patients = []
    patient_db_id = 0

    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_content_dict = json.load(f)

        if (json_content_dict.get('resourceType') == 'Patient'):

            patient_db_id += 1
            
            print(json_content_dict)

            print('\n')

            print('\n')

            if 'animal' in json_content_dict.keys():
                for f in json_content_dict.get('animal'):
                    animal = Animal(json_content_dict.get('species'), json_content_dict.get('breed'), json_content_dict.get('genderStatus'))
            else:
                animal = None

            patient = Patient(patient_db_id, json_content_dict.get('active'), json_content_dict.get('gender'), json_content_dict.get('birthDate'), json_content_dict.get('deceasedBoolean'), json_content_dict.get('managingOrganization'), json_content_dict.get('maritalStatus'), json_content_dict.get('multipleBirthBoolean'), json_content_dict.get('multipleBirthInteger'), json_content_dict.get('photo'), json_content_dict.get('generalPractioner'), animal)

            for a in json_content_dict.get('name'):
                name = Name('patient', a.get('use'), a.get('text'), a.get('family'), a.get('given'), a.get('period'), a.get('prefix'), a.get('suffix'))
                patient.names.append(name)

            for b in json_content_dict.get('identifier'):
                identifier = Identifier(b.get('use'), b.get('type'), b.get('system'), b.get('value'), b.get('period'), b.get('assigner'))
                patient.identifiers.append(identifier)

            for c in json_content_dict.get('telecom'):
                telecom = Telecom('patient', c.get('system'), c.get('value'), c.get('use'), c.get('rank'), c.get('period'))
                patient.telecoms.append(telecom)

            for d in json_content_dict.get('address'):
                address = Address('patient', d.get('use'), d.get('type'), d.get('text'), d.get('line'), d.get('city'), d.get('district'), d.get('state'), d.get('postalCode'), d.get('country'), d.get('period'))
                patient.addresses.append(address)

            if 'contact' in json_content_dict.keys():
                for e in json_content_dict.get('contact'):
                    name = Name('contact', e.get('name').get('use'), e.get('name').get('text'), e.get('name').get('family'), e.get('name').get('given'), e.get('name').get('period'), e.get('name').get('prefix'), e.get('name').get('suffix'))
                    address = Address('contact', e.get('address').get('use'), e.get('address').get('type'), e.get('address').get('text'), e.get('address').get('line'), e.get('address').get('city'), e.get('address').get('district'), e.get('address').get('state'), e.get('address').get('postalCode'), e.get('address').get('country'), e.get('address').get('period'))
                    contact = Contact(e.get('relationship'), name, address, e.get('gender'), e.get('organization'), e.get('period'))
                    for f in e.get('telecom'):
                        telecom = Telecom('contact', f.get('system'), f.get('value'), f.get('use'), f.get('rank'), f.get('period'))
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

            print(patient)

            print(patient.get_patient_db_id())
            print(patient.get_active())
            print(patient.get_gender())
            print(patient.get_birthDate())
            print(patient.get_deceasedBoolean())
            print(patient.get_managingOrganization())
            print(patient.get_maritalStatus())
            print(patient.get_multipleBirthBoolean())
            print(patient.get_multipleBirthInteger())
            print(patient.get_photo())
            print(patient.get_generalPractitioner())

            print('\n')

            print(patient.get_Animal())

            print('\n')

            print(patient.names)
            print(patient.identifiers)
            print(patient.telecoms)
            print(patient.addresses)
            print(patient.contacts)
            print(patient.links)
            print(patient.communications)

            print('\n')

            for i in patient.names:
                print(i.get_p_or_c())
                print(i.get_use())
                print(i.get_text())
                print(i.get_family())
                print(i.get_given())
                print(i.get_period())
                print(i.get_prefix())
                print(i.get_suffix())

            print('\n')

            for j in patient.identifiers:
                print(j.get_use())
                print(j.get_type())
                print(j.get_system())
                print(j.get_value())
                print(j.get_period())
                print(j.get_assigner())

            print('\n')

            for m in patient.telecoms:
                print(m.get_p_or_c())
                print(m.get_system())
                print(m.get_value())
                print(m.get_use())
                print(m.get_rank())
                print(m.get_period())

            print('\n')

            for n in patient.addresses:
                print(n.get_p_or_c())
                print(n.get_use())
                print(n.get_type())
                print(n.get_text())
                print(n.get_line())
                print(n.get_city())
                print(n.get_district())
                print(n.get_state())
                print(n.get_postalCode())
                print(n.get_country())
                print(n.get_period())

            print('\n')

            for l in patient.contacts:
                print(l.get_relationship())
                print(l.get_Name())
                print(l.get_Name().get_p_or_c())
                print(l.get_Name().get_use())
                print(l.get_Name().get_text())
                print(l.get_Name().get_family())
                print(l.get_Name().get_given())
                print(l.get_Name().get_period())
                print(l.get_Name().get_prefix())
                print(l.get_Name().get_suffix())
                print(l.get_gender())
                print(l.get_organization())
                print(l.get_period())
                print(l.get_Address())
                print(l.get_Address().get_p_or_c())
                print(l.get_Address().get_use())
                print(l.get_Address().get_type())
                print(l.get_Address().get_text())
                print(l.get_Address().get_line())
                print(l.get_Address().get_city())
                print(l.get_Address().get_district())
                print(l.get_Address().get_state())
                print(l.get_Address().get_postalCode())
                print(l.get_Address().get_country())
                print(l.get_Address().get_period())
                for telecom in l.telecoms:
                    print(telecom.get_p_or_c())
                    print(telecom.get_system())
                    print(telecom.get_value())
                    print(telecom.get_use())
                    print(telecom.get_rank())
                    print(telecom.get_period())

            print('\n')

    print(patients)
    return patients


def populate_db(patients, database):
    print('\n')
    print('POPULATE DB:')

    for patient in patients:
        
        patient_data = (patient.get_patient_db_id(), patient.get_active(), str(patient.get_gender()), str(patient.get_birthDate()), patient.get_deceasedBoolean(), str(patient.get_managingOrganization()), str(patient.get_maritalStatus()), patient.get_multipleBirthBoolean(), patient.get_multipleBirthInteger(), str(patient.get_photo()), str(patient.get_generalPractitioner())) 
        # print(patient_data)
        list_patient_data = list(patient_data)
        for i in range(0, len(list_patient_data)):
            if (list_patient_data[i] == 'None'):
                list_patient_data[i] = None
        tuple_patient_data = tuple(list_patient_data)
        database.execute('INSERT INTO patient(patient_db_id, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner) VALUES (?,?,?,?,?,?,?,?,?,?,?);', tuple_patient_data)

        if (patient.get_Animal() != None):
            animal_data = (patient.get_patient_db_id(), str(patient.get_Animal().get_species()), str(patient.get_Animal().get_breed()), str(patient.get_Animal().get_genderStatus()))
            # print(animal_data)
            list_animal_data = list(animal_data)
            for i in range(0, len(list_animal_data)):
                if (list_animal_data[i] == 'None'):
                    list_animal_data[i] = None
            tuple_animal_data = tuple(list_animal_data)
            database.execute('INSERT INTO animal(patient_db_id, species, breed, genderStatus) VALUES (?,?,?,?);', tuple_animal_data)

        for link in patient.links:
            link_data = (patient.get_patient_db_id(), str(link.get_other()), str(link.get_type()))
            # print(link_data)
            list_link_data = list(link_data)
            for i in range(0, len(list_link_data)):
                if (list_link_data[i] == 'None'):
                    list_link_data[i] = None
            tuple_link_data = tuple(list_link_data)
            database.execute('INSERT INTO link(patient_db_id, other, type) VALUES (?,?,?);', tuple_link_data)

        for contact in patient.contacts:
            contact_data = (patient.get_patient_db_id(), str(contact.get_relationship()), str(contact.get_gender()), str(contact.get_organization()), str(contact.get_period()))
            # print(contact_data)
            list_contact_data = list(contact_data)
            for i in range(0, len(list_contact_data)):
                if (list_contact_data[i] == 'None'):
                    list_contact_data[i] = None
            tuple_contact_data = tuple(list_contact_data)
            database.execute('INSERT INTO contact(patient_db_id, relationship, gender, organization, period) VALUES (?,?,?,?,?);', tuple_contact_data)
            if (contact.get_Address() != None):
                address_data = (patient.get_patient_db_id(), str(contact.get_Address().get_p_or_c()), str(contact.get_Address().get_use()), str(contact.get_Address().get_type()), str(contact.get_Address().get_text()), str(contact.get_Address().get_line()), str(contact.get_Address().get_city()), str(contact.get_Address().get_district()), str(contact.get_Address().get_state()), contact.get_Address().get_postalCode(), str(contact.get_Address().get_country()), str(contact.get_Address().get_period()))
                # print(address_data)
                list_address_data = list(address_data)
                for i in range(0, len(list_address_data)):
                    if (list_address_data[i] == 'None'):
                        list_address_data[i] = None
                tuple_address_data = tuple(list_address_data)
                database.execute('INSERT INTO address(patient_db_id, p_or_c, use, type, textt, line, city, district, state, postalCode, country, period) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', tuple_address_data)
            if (contact.get_Name() != None):
                name_data = (patient.get_patient_db_id(), str(contact.get_Name().get_p_or_c()), str(contact.get_Name().get_use()), str(contact.get_Name().get_text()), str(contact.get_Name().get_family()), str(contact.get_Name().get_given()), str(contact.get_Name().get_period()), str(contact.get_Name().get_prefix()), str(contact.get_Name().get_suffix()))
                # print(name_data)
                list_name_data = list(name_data)
                for i in range(0, len(list_name_data)):
                    if (list_name_data[i] == 'None'):
                        list_name_data[i] = None
                tuple_name_data = tuple(list_name_data)      
                database.execute('INSERT INTO name(patient_db_id, p_or_c, use, textt, family, given, period, prefix, suffix) VALUES (?,?,?,?,?,?,?,?,?);', tuple_name_data)
            for telecom in contact.telecoms:
                telecom_data = (patient.get_patient_db_id(), str(telecom.get_p_or_c()), str(telecom.get_system()), str(telecom.get_value()), str(telecom.get_use()), telecom.get_rank(), str(telecom.get_period()))
                # print(telecom_data)
                list_telecom_data = list(telecom_data)
                for i in range(0, len(list_telecom_data)):
                    if (list_telecom_data[i] == 'None'):
                        list_telecom_data[i] = None
                tuple_telecom_data = tuple(list_telecom_data)
                database.execute('INSERT INTO telecom(patient_db_id, p_or_c, system, value, use, rank, period) VALUES (?,?,?,?,?,?,?);', tuple_telecom_data)

        for communication in patient.communications:
            communication_data = (patient.get_patient_db_id(), str(communication.get_language()), communication.get_preferred())
            # print(communication_data)
            list_communication_data = list(communication_data)
            for i in range(0, len(list_communication_data)):
                if (list_communication_data[i] == 'None'):
                    list_communication_data[i] = None
            tuple_communication_data = tuple(list_communication_data)
            database.execute('INSERT INTO communication(patient_db_id, language, preferred) VALUES (?,?,?);', communication_data)

        for address in patient.addresses:
            address_data = (patient.get_patient_db_id(), str(address.get_p_or_c()), str(address.get_use()), str(address.get_type()), str(address.get_text()), str(address.get_line()), str(address.get_city()), str(address.get_district()), str(address.get_state()), address.get_postalCode(), str(address.get_country()), str(address.get_period()))
            # print(address_data)
            list_address_data = list(address_data)
            for i in range(0, len(list_address_data)):
                if (list_address_data[i] == 'None'):
                    list_address_data[i] = None
            tuple_address_data = tuple(list_address_data)
            database.execute('INSERT INTO address(patient_db_id, p_or_c, use, type, textt, line, city, district, state, postalCode, country, period) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', tuple_address_data)

        for identifier in patient.identifiers:
            identifier_data = (patient.get_patient_db_id(), str(identifier.get_use()), str(identifier.get_type()), str(identifier.get_system()), identifier.get_value(), str(identifier.get_period()), str(identifier.get_assigner()))
            # print(identifier_data)
            list_identifier_data = list(identifier_data)
            for i in range(0, len(list_identifier_data)):
                if (list_identifier_data[i] == 'None'):
                    list_identifier_data[i] = None
            tuple_identifier_data = tuple(list_identifier_data)
            database.execute('INSERT INTO identifier(patient_db_id, use, type, system, value, period, assigner) VALUES (?,?,?,?,?,?,?);', tuple_identifier_data)

        for name in patient.names:
            name_data = (patient.get_patient_db_id(), str(name.get_p_or_c()), str(name.get_use()), str(name.get_text()), str(name.get_family()), str(name.get_given()), str(name.get_period()), str(name.get_prefix()), str(name.get_suffix()))
            # print(name_data)
            list_name_data = list(name_data)
            for i in range(0, len(list_name_data)):
                if (list_name_data[i] == 'None'):
                    list_name_data[i] = None
            tuple_name_data = tuple(list_name_data)
            database.execute('INSERT INTO name(patient_db_id, p_or_c, use, textt, family, given, period, prefix, suffix) VALUES (?,?,?,?,?,?,?,?,?);', tuple_name_data)

        for telecom in patient.telecoms:
            telecom_data = (patient.get_patient_db_id(), str(telecom.get_p_or_c()), str(telecom.get_system()), str(telecom.get_value()), str(telecom.get_use()), telecom.get_rank(), str(telecom.get_period()))
            # print(telecom_data)
            list_telecom_data = list(telecom_data)
            for i in range(0, len(list_telecom_data)):
                if (list_telecom_data[i] == 'None'):
                    list_telecom_data[i] = None
            tuple_telecom_data = tuple(list_telecom_data)
            database.execute('INSERT INTO telecom(patient_db_id, p_or_c, system, value, use, rank, period) VALUES (?,?,?,?,?,?,?);', tuple_telecom_data)

    print('\n')
    print('CONTENT IN PATIENT TABLE:')
    for row in database.execute('SELECT * FROM patient'):
        print(row)

    print('\n')
    print('CONTENT IN ANIMAL TABLE:')
    for row in database.execute('SELECT * FROM animal'):
        print(row)

    print('\n')
    print('CONTENT IN LINK TABLE:')
    for row in database.execute('SELECT * FROM link'):
        print(row)

    print('\n')
    print('CONTENT IN CONTACT TABLE:')
    for row in database.execute('SELECT * FROM contact'):
        print(row)

    print('\n')
    print('CONTENT IN COMMUNICATION TABLE:')
    for row in database.execute('SELECT * FROM communication'):
        print(row)

    print('\n')
    print('CONTENT IN ADDRESS TABLE:')
    for row in database.execute('SELECT * FROM address'):
        print(row)

    print('\n')
    print('CONTENT IN IDENTIFIER TABLE:')
    for row in database.execute('SELECT * FROM identifier'):
        print(row)

    print('\n')
    print('CONTENT IN NAME TABLE:')
    for row in database.execute('SELECT * FROM name'):
        print(row)

    print('\n')
    print('CONTENT IN TELECOM TABLE:')
    for row in database.execute('SELECT * FROM telecom'):
        print(row)

    database.commit()
    return


if __name__ == '__main__':
    connection = create_connection(r"/home/beatriz/Documents/TIS/health_informatics_project1/database/my-database.db")

    patients = parser()

    if connection is not None:

        # DROP TABLES
        connection.execute(drop_patients_sql)
        connection.execute(drop_animals_sql)
        connection.execute(drop_links_sql)
        connection.execute(drop_contacts_sql)
        connection.execute(drop_communications_sql)
        connection.execute(drop_addresses_sql)
        connection.execute(drop_identifiers_sql)
        connection.execute(drop_names_sql)
        connection.execute(drop_telecoms_sql)

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

        populate_db(patients, connection)

        connection.close()

    else:
        print("Error! cannot create the database connection.")