from flask import Flask, render_template, request,send_file
from flask_restful import Resource, Api
from json import dumps
# from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from scripts.scripts import validate_headers
from sqlalchemy.sql import func
from config import db_path
from dbs import dbs
import random
from datetime import datetime
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)




class Manage_Users(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(20))
    access_token = db.Column(db.String(20))
    role = db.Column(db.String(10))
    token_type = db.Column(db.String(10))

    def __init__(self,name, email, password,access_token,role,token_type):
        self.name = name
        self.email = email
        self.password = password
        self.access_token = access_token
        self.role = role
        self.token_type = token_type


class manage_users(Resource):

    def get(self):
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            query = dbs.get_table("users")
            # print(query['keys'])
            return jsonify({'users': [{"name":i[query['keys'].index("name")],"email":i[query['keys'].index("email")],"role":i[query['keys'].index("role")]} for i in query["values"]]})

        return jsonify(res_v)

    def post(self):
        users_l =[list(i)[0] for i in dbs.get_table("users")["values"]]
        status = []
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if "users" in data and isinstance(data["users"],list):
                for i in request.get_json()["users"]:
                    if i["role"]=="user":i.update({"access_token":"nnnnnnnnnnnnnnnnnnnn","token_type":"u","role":"USER","email":i['email'].lower()})
                    elif i["role"]=="admin":
                        i.update({"access_token":"nnnnnnnnnnnnnnnnnnnn","token_type":"a","role":"ADMIN","email":i['email'].lower()})
                    if i["email"] in users_l:
                        status.append({"status":False,"remarks":"user '{0}' already exists".format(i['email'])})
                    else:
                        print(i)
                        d_s = dbs.insert_row("users",which_=i)
                        if d_s["status"]:
                            status.append({"status":True,"remarks":"user with email id '{0}' added successfully".format(i['email'])})
                        else:
                            d_s.update({"remarks":"user '{0}' was not added".format(i['email'])})
                            status.append(d_s)
                return jsonify(status)
            else:
                return jsonify({"status":False,"remarks":"Invalid Json"})
        else:
            return jsonify(res_v)

    def put(self):

        users_l =[list(i)[0] for i in dbs.get_table("users")["values"]]
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if not data["email"] in users_l:
                return {"status":False,"remarks":"user not exists to update"}
            else:
                if data["role"]=="user":i.update({"token_type":"u"})
                elif data["role"]=="admin":i.update({"token_type":"a"})
                d_s = dbs.get_row("users",
                where_={"email":data["email"]},which_={"password":data["password"],"role":data["role"]})
                if d_s["status"]:
                    return {"status":True,"remarks":"user is updated successfully","email":data["email"],"password":data["password"]}
                else:
                    return jsonify(d_s)
        else:
            return jsonify(res_v)

    def delete(self):
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            users_l =[list(i)[0] for i in dbs.get_table("users")["values"]]
            if not data["email"] in users_l:
                return {"status":False,"remarks":"user not exists to delete"}
            else:
                d_s = dbs.delete_row("users",where_={"email":data["email"]})
                if d_s["status"]:
                    return {"status":True,"remarks":"user '{0}' deleted successfully".format(data["email"])}
                else:
                    return jsonify(d_s)
        else:
            return jsonify(res_v)


class user_login(Resource):
    def post(self):
        res_v = validate_headers(request.headers,validate_token=False)
        access_token = "nnnnnnnnnnnnnnnnnnnn"
        if res_v["status"]:
            users_lp =[[list(i)[0],list(i)[1],list(i)[2], list(i)[3],list(i)[4]] for i in dbs.get_table("users")["values"]]
            users_l = [i[0] for i in users_lp]
            data = request.get_json()
            if data["email"] in users_l:
                if data["password"] == users_lp[users_l.index(data["email"])][1]:
                    if users_lp[users_l.index(data["email"])][2] == access_token or not users_lp[users_l.index(data["email"])][2]:
                        key = ''.join(random.choice('0123456789ABCDEFGIKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@$#') for i in range(20))
                        a_s = dbs.update_access_token("users",access_token=key,email=data["email"])
                        print(a_s)
                        if a_s["status"]:
                            return jsonify({"status":True,"remarks":"user authenticated successfully",
                            "access_token":key,"token_type":users_lp[users_l.index(data["email"])][4]})
                        else:
                            return jsonify(a_s)
                    else:
                        return jsonify({"status":True,"remarks":"user authenticated successfully",
                        "access_token":users_lp[users_l.index(data["email"])][2],
                        "token_type":users_lp[users_l.index(data["email"])][4]})
                else:
                    return jsonify({"status":False,"remarks":"password mismatch"})
            else:
                return jsonify({"status":False,"remarks":"user is not registered"})
        else:
            return jsonify(res_v)

