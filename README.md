# Health informatics project 1

The *HL7 Fast Healthcare Interoperability Resources* (FHIR[¹]) standards framework is built on a set of modular resources that can easily be assembled into working systems. For instance, the *Patient*[²] resource covers data about patients involved in a wide range of health-related activities, including the demographic information necessary to support the clinical, administrative, financial and logistic procedures. The FHIR website gives a description for the resource, detailing how the information can be encoded in different formats (e.g., XML or JSON). A corresponding high-level diagram is as follows.

![Patient uml](https://github.com/BeatrizRCorreia/health_informatics_project1/blob/master/patient_uml.png)

Q1 - Derive a Relational Model to hold the information of the *Patient* resource. You may start by an Entity-Relationship (ER) model of the resources and then convert the ER model to the Relational Model, or you can just map the UML model of the resources into a relational schema directly. Then, implement the database in a database management system of your choice (**suggestion**: *sqlite*[³]). Your answer should contain (i) the Relational 3 Schema of the module and (ii) the SQL instructions to define the relational schema of the database.

Q2 - Write a program to populate the relational database from JSON files encoding *Patient* resources according to the HL7-PHIR format (**suggestion**: use Python with the sqlite library[⁴]). You can file example JSON files in the *Patient* description[⁵]. You should be able to load the General Person Example[⁶]. 

[¹]: http://www.hl7.org/fhir/stu3/
[²]: http://hl7.org/fhir/STU3/patient.html
[³]: https://www.sqlite.org/index.html
[⁴]: https://docs.python.org/2/library/sqlite3.html
[⁵]: http://hl7.org/fhir/STU3/patient-examples.html
[⁶]: http://hl7.org/fhir/STU3/patient-example.json.html