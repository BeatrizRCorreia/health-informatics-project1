import sqlite3
from sqlite3 import Error
import json

from Identifier import Identifier
from Name import Name
from Patient import Patient
from Telecom import Telecom
from Address import Address
from Contact import Contact

json_files = ['patient-example.json']

patients_sql = """CREATE TABLE IF NOT EXISTS patient (
    identifier integer PRIMARY KEY,
    active integer,
    name text,
    telecom text,
    gender text,
    birthDate integer,
    deceasedBoolean integer,
    address text,
    maritalStatus text,
    multipleBirth integer,
    photo blob,
    generalPractioner text,
    managingOrganization text)"""

animals_sql = """CREATE TABLE IF NOT EXISTS animal (
    species text,
    breed text,
    genderStatus text)"""

links_sql = """CREATE TABLE IF NOT EXISTS link (
    other integer,
    type text)"""

contacts_sql = """CREATE TABLE IF NOT EXISTS contact (
    relationship text,
    name text,
    telecom text,
    address text,
    gender text,
    organization text,
    period integer)"""

communications_sql = """CREATE TABLE IF NOT EXISTS communication (
    language text
    preferred text)"""

drop_patients_sql = """DROP TABLE IF EXISTS patient"""

drop_animals_sql = """DROP TABLE IF EXISTS animal"""

drop_links_sql = """DROP TABLE IF EXISTS link"""

drop_contacts_sql = """DROP TABLE IF EXISTS contact"""

drop_communications_sql = """DROP TABLE IF EXISTS communication"""

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def parser():

    patients = []

    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_content_dict = json.load(f)

        if (json_content_dict.get('resourceType') == 'Patient'):
            
            print(json_content_dict)

            print('\n')

            print('\n')

            patient = Patient(json_content_dict.get('active'), json_content_dict.get('gender'), json_content_dict.get('birthDate'), json_content_dict.get('deceasedBoolean'), json_content_dict.get('managingOrganization'))

            for a in json_content_dict.get('name'):
                name = Name(a.get('use'), a.get('text'), a.get('family'), a.get('given'), a.get('period'), a.get('prefix'), a.get('suffix'))
                patient.names.append(name)

            for b in json_content_dict.get('identifier'):
                identifier = Identifier(b.get('use'), b.get('type'), b.get('system'), b.get('value'), b.get('period'), b.get('assigner'))
                patient.identifiers.append(identifier)

            for c in json_content_dict.get('telecom'):
                telecom = Telecom(c.get('system'), c.get('value'), c.get('use'), c.get('rank'), c.get('period'))
                patient.telecoms.append(telecom)

            for d in json_content_dict.get('address'):
                address = Address(d.get('use'), d.get('type'), d.get('text'), d.get('line'), d.get('city'), d.get('district'), d.get('state'), d.get('postalCode'), d.get('country'), d.get('period'))
                patient.addresses.append(address)

            for e in json_content_dict.get('contact'):
                name = Name(e.get('name').get('use'), e.get('name').get('text'), e.get('name').get('family'), e.get('name').get('given'), e.get('name').get('period'), e.get('name').get('prefix'), e.get('name').get('suffix'))
                address = Address(e.get('address').get('use'), e.get('address').get('type'), e.get('address').get('text'), e.get('address').get('line'), e.get('address').get('city'), e.get('address').get('district'), e.get('address').get('state'), e.get('address').get('postalCode'), e.get('address').get('country'), e.get('address').get('period'))
                contact = Contact(e.get('relationship'), name, address, e.get('gender'), e.get('organization'), e.get('period'))
                for f in e.get('telecom'):
                    telecom = Telecom(f.get('system'), f.get('value'), f.get('use'), f.get('rank'), f.get('period'))
                    contact.telecoms.append(telecom)
                patient.contacts.append(contact)

            patients.append(patient)

            print(patient)

            print(patient.get_active())
            print(patient.get_gender())
            print(patient.get_birthDate())
            print(patient.get_deceasedBoolean())
            print(patient.get_managingOrganization())

            print(patient.names)

            for i in patient.names:
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
                print(m.get_system())
                print(m.get_value())
                print(m.get_use())
                print(m.get_rank())
                print(m.get_period())

            print('\n')

            for n in patient.addresses:
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
                    print(telecom.get_system())
                    print(telecom.get_value())
                    print(telecom.get_use())
                    print(telecom.get_rank())
                    print(telecom.get_period())

            print('\n')

    print(patients)



def create_table_Patient(database):
    database.execute(patients_sql)

def create_table_Animal(database):
    database.execute(animals_sql)

def create_table_Link(database):
    database.execute(links_sql)

def create_table_Contact(database):
    database.execute(contacts_sql)

def create_table_Communication(database):
    database.execute(communications_sql)

if __name__ == '__main__':
    connection = create_connection(r"/home/beatriz/Documents/TIS/health_informatics_project1/database/my-database.db")

    parser()

    if connection is not None:
        connection.execute(drop_patients_sql)

        connection.execute(drop_animals_sql)

        connection.execute(drop_links_sql)

        connection.execute(drop_contacts_sql)

        connection.execute(drop_communications_sql)

        create_table_Patient(connection);

        create_table_Animal(connection);

        create_table_Link(connection);

        create_table_Contact(connection);

        create_table_Communication(connection);

            



        connection.close()

    else:
        print("Error! cannot create the database connection.")