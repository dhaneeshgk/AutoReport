import api_resources

api_resources.db.create_all()
api_resources.app.run(port=5300,debug=True)
