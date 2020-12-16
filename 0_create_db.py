import sqlite3

if __name__ == "__main__":
	statement = "CREATE TABLE \"videos\" ( `course_name` TEXT NOT NULL, `course_id` TEXT NOT NULL, `week` TEXT NOT NULL, 'video_in_week' INTEGER DEFAULT NULL, `video_name` TEXT NOT NULL, `page_url` TEXT NOT NULL UNIQUE, `video_url` TEXT, `srt_url` TEXT, `file_exists` INTEGER DEFAULT 0, PRIMARY KEY(`page_url`) )"

	database = sqlite3.connect("main.db")
	database.execute(statement)
	database.commit()