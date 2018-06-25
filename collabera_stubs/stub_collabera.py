from flask import Flask, render_template, request,send_file
from flask_restful import Resource, Api
from json import dumps
# from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
# from scripts.scripts import validate_headers,drop_user_creation_email
# from sqlalchemy.sql import func
# from config import db_path
# from dbs import dbs
import random
from datetime import datetime
import os
import json

app = Flask(__name__)
api = Api(app)



class test_links_wittyparrot(Resource):

    def get(self):
        val = request.url
        print(val)
        # val = val.split("#")[1]
        return request.url


class clients_list(Resource):

    def get(self,clientName):
        data_set = json.loads(open("DATA_SET.json","r").read())
        # print(data_set[0]["ClientName"], data_set[0]["ClientName"].find(clientName))
        result = [i for i in data_set if i["ClientName"].lower().find(clientName.lower())>=0]
        data_set = result

        if request.url.find("?location")>=0:
            location = request.url.split("?location=")[-1].lower()
            # d_set_l = {"CorporateHqCountry":"CountryName","CorporateHqState":"StateName","CorporateHqCity":"CityName"}
            data_set_f = [client for client in data_set  if location in [client["CorporateHqCountry"]["CountryName"].lower(),client["CorporateHqState"]["StateName"].lower(),client["CorporateHqCity"]["CityName"].lower()]]
            return jsonify({"Results":data_set_f, "Count":len(data_set_f)})
        else:
            data_set_f = data_set

        return jsonify({"Results":data_set_f, "Count":len(data_set_f)})

class clients(Resource):

    def get(self):
        if request.url.find("?location")>=0:
            location = request.url.split("?location=")[-1].lower()
            data_set = json.loads(open("DATA_SET.json","r").read())
            # d_set_l = {"CorporateHqCountry":"CountryName","CorporateHqState":"StateName","CorporateHqCity":"CityName"}
            data_set_f = [client for client in data_set  if location in [client["CorporateHqCountry"]["CountryName"].lower(),client["CorporateHqState"]["StateName"].lower(),client["CorporateHqCity"]["CityName"].lower()]]
            return jsonify({"Results":data_set_f, "Count":len(data_set_f)})
        elif request.url.split("/clients")[-1]:
            return jsonify({"Results":"Invalid Query", "Count": 0})
        else:
            data_set = json.loads(open("DATA_SET.json","r").read())
            return jsonify({"Results":data_set, "Count":len(data_set)})
        

class fav_client(Resource):

    def get(self):
        data_set = json.loads(open("Fav_JSON.json","r").read())
        return jsonify({"Results":data_set, "Count": len(data_set)})


class contact_client(Resource):

    def get(self,clientName):
        data_set = [i for i in json.loads(open("DATA_SET.json","r").read()) if i["ClientName"].find(clientName)>=0]

        if request.url.find("?location")>=0:
            location = request.url.split("?location=")[-1].lower()
            # d_set_l = {"CorporateHqCountry":"CountryName","CorporateHqState":"StateName","CorporateHqCity":"CityName"}
            data_set_f = [client for client in data_set  if location in [client["CorporateHqCountry"]["CountryName"].lower(),client["CorporateHqState"]["StateName"].lower(),client["CorporateHqCity"]["CityName"].lower()]]
            return jsonify({"Results":data_set_f, "Count":len(data_set_f)})
        else:
            data_set_f = data_set 

        return jsonify({"Results":data_set_f, "Count": len(data_set_f)})


class my_to_dos(Resource):

    def get(self,date=None):
        data_set = json.loads(open("./ToDo-DB/mytodos.json").read())
        return jsonify({"Results":data_set, "Count": len(data_set)})

class update_to_dos(Resource):

    def put(self,todo):
        return jsonify({"Results":"PUT is sucessfull"})

class add_to_dos(Resource):

    def post(self):
        return jsonify({"Results":"Successfully Added to do"})


api.add_resource(test_links_wittyparrot,'/test_links_wittyparrot/')
api.add_resource(clients_list, '/clients/clientName/<clientName>')
api.add_resource(fav_client, '/clients/favorites')
api.add_resource(contact_client, '/clientmanager/clients/clientName/<clientName>')
api.add_resource(clients, '/clients')
api.add_resource(my_to_dos,'/org/us_entr/todos/users/me')
api.add_resource(add_to_dos,'/org/us_entr/todos')
api.add_resource(update_to_dos,'/org/us_entr/todos/<todo>/reminders')


if __name__ == "__main__":
    app.run(port=3200)