class validate_auth(Resource):
    def post(self):
        res_v = validate_headers(request.headers,validate_token=False)
        if res_v["status"]:
            users_lp =[[list(i)[0],list(i)[1],list(i)[2]] for i in dbs.get_table("users")["values"]]
            users_l = [i[0] for i in users_lp]
            users_t = [i[2] for i in users_lp]
            data = request.get_json()
            if data["access_token"] in users_t:
                return {"status":True,"remarks":"validation of user access_token successfull","email":users_lp[users_t.index(data["access_token"])][0]}
            else:
                return {"status":False,"remarks":"validation of user access_token unsuccessfull"}
        else:
            return jsonify(res_v)

class logout(Resource):
    def post(self):
        res_v = validate_headers(request.headers,validate_token=False)
        access_token = "nnnnnnnnnnnnnnnnnnnn"
        if res_v["status"]:
            users_lp =[[list(i)[0],list(i)[1],list(i)[2]] for i in dbs.get_table("users")["values"]]
            users_t = [i[2] for i in users_lp]
            data = request.get_json()
            if data["access_token"] in users_t:
                email = users_lp[users_t.index(data["access_token"])][0]
                a_s = dbs.update_access_token("users",access_token=access_token,email=email)
                if a_s["status"]:
                    return jsonify({"status":True,"remarks":"user logged out successfully"})
                else:
                    return jsonify(a_s)
            else:
                return jsonify({"status":False,"remarks":"user not logged out successfully"})
        else:
            return jsonify(res_v)






class Manage_VMS(db.Model):
    __tablename__ = "vms"
    vm = db.Column(db.String(120), primary_key=True)
    vm_type = db.Column(db.String(1))
    os = db.Column(db.String(20))
    office365 = db.Column(db.String(1))
    status = db.Column(db.String(1))

    def __init__(self, vm,os,office365,status):
        self.vm = vm
        self.os = os
        self.vm_type = vm_type
        self.office365 = office365
        self.status = status

class manage_vms(Resource):

    def get(self):
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            d_s = dbs.get_table("vms")
            if d_s['status']:
                return {'vms': [{"vm":i[0],"os":i[1],"office365":i[2],"status":i[3]} for i in d_s['values']]}
            else:
                return jsonify(d_s)
        else:
            return jsonify(res_v)

    def post(self):

        vms_l =[list(i)[0] for i in dbs.get_table("vms")["values"]]
        status = []
        data = request.get_json()

        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if "vms" in data and isinstance(data["vms"],list):
                for i in request.get_json()["vms"]:
                    if i["vm"] in vms_l:
                        status.append({"status":False,"remarks":"virtual machine '{0}' already exists in database".format(i['vm'])})
                    else:
                        d_s = dbs.insert_row("vms",which_=i)
                        if d_s["status"]:
                            status.append({"status":True,"remarks":"virtual machine '{0}' added successfully".format(i['vm'])})
                        else:
                            status.append({"status":False,"remarks":"virtual machine '{0}' not added".format(i['vm'])})
                return jsonify(status)
            else:
                return jsonify({"status":False,"remarks":"Invalid Json"})
        else:
            return jsonify(res_v)


    def put(self):

        vms_l =[list(i)[0] for i in dbs.get_table("vms")["values"]]
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if not data["vm"] in vms_l:
                return {"status":False,"remarks":"virtual machine not exists to update"}
            else:
                which_ = {i: data[i] for i in data if i!="vm"}
                where_ = {"vm":data["vm"]}
                d_s = dbs.update_row(table_name="vms",)
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"virtual machine info is updated successfully","vm":data["vm"]})
                else:
                    return jsonify(d_s)
        else:
            return jsonify(res_v)

    def delete(self):
        status = []
        vms_l =[list(i)[0] for i in dbs.get_table("vms")["values"]]
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            for i in data["vms"]:
                if not i in vms_l:
                    status.append({"status":False,"remarks":"virtual machine not exists to delete","vm":i})
                else:
                    d_s = dbs.delete_row(table_name="vms",where_={"vm":i})
                    if d_s["status"]:
                        status.append({"status":True,"remarks":"virtual machine '{0}' is deleted successfully".format(i)})
                    else:
                        return jsonify(d_s)
        else:
            return jsonify(res_v)
        return jsonify(status)

