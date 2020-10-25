import sqlite3

statement = "CREATE TABLE \"Videos\" ( `course` TEXT NOT NULL, `courseID` TEXT NOT NULL, `week` TEXT NOT NULL, `name` TEXT NOT NULL, `pageUrl` TEXT NOT NULL UNIQUE, `videoUrl` TEXT, `srtUrl` TEXT, PRIMARY KEY(`pageUrl`) )"

database = sqlite3.connect("example.db")
database.execute(statement)
database.commit()