# Health Informatics - Project 1

The *HL7 Fast Healthcare Interoperability Resources* ([FHIR](http://www.hl7.org/fhir/stu3/)) standards framework is built on a set of modular resources that can easily be assembled into working systems. For instance, the [*Patient*](http://hl7.org/fhir/STU3/patient.html) resource covers data about patients involved in a wide range of health-related activities, including the demographic information necessary to support the clinical, administrative, financial and logistic procedures. The FHIR website gives a description for the resource, detailing how the information can be encoded in different formats (e.g., XML or JSON). A corresponding high-level diagram is as follows.

![Patient uml](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient_uml.png)

**Q1 -** Derive a Relational Model to hold the information of the *Patient* resource. You may start by an Entity-Relationship (ER) model of the resources and then convert the ER model to the Relational Model, or you can just map the UML model of the resources into a relational schema directly. Then, implement the database in a database management system of your choice (**suggestion**: [*sqlite*](https://www.sqlite.org/index.html)). Your answer should contain **(i)** the Relational 3 Schema of the module and **(ii)** the SQL instructions to define the relational schema of the database.
___
**(i)**

patient (<ins>patient_db_id</ins>, active, gender, birthDate, deceasedBoolean, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthInteger, photo, generalPractitioner)

animal (<ins>patient_db_id</ins>, species, breed, genderStatus)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

link (<ins>patient_db_id</ins>, other, type)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

contact (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, relationship, gender, organization, period)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

communication (<ins>patient_db_id</ins>, language, preferred)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

address (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, use, type, textt, line, city, district, state, postalCode, country, period)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;contact_db_id: FK (contact)

identifier (<ins>patient_db_id</ins>, use, type, system, value, period, assigner)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

name (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, use, textt, family, given, period, prefix, suffix)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;contact_db_id: FK (contact)

telecom (<ins>patient_db_id</ins>, <ins>contact_db_id</ins>, system, value, use, rank, period)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patient_db_id: FK (patient)

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