class Manage_Scheduled_Tasks(db.Model):
    __tablename__ = "scheduled_tasks"
    id = db.Column(db.String(16),primary_key=True)
    date = db.Column(db.String(10))
    time = db.Column(db.String(15))
    task = db.Column(db.String(120),unique=True)
    description = db.Column(db.String(200))
    vm = db.Column(db.String(20))
    environment = db.Column(db.String(10))
    test_suite = db.Column(db.String(50))
    schedule_date = db.Column(db.String(10))
    schedule_time = db.Column(db.String(10))
    status = db.Column(db.String(1))

    def __init__(self,id,date,time,task,descripton,vm,status,environment):
        self.id = id
        self.date = date
        self.time = time
        self.task = task
        self.description = description
        self.vm = vm
        self.environment = environment
        self.test_suite = test_suite
        self.schedule_date = schdule_date
        self.schedule_time = schedule_time
        self.status = status


class schedule_vms(Resource):

    def get(self):
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            d_s = dbs.get_table(table_name="scheduled_tasks")
            if d_s["status"]:
                tasks = {'tasks':[{d_s["keys"][row.index(i)]:i for i in row}for row in d_s["values"]]}
                return jsonify(tasks)
            else:
                return jsonify(d_s)
        else:
            return jsonify(res_v)

    def post(self):
        tasks = [list(i)[3] for i in dbs.get_table(table_name="scheduled_tasks")["values"]]
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if "task" in data:
                if not data["task"] in tasks:
                    t = datetime.today()
                    data.update({"id":"".join(str(t.timestamp()).split(".")),"date":str(t.date()),
                    "time":str(t.time()).split(".")[0],"status":"Y"})
                    print(data)
                    d_s = dbs.insert_row(table_name="scheduled_tasks",which_=data)
                    if d_s["status"]:
                        return jsonify({"status":True,"remarks":"Task '{0}' has been scheduled successfully".format(data["task"])})
                    else:
                        return jsonify(d_s)
                else:
                    return jsonify({"status":False,"remarks":"Task '{0}' with same name already exists".format(data["task"])})
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)

    def put(self):

        data = request.get_json()
        res_v = validate_headers(request.headers)
        tasks = [list(i)[3] for i in dbs.get_row(table_name="scheduled_tasks")["values"]]

        if res_v["status"]:
            if data and "task" in data:

                if data["task"] in tasks:
                    which_ = {i:data[i] for i in data if i!= "task"}
                    where_ = {"task": data["task"]}
                    d_s = dbs.update_row(table_name="scheduled_tasks",which_=which_,where_=where_)
                    if d_s["status"]:
                        return jsonify({"status":False,"remarks":"task '{0}' as been upated successfully".format(data["format"])})
                    else:
                        jsonify(d_s)
                else:
                    jsonify({"staus":False,"remarks":"task not exists to update","task":data["task"]})
            else:
                return jsonify({"status":False,"remarks":"Invalid Json"})
        else:
            return jsonify(res_v)

    def delete(self):
        data = request.get_json()
        res_v = validate_headers(request.headers)
        res = dbs.get_table(table_name="scheduled_tasks")
        tasks = [i[res["keys"].index("task")] for i in res["values"]]

        if res_v["status"]:
            if data and "task" in data:
                if data["task"] in tasks:
                    d_s = dbs.delete_row(table_name="scheduled_tasks",where_=data)
                    if d_s["status"]:
                        return jsonify({"status":False,"remarks":"Task '{0}' as been deleted successfully".format(data["task"])})
                    else:
                        jsonify(d_s)
                else:
                    return jsonify({"status":False,"remarks":"Task '{0}' not exists to delete".format(data["task"])})
            else:
                return jsonify({"status":False,"remarks":"Invalid Json"})
        else:
            return jsonify(res_v)


class Update_Details(db.Model):
    __tablename__ = "update_database"
    key_code = db.Column(db.String(5), primary_key=True)
    status = db.Column(db.String(1))
    description = db.Column(db.String(200))
    counts = db.Column(db.Integer)

    def __init__(self,key_code,staus,description,count):
        self.key_code = key_code
        self.status = status
        self.description = description
        self.counts = count

