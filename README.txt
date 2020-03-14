LINUX ENVIRONMENT INSTRUCTIONS

TO CHECK THE CONTENTS INSIDE THE DATABASE BY RUNNING MY PROGRAM THAT HAS ACCESS TO THE DATABASE:
1. Open a terminal.
2. Get to the folder where the file "patient-database.py" is.
3. Run the command "python3 patient-database.py".

TO CHECK THE CONTENTS INSIDE THE DATABASE BY ENTERING THE DATABASE:
1. Open a terminal.
2. Get to the folder where the file "patient-database.py" is.
3. Get inside the folder "database" with the command "cd database/".
4. Run the command "sqlite3" (this package needs to be installed).
5. Now inside sqlite3, to open the database, run ".open my-database.db".
6. Activate the foreign keys by running "PRAGMA foreign_keys = ON;" (because they always start turned off in sqlite).
7. To view the contents in a prettier way, run the commands ".headers on" and ".mode columns".
8. Finally, run sql queries, such as: "select * from patient;".
9. To exit sqlite, run the command ".exit".