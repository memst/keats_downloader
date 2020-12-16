import os
import sqlite3

import kd_utilities

def check_exists(database):
    database.execute("UPDATE videos SET file_exists = 0")

    for (page_url,) in database.execute("SELECT page_url FROM videos WHERE video_url IS NOT NULL"):
        paths = kd_utilities.get_paths(page_url, database, online=False)

        if os.path.isfile(paths['file_path']):
            database.execute("UPDATE videos SET file_exists = 1 WHERE page_url = ?", (page_url,))

if __name__ == "__main__":
    database = kd_utilities.open_database()

    check_exists(database)

    database.commit()