class update_info(Resource):

    def get(self):

        res_v = validate_headers(request.headers)
        if res_v["status"]:
            d_s = dbs.get_row(table_name="update_database",which_="all",where_={"status":"Y"})
            if d_s["status"]:
                keycodes = {list(i)[0]:list(i)[3] for i in d_s["values"]}
                return jsonify(keycodes)
            return jsonify(d_s)
        else:
            return jsonify(res_v)


    def post(self):

        data = request.get_json()
        res_v = validate_headers(request.headers)

        if res_v["status"]:
            if "key_codes" in data:
                which_ = {}
                d_s = dbs.insert_row(table_name="update_database",which_=data["key_codes"])
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Key Codes added successfully"})
                else:
                    return jsonify(d_s)
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)

    def put(self):

        data = request.get_json()
        res_v = validate_headers(request.headers)

        if res_v["status"]:
            if "key_code" in data:
                which_ = {}
                if "status" in data:
                    which_.update({"status":data["status"]})
                if "description" in data:
                    which_.update({"description":data["description"]})

                d_s = dbs.update_row(table_name="update_database",where_={"key_code":data["key_code"]},
                    which_=which_)

                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Key Code updated successfully"})
                else:
                    return jsonify(d_s)
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)

    def delete(self):

        data = request.get_json()
        res_v = validate_headers(request.headers)

        if res_v["status"]:
            if "key_code" in data:
                d_s = dbs.delete_row(table_name="update_database",where_={"key_code":data["key_code"]})
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Key Code deleted successfully"})
                else:
                    return jsonify(d_s)
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)

class Update_Server_Info(db.Model):
    __tablename__ = "update_server_info"
    environment = db.Column(db.String(5), primary_key=True)
    url = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.String(1))
    descritption = db.Column(db.String(200))

    def __init__(self,environment,staus,url,description):
        self.environment = key_code
        self.url = url
        self.status = status
        self.description = description

class update_server_info(Resource):

    def get(self):
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            return jsonify({'environments':[{"name":list(i)[0],"url":list(i)[1],"status":list(i)[2]} for i in dbs.get_table(table_name="update_server_info")["values"]]})
        return jsonify(res_v)

    def post(self):

        status = []
        data = request.get_json()

        res_v = validate_headers(request.headers)
        if res_v:
            if data:
                d_s = dbs.insert_row(table_name="update_server_info",which_=data)
                if d_s["status"]:
                    # print("pass")
                    return jsonify({"status":True,"remarks":"Environment '{0}' is added successfully".format(data["environment"])})
                else:
                    # print("fail")
                    d_s.update({"remarks":"Environment '{0}' is not added successfully".format(data["environment"])})
                    return jsonify(d_s)
        else:
            return jsonify(res_v)

    def put(self):

        status = []
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if data:
                where_ = {"environment":data["environment"]}
                which_ = dict()
                if "url" in data:
                    which_.udate({"url":data["url"]})
                if "status" in data:
                    which_.udate({"status":data["status"]})
                d_s = dbs.insert_row(table_name="update_server_info",where_=where_,which_=which_)
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Environment '{0}' status is updated successfully".format(data["environment"])})
                else:
                    return jsonify(d_s.update({"remarks":"Environment '{0}' status is not updated successfully".format(data["environment"])}))
        else:
            return jsonify(res_v)

    def delete(self):
        status = []
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if data:
                d_s = dbs.delete_row(table_name="update_server_info",where_={"environment":data["environment"]})
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Environment '{0}' status is deleted successfully".format(data["environment"])})
                else:
                    return jsonify(d_s.update({"remarks":"Environment '{0}' status is not deleted successfully".format(data["environment"])}))
        else:
            return jsonify(res_v)


class Test_Suite(db.Model):
    __tablename__ = "test_suites"
    name = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(100))
    status = db.Column(db.String(1))
    environment = db.Column(db.String(50))

    def __init__(self,name,staus,description):
        self.name = key_code
        self.description = description
        self.status = status
        self.environment = environment


