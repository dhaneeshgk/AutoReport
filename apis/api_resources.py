from flask import Flask, render_template, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Vidya@11@localhost:5433/users'
db_connect  = create_engine('postgresql://postgres:Vidya@11@localhost:5433/users')
db = SQLAlchemy(app)




class Manage_Users(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(20))

    def __init__(self, email, password):
        self.email = email
        self.password = password

class manage_users(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from users")
        conn.__dict__
        # print(query.cursor.columns)
        # try:
        #     print(query.column_descriptions)
        # except Exception as e:
        #     return jsonify({"status":Fail})
        return jsonify({'users': [{"email":i[0],"password":i[1]} for i in query.cursor.fetchall()]})

    def post(self):
        conn = db_connect.connect()
        users_l =[list(i)[0] for i in conn.execute("select * from users").cursor.fetchall()]
        status = []
        data = request.get_json()
        if "users" in data and isinstance(data["users"],list):
            for i in request.get_json()["users"]:
                if i["email"] in users_l:
                    status.append({"status":False,"remarks":"user '{0}' already exists".format(i['email'])})
                else:
                    conn.execute("INSERT INTO users VALUES ('{email}','{password}')".format(email=i["email"],password=i["password"]))
                    status.append({"status":True,"remarks":"user '{0}' added successfully".format(i['email'])})
            return jsonify(status)
        else:
            return jsonify({"status":False,"remarks":"Invalid Json"})

    def put(self):
        conn = db_connect.connect()
        users_l =[list(i)[0] for i in conn.execute("select * from users").cursor.fetchall()]
        data = request.get_json()
        if not data["email"] in users_l:
            return {"status":False,"remarks":"user not exists to update"}
        else:
            conn.execute("UPDATE users SET password = '{password}' WHERE email = '{email}'".format(email=data["email"],password=data["password"]))
            return {"status":True,"remarks":"user is updated successfully","email":data["email"],"password":data["password"]}

    def delete(self):
        conn = db_connect.connect()
        data = request.get_json()
        users_l =[list(i)[0] for i in conn.execute("select * from users").cursor.fetchall()]
        if not data["email"] in users_l:
            return {"status":False,"remarks":"user not exists to delete"}
        else:
            conn.execute("DELETE FROM users WHERE email == '{email}'".format(email=data["email"]))
            return {"status":True,"remarks":"user deleted successfully"}



class auth_user(Resource):
    def post(self):
        conn = db_connect.connect()
        users_lp =[[list(i)[0],list(i)[1]] for i in conn.execute("select * from users").cursor.fetchall()]
        users_l = [i[0] for i in users_lp]
        data = request.get_json()
        if data["email"] in users_l:
            if data["password"] == users_lp[users_lp.index(data["email"])][1]:
                return {"status":True,"remarks":"user authenticated successfully"}
            else:
                return {"status":False,"remarks":"password mismatch"}
        else:
            return {"status":False,"remarks":"user is not registered"}


class Manage_VMS(db.Model):
    __tablename__ = "vms"
    vm = db.Column(db.String(120), primary_key=True)
    vm_type = db.Column(db.String(1))
    os = db.Column(db.String(20))
    office365 = db.Column(db.String(1))
    # status = db.Column(db.String(1))

    def __init__(self, vm,os,office365,status):
        self.vm = email
        self.os = os
        self.vm_type = vm_type
        self.office365 = office365
        # self.status = status

class manage_vms(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from vms")
        return {'users': [{"vm":i[0],"os":i[1],"office365":i[2],"status":i[3]} for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        vms_l =[list(i)[0] for i in conn.execute("select * from vms").cursor.fetchall()]
        status = []
        data = request.get_json()
        if "vms" in data and isinstance(data["vms"],list):
            for i in request.get_json()["vms"]:
                if i["vms"] in vms_l:
                    status.append({"status":Flase,"remarks":"vm '{0}' already updated in database".format(i['email'])})
                else:
                    conn.execute("INSERT INTO users VALUES ('{vm}','{vm_type}','{os}','{office365}')".format(vm=i["vm"],vm_type=i["vm_type"],os=i["os"],
                    office365=i["office365"]
                    ))
                    status.append({"status":True,"remarks":"vm '{0}' added successfully".format(i['email'])})
            return jsonify(status)
        else:
            return jsonify({"status":False,"remarks":"Invalid Json"})

    def put(self):
        conn = db_connect.connect()
        vms_l =[list(i)[0] for i in conn.execute("select * from vms").cursor.fetchall()]
        data = request.get_json()
        if not data["vm"] in vms_l:
            return {"status":False,"remarks":"user not exists to update"}
        else:
            for i in data:
                if i != "vm":
                    conn.execute("UPDATE vms SET {to_set_n} = '{to_set_v}' WHERE vm = '{vm}'".format(vm=data["vm"],to_set_v=data[i],to_set_n=i))
            return {"status":True,"remarks":"vm info is updated successfully","vm":data["vm"]}



class Manage_Scheduled_Tasks(db.Model):
    __tablename__ = "scheduled_tasks"
    id = db.Column(db.TIMESTAMP,primary_key=True)
    date = db.Column(db.DATE)
    time = db.Column(db.TIME)
    task = db.Column(db.String(120))
    description = db.Column(db.String(200))
    vm = db.Column(db.String(20))
    schedule_date = db.Column(db.String(10))
    schedule_time = db.Column(db.String(10))
    status = db.Column(db.String(1))

    def __init__(self,task,descripton,time,vm,status):
        self.task = task
        self.description = description
        self.time = time
        self.vm = vm
        self.schedule_date = schdule_date
        self.schedule_time = schedule_time
        self.status = status


class schedule_vms(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from scheduled_tasks")
        return {'tasks': [{"date":i[1],"time":i[2],"task":i[3],"vm":i[4],"schedule_date":i[5],"schedule_time":i[6],
        "status":i[7]} for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        vms_l =[list(i)[0] for i in conn.execute("select * from vms").cursor.fetchall()]
        status = []
        data = request.get_json()
        if "vms" in data and isinstance(data["vms"],list):
            for i in request.get_json()["vms"]:
                if i["vms"] in vms_l:
                    status.append({"status":Flase,"remarks":"vm '{0}' already updated in database".format(i['email'])})
                else:
                    conn.execute("INSERT INTO users VALUES ('{vm}','{vm_type}','{os}','{office365}')".format(vm=i["vm"],vm_type=i["vm_type"],os=i["os"],
                    office365=i["office365"]
                    ))
                    status.append({"status":True,"remarks":"vm '{0}' added successfully".format(i['email'])})
            return jsonify(status)
        else:
            return jsonify({"status":False,"remarks":"Invalid Json"})


class Update_Details(db.Model):
    __tablename__ = "update_database"
    key_code = db.Column(db.String(5), primary_key=True)
    status = db.Column(db.String(1))
    def __init__(self,key_code,staus):
        self.key_code = key_code
        self.status = status

class update_info(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from update_database")
        return {}

    def post(self):
        conn = db_connect.connect()
        return request.form




api.add_resource(manage_users, '/users')
api.add_resource(auth_user,'/auth_user')
api.add_resource(manage_vms,'/manage_vms')
api.add_resource(schedule_vms,'/schedule_vms')
api.add_resource(update_info,'/update')


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
