******* Run my solution - Linux environment instructions: *******

TO CHECK THE CONTENTS INSIDE THE DATABASE BY RUNNING MY PROGRAM THAT HAS ACCESS TO THE DATABASE:
1. Adjust the file path on line 392 ("patient-database.py") to the place in your computer where you want to create the database file "my-database.db".
2. Open a terminal.
3. Get to the folder where the file "patient-database.py" is (along with all the previously mentioned python and json files).
4. Run the command "python3 patient-database.py".

TO CHECK THE CONTENTS INSIDE THE DATABASE BY ENTERING THE DATABASE:
1. Open a terminal.
2. Get to the folder where the file "patient-database.py" is (along with all the previously mentioned python and json files).
3. Get inside the folder "database" with the command "cd database/" - this is the folder where i have my database file "my-database.db".
4. Run the command "sqlite3" (this package needs to be installed).
5. Now inside sqlite3, to open the database, run ".open my-database.db".
6. Activate the foreign keys by running "PRAGMA foreign_keys = ON;" (because they always start turned off in sqlite).
7. To view the contents in a prettier way, run the commands ".headers on" and ".mode columns".
8. Finally, run sql queries, such as: "select * from patient;".
9. To exit sqlite, run the command ".exit".

******* How to populate the database with more json files: *******

1. Add the json file to the directory where are all the other python and json files.
2. Add the name of the file to the json files list in line 18 ("patient-database.py").