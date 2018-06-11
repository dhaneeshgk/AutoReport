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
        data_set = {"Results":[i for i in data_set if i["ClientName"].lower().find(clientName.lower())>=0]}
        return jsonify(data_set)

class clients(Resource):

    def get(self):
        data_set = json.loads(open("DATA_SET.json","r").read())
        return {"Results":jsonify(data_set)}

class fav_client(Resource):

    def get(self):
        data_set = json.loads(open("Fav_JSON.json","r").read())
        return {"Results":jsonify(data_set)}


class contact_client(Resource):

    def get(self,clientName):
        data_set = json.loads(open("DATA_SET.json","r").read())
        return {"Results":jsonify(data_set)}


api.add_resource(test_links_wittyparrot,'/test_links_wittyparrot/')
api.add_resource(clients_list, '/clients/clientName/<clientName>')
api.add_resource(fav_client, '/clients/favorites')
api.add_resource(contact_client, '/clientmanager/clients/clientName/<clientName>')
api.add_resource(clients, '/clients')