class test_suites(Resource):

    def get(self):
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            d_s = dbs.get_table('test_suites')
            # print(d_s)
            if d_s['status']:
                return jsonify({'test_suites':[{d_s['keys'][suite.index(i)]:i for i in suite} for suite in d_s['values']],'status':True})
        return jsonify(res_v)

    def post(self):

        status = []
        data = request.get_json()
        d_ts = dbs.get_table('test_suites')
        test_suites_p = [i[d_ts['keys'].index("name")] for i in d_ts["values"]]
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if "name" in data:
                if not data["name"] in test_suites_p:
                    d_s = dbs.insert_row(table_name="test_suites",which_=data)
                    if d_s["status"]:
                        return jsonify({"status":True,"remarks":"Test Suite '{0}' is added successfully".format(data["name"])})
                    else:
                        d_s.update({"status":False,"remarks":"Test Suite '{0}' is not added successfully".format(data["name"])})
                        return jsonify(d_s)
                else:
                    return jsonify({"status":False,"remarks":"Test Suite '{0}' is already exists".format(data["name"])})
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)

    def put(self):

        status = []
        data = request.get_json()
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if data:
                where_ = {"environment":data["environment"]}
                which_ = dict()
                if "url" in data:
                    which_.udate({"url":data["url"]})
                if "status" in data:
                    which_.udate({"status":data["status"]})
                d_s = dbs.insert_row(table_name="update_server_info",where_=where_,which_=which_)
                if d_s["status"]:
                    return jsonify({"status":True,"remarks":"Environment '{0}' status is updated successfully".format(data["environment"])})
                else:
                    return jsonify(d_s.update({"remarks":"Environment '{0}' status is not updated successfully".format(data["environment"])}))
        else:
            return jsonify(res_v)

    def delete(self):
        status = []
        data = request.get_json()
        d_ts = dbs.get_table('test_suites')
        test_suites_p = [i[d_ts['keys'].index("name")] for i in d_ts["values"]]
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            if 'test_suites' in data:
                for i in data['test_suites']:
                    if i in test_suites_p:
                        d_s = dbs.delete_row(table_name="test_suites",where_={'name':i})
                        if d_s["status"]:
                            return jsonify({"status":True,"remarks":"Test Suite '{0}' is deleted successfully".format(i)})
                        else:
                            return jsonify(d_s.update({"remarks":"Test Suite '{0}' is not deleted successfully".format(i)}))
                    else:
                        return jsonify({"status":False,"remarks":"Test Suite '{0}' is not exists to delete".format(i)})
            else:
                return jsonify({"status":False,"remarks":"Invalid JSON"})
        else:
            return jsonify(res_v)


class docs(Resource):

    def get(self):
        file_name = request.url.split("file=")[-1]
        print(file_name,"hey")
        file_path = os.getcwd()+"/server_ware_house/"
        if file_name:
            if os.path.exists(file_path+file_name):
                return send_file(file_path+file_name,
                attachment_filename=file_name,
                as_attachment=True)
        return send_file(file_path+"read.txt",
        attachment_filename="read.txt",
        as_attachment=True)

    def post(self):
        d_ts = dbs.get_table('test_suites')
        test_suites_p = [i[d_ts['keys'].index("name")] for i in d_ts["values"]]
        res_v = validate_headers(request.headers,validate_content_type=False)
        if res_v["status"]:
            file = request.files['upload_file']
            file_path = os.getcwd()+"/server_ware_house/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file.save(file_path+file.filename)
            return jsonify({"status":True,"remarks":"file '{0}' is added successfully".format(file.filename)})
        else:
            return jsonify(res_v)

    def delete(self):
        data = request.get_json()
        # print(data)
        d_ts = dbs.get_table('test_suites')
        # test_suites_p = [i[d_ts['keys'].index("name")] for i in d_ts["values"]]
        res_v = validate_headers(request.headers)
        if res_v["status"]:
            file_path = os.getcwd()+"/server_ware_house/"
            if os.path.exists(file_path+data["file"]):
                os.unlink(file_path+data["file"])
            return jsonify({"status":True,"remarks":"file '{0}' is deleted successfully".format(data["file"])})
        else:
            return jsonify(res_v)


api.add_resource(manage_users, '/manage_users')
api.add_resource(user_login,'/user_login')
api.add_resource(validate_auth,'/validate_auth')
api.add_resource(logout,'/logout')
api.add_resource(manage_vms,'/manage_vms')
api.add_resource(schedule_vms,'/schedule_vms')
api.add_resource(update_info,'/update')
api.add_resource(update_server_info,'/envs')
api.add_resource(test_suites,'/test_suites')
api.add_resource(docs,'/docs')




if __name__ == '__main__':
    db.create_all()
    app.run(port=5300,debug=True)
