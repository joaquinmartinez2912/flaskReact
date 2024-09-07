import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId, MongoClient
from flask_cors import CORS

from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Para trabajar la base de datos desde localhost:
    # app.config['MONGO_URI']= 'mongodb://localhost/pythonreactdb'
    # mongo = PyMongo(app)
    # db = mongo.db.users
    
    # Para trabajar la base de datos en la nube:
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.users
    
    #Para hacer el puente entre el puerto del back y el del front.
    CORS(app)
    #Crea el container de la base de datos (vendria a ser el equivalente a una tabla de SQL)

    @app.route('/users', methods=['POST'])
    def createUser():   
        new_user = app.db.users.insert_one({
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        })
        print(str(ObjectId(new_user.inserted_id)))
        return jsonify(str(ObjectId(new_user.inserted_id)))

    @app.route('/users', methods=['GET'])
    def getUsers():
        users = []
        for doc in app.db.users.find():
            users.append({
                '_id': str(ObjectId(doc['_id'])),
                'name': doc['name'],
                'email': doc['email'],
                'password': doc['password']
            })
        return jsonify(users)

    @app.route('/users/<id>', methods=['GET'])
    def getUser(id):
        user = app.db.users.find_one({'_id': ObjectId(id)})
        return jsonify({
                '_id': str(ObjectId(user['_id'])),
                'name': user['name'],
                'email': user['email'],
                'password': user['password']
            })

    @app.route('/users/<id>', methods=['DELETE'])
    def deleteUser(id):
        app.db.users.delete_one({'_id': ObjectId(id)})
        return jsonify({'msg':'user deleted'})

    @app.route('/users/<id>', methods=['PUT'])
    def updateUser(id):
        app.db.users.update_one({'_id': ObjectId(id)},
        {'$set': {
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        }}

        )
        return jsonify({'msg':'user updated'})
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

