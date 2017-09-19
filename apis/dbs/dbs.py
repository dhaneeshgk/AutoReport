from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# from config import db_path

db_path = 'postgresql://postgres:Vidya@11@localhost:5433/users'
db_connect  = create_engine(db_path)


def get_table(table_name="users"):
    conn = db_connect.connect()
    query = conn.execute("select * from {table_name}".format(table_name=table_name))
    # print(query.cursor.fetchall())
    return {"status":True,"keys":query.keys(),"values":query.cursor.fetchall()}

def update_access_token(table_name="users",**data):
    try:
        conn = db_connect.connect()
        conn.execute("UPDATE users SET access_token = '{access_token}' WHERE email ='{email}'".format(access_token=data["access_token"],email=data["email"]))
        return {"status":True}
    except Exception as e:
        return {"status":False,"error":str(e)}

def get_row(table_name="users",where_=None,which_=None):
    try:
        conn = db_connect.connect()

        if which_:
            if which_ == "all":
                to_set = '*'
            else:
                da_f = "{0} = '{1}'"
                to_set = ""
                for i in list(which_.keys())[:-1]:
                    to_set = da_f.format(i,which_[i]) + "," + to_set
                to_set = to_set+da_f.format(list(which_.keys())[-1],which_[list(which_.keys())[-1]])
        if where_:
            da_f = "{0} = '{1}'"
            to_point = ""
            for i in list(where_.keys())[:-1]:
                to_point = da_f.format(i,where_[i]) + "," + to_point

            to_point = to_point+da_f.format(list(where_.keys())[-1],where_[list(where_.keys())[-1]])


        if which_=="all":
            query = conn.execute("SELECT * FROM {table_name} WHERE {to_point}".format(table_name=table_name,to_set=to_set,to_point=to_point))
            return {"status":True,"keys":query.keys(),"values":query.cursor.fetchall()}
        else:
            query = conn.execute("SELECT {to_set} FROM {table_name} WHERE {to_point}".format(table_name=table_name,to_set=to_set,to_point=to_point))
            return {"status":True,"keys":query.keys(),"values":query.cursor.fetchall()}

    except Exception as e:
        return {"status":False,"error":str(e)}


def update_row(table_name="users",where_=None,which_=None):
    try:

        conn = db_connect.connect()

        if which_:
            da_f = "{0} = '{1}'"
            to_set = ""
            for i in list(which_.keys())[:-1]:
                to_set = da_f.format(i,which_[i]) + "," + to_set
            to_set = to_set+da_f.format(list(which_.keys())[-1],which_[list(which_.keys())[-1]])

        if where_:
            da_f = "{0} = '{1}'"
            to_point = ""
            for i in list(where_.keys())[:-1]:
                to_point = da_f.format(i,where_[i]) + "," + to_point
            to_point = to_point+da_f.format(list(where_.keys())[-1],where_[list(where_.keys())[-1]])

        # print("to_set",to_set)
        # print("to_point",to_point)
        # print("UPDATE {table_name} SET {to_set} WHERE {to_point}".format(table_name=table_name,to_set=to_set,to_point=to_point))
        if where_:
            query = conn.execute("UPDATE {table_name} SET {to_set} WHERE {to_point}".format(table_name=table_name,to_set=to_set,to_point=to_point))
            return {"status":True,"keys":query.keys(),"values":None}
        else:
            query = conn.execute("UPDATE {table_name} SET {to_set} ".format(table_name=table_name,to_set=to_set,to_point=to_point))
            return {"status":True,"keys":query.keys(),"values":None}
    except Exception as e:
        return {"status":False,"error":str(e)}


def insert_row(table_name="users",where_=None,which_=None):
    try:
        # print(which_)
        conn = db_connect.connect()
        if which_ and where_:
            da_f = "{0} = '{1}'"
            to_set = ""
            for i in list(which_.keys())[:-1]:
                to_set = da_f.format(i,which_[i]) + "," + to_set
            to_set = to_set+da_f.format(list(which_.keys())[-1],which_[list(which_.keys())[-1]])
        else:
            da_f = "'{0}'"
            to_set = ""
            t_d = get_table(table_name)
            if table_name=="users":
                lc = -2
            else:
                lc = -1
            to_set = da_f.format(which_[list(t_d["keys"])[0]])
            # print(t_d["keys"])
            for i in list(t_d["keys"])[1:]:
                to_set = to_set+","+da_f.format(which_[i])

        if where_:
            da_f = "{0} = '{1}'"
            to_point = ""
            for i in list(where_.keys())[:-1]:
                to_point = da_f.format(i,where_[i]) + "," + to_point
            to_point = to_point+da_f.format(list(where_.keys())[-1],where_[list(where_.keys())[-1]])

        if where_:
            query = conn.execute("INSERT INTO {table_name} VALUES {to_set} WHERE {to_point}".format(table_name=table_name,to_set=to_set))
            return {"status":True,"keys":query.keys(),"values":{}}
        else:
            # print("INSERT INTO {table_name} VALUES ({to_set})".format(table_name=table_name,to_set=to_set))
            query = conn.execute("INSERT INTO {table_name} VALUES ({to_set})".format(table_name=table_name,to_set=to_set))
            return {"status":True,"keys":query.keys(),"values":{}}

    except Exception as e:
        return {"status":False,"error":str(e)+" from dbs"}


def delete_row(table_name="users",where_=None,which_=None):
    try:
        conn = db_connect.connect()

        da_f = "{0} = '{1}'"
        to_point = ""
        for i in list(where_.keys())[:-1]:
            to_point = da_f.format(i,where_[i]) + "," + to_point
        to_point = to_point+da_f.format(list(where_.keys())[-1],where_[list(where_.keys())[-1]])

        query = conn.execute("DELETE FROM {table_name} WHERE {to_point}".format(table_name=table_name,to_point=to_point))
        return {"status":True,"keys":query.keys(),"values":{}}
    except Exception as e:
        return {"status":False,"error":str(e)+" from dbs"}


def create_keycode():

    try:
        conn = db_connect.connect()
        # query_c = conn.execute("ALTER TABLE update_database add column start_vm char(1)")
        # print()
        query = conn.execute("UPDATE update_database SET stop_vm='N'")
    except Exception as e:
        print(e)
        pass


def admin_create_user():
    try:
        conn = db_connect.connect()
        query = conn.execute("INSERT INTO users VALUES ('Dhaneesh G K','dhaneesh.gk@gmail.com','welcome123','nnnnnnnnnnnnnnnnnnnn','OWNER','a')")
        query = conn.execute("INSERT INTO users VALUES ('admin','admin@autoreport.com','welcome','nnnnnnnnnnnnnnnnnnnn','OWNER','a')")
        return {"status":True,"remarks":"success"}
    except Exception as e:
        return {"status":False,"remarks":"error {0}".format(str(e))}


if __name__=="__main__":
    create_keycode()
