import api_resources
api_resources.db.create_all()
api_resources.app.run(host='0.0.0.0',port=80,debug=True)
