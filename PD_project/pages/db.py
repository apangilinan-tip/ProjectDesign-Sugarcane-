import sqlite3
from pathlib import Path
import sys


DB_FILE_PATH = Path(__file__).resolve().parent.parent / 'canecheck.db'

class DbPage:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_path = DB_FILE_PATH.resolve()

    def setup(self):
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            # --- Session Table ---
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Session (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT
                )''')

            # --- Detection Table ---
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Detection (
                    detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    sequence INTEGER NOT NULL,
                    detection_time TEXT NOT NULL,
                    image_file TEXT,
                    variety_id INTEGER NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES Session(session_id)
                )''')

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"DATABASE SETUP ERROR at {self.db_path}: {e}", file=sys.stderr)
            if self.conn:
                try: self.conn.close()
                except sqlite3.Error: pass
            self.conn = None
            self.cursor = None
            return False
        except Exception as e:
            print(f"GENERAL ERROR during DB setup at {self.db_path}: {e}", file=sys.stderr)
            self.conn = None
            self.cursor = None
            return False

    def close(self):
        if self.conn:
            try:
                self.conn.commit()
                self.conn.close()
            except sqlite3.Error as e:
                print(f"Error closing database connection {self.db_path.name}: {e}", file=sys.stderr)
            finally:
                 self.conn = None
                 self.cursor = None

if __name__ == "__main__":
    print(f"Running DbPage setup test on: {DB_FILE_PATH.resolve()}")
    db_manager = DbPage()
    if db_manager.setup():
        print("Database setup/check successful.")
        try:
            db_manager.cursor.execute("SELECT COUNT(*) FROM Session")
            count = db_manager.cursor.fetchone()[0]
            print(f"Current session count: {count}")
        except Exception as e:
             print(f"Test query failed: {e}")
        finally:
             db_manager.close()
             print("Connection closed.")
    else:
        print("Database setup failed.")