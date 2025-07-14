import sqlite3
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
from langchain.sql_database import SQLDatabase

def configure_database(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    """
    Configures and returns an SQLDatabase instance based on the provided URI and credentials.
    Handles both SQLite and MySQL connections.
    """
    if db_uri == "USE_LOCALDB":
        dbfilepath = (Path(__file__).parent.parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == "USE_MYSQL":
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            raise ValueError("All MySQL connection details (host, user, password, db) must be provided.")
        try:
            engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
            # Attempt to connect to validate credentials and accessibility
            with engine.connect() as connection:
                pass
            return SQLDatabase(engine)
        except (OperationalError, ProgrammingError) as e:
            raise ConnectionError(f"Failed to connect to MySQL database. Please check your credentials and host. Error: {e}")
        except Exception as e:
            raise ConnectionError(f"An unexpected error occurred while connecting to MySQL: {e}")
    else:
        raise ValueError("Invalid database URI option.")