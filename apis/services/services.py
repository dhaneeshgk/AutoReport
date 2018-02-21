from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import db_path

# db_path = 'postgresql://postgres:Vidya@11@localhost:5433/users'
db_connect  = create_engine(db_path)

def check_for_run():
    conn = db_connect.connect()
    query = conn.execute("select * from {table_name} where status=w".format(table_name=table_name))
