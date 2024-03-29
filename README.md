# Health Informatics - Project 1

The *HL7 Fast Healthcare Interoperability Resources* ([FHIR](http://www.hl7.org/fhir/stu3/)) standards framework is built on a set of modular resources that can easily be assembled into working systems. For instance, the [*Patient*](http://hl7.org/fhir/STU3/patient.html) resource covers data about patients involved in a wide range of health-related activities, including the demographic information necessary to support the clinical, administrative, financial and logistic procedures. The FHIR website gives a description for the resource, detailing how the information can be encoded in different formats (e.g., XML or JSON). A corresponding high-level diagram is as follows.

![Patient uml](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient_uml.png)

**Q1 -** Derive a Relational Model to hold the information of the *Patient* resource. You may start by an Entity-Relationship (ER) model of the resources and then convert the ER model to the Relational Model, or you can just map the UML model of the resources into a relational schema directly. Then, implement the database in a database management system of your choice (**suggestion**: [*sqlite*](https://www.sqlite.org/index.html)). Your answer should contain **(i)** the Relational 3 Schema of the module and **(ii)** the SQL instructions to define the relational schema of the database.
___
**(i)**

patient (<ins>patient_db_id</ins>, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner)

animal (<ins>patient_db_id</ins>, species, breed, genderStatus)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

link (<ins>patient_db_id</ins>, other, type)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

contact (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, relationship, gender, organization, period)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

communication (<ins>patient_db_id</ins>, language, preferred)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

address (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, use, type, textt, line, city, district, state, postalCode, country, period)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;contact_db_id: FK (contact)

identifier (<ins>patient_db_id</ins>, use, type, system, value, period, assigner)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

name (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, use, textt, family, given, period, prefix, suffix)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;contact_db_id: FK (contact)

telecom (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, system, value, use, rank, period)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;contact_db_id: FK (contact)
___
**(ii)**
```
CREATE TABLE IF NOT EXISTS patient (
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
    CONSTRAINT check_gender CHECK (gender IN ('male', 'female', 'other', 'unknown')));

CREATE TABLE IF NOT EXISTS animal (
    patient_db_id integer,
    species text,
    breed text,
    genderStatus text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS link (
    patient_db_id integer,
    other text,
    type text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_type CHECK (type IN ('replaced-by', 'replaces', 'refer', 'seealso')));

CREATE TABLE IF NOT EXISTS contact (
    patient_db_id integer,
    contact_db_id integer PRIMARY KEY,
    relationship text,
    gender text,
    organization text,
    period text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_gender CHECK (gender IN ('male', 'female', 'other', 'unknown')));

CREATE TABLE IF NOT EXISTS communication (
    patient_db_id integer,
    language text,
    preferred integer,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS address (
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
    CONSTRAINT check_type CHECK (type IN ('postal', 'physical', 'both')));

CREATE TABLE IF NOT EXISTS identifier (
    patient_db_id integer,
    use text,
    type text,
    system text,
    value integer,
    period text,
    assigner text,
    FOREIGN KEY(patient_db_id) REFERENCES patient(patient_db_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_use CHECK (use IN ('usual', 'official', 'temp', 'secondary')));

CREATE TABLE IF NOT EXISTS name (
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
    CONSTRAINT check_use CHECK (use IN ('usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden')));

CREATE TABLE IF NOT EXISTS telecom (
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
    CONSTRAINT check_use CHECK (use IN ('home', 'work', 'temp', 'old', 'mobile')));

```
___
**Q2 -** Write a program to populate the relational database from JSON files encoding *Patient* resources according to the HL7-PHIR format (**suggestion**: use Python with the [sqlite library](https://docs.python.org/2/library/sqlite3.html)). You can file example JSON files in the [*Patient* description](http://hl7.org/fhir/STU3/patient-examples.html). You should be able to load the [General Person Example](http://hl7.org/fhir/STU3/patient-example.json.html). 
___
**Files that solve this question:**\
main file: [patient-database.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient-database.py)\
objects files: [Patient.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Patient.py), [Animal.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Animal.py), [Link.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Link.py), [Contact.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Contact.py), [Communication.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Communication.py), [Address.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Address.py), [Identifier.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Identifier.py), [Name.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Name.py) and [Telecom.py](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/Telecom.py)\
patients files: [patient-example.json](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient-example.json) and [patient-example-2.json](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient-example-2.json)

**My procedure to solve this question:**

1. Set the database connection.
2. Parse the JSON files by saving the JSON fields inside objects fields (objects are Patient, Animal, Link, Contact, Communication, Address, Identifier, Name and Telecom).
3. Drop existing tables.
4. Create new tables (patient, animal, link, contact, communication, address, identifier, name and telecom).
5. Populate: insert into the corresponding tables the object fields.
6. Close the database connection.

**Run my solution - Linux environment instructions:**

To check the contents inside the database by running my program that has access to the database:
1. Adjust the file path on line 392 ("patient-database.py") to the place in your computer where you want to create the database file "my-database.db".
2. Open a terminal.
3. Get to the folder where the file "patient-database.py" is (along with all the previously mentioned python and json files).
4. Run the command "python3 patient-database.py".

To check the contents inside the database by entering the database:
1. Open a terminal.
2. Get to the folder where the file "patient-database.py" is (along with all the previously mentioned python and json files).
3. Get inside the folder "database" with the command "cd database/" - this is the folder where i have my database file "my-database.db".
4. Run the command "sqlite3" (this package needs to be installed).
5. Now inside sqlite3, to open the database, run ".open my-database.db".
6. Activate the foreign keys by running "PRAGMA foreign_keys = ON;" (because they always start turned off in sqlite).
7. To view the contents in a prettier way, run the commands ".headers on" and ".mode columns".
8. Finally, run sql queries, such as: "select * from patient;".
9. To exit sqlite, run the command ".exit".

**How to populate the database with more json files:**

1. Add the json file to the directory where are all the other python and json files.
2. Add the name of the file to the json files list in line 18 ("patient-database.py").
___
