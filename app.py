from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///exemplo.db')
app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {
            'message': 'Hello World',
            'version': '0.1.0'
        }


class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM user")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        name = request.json['name']
        email = request.json['email']

        conn.execute(
            "INSERT INTO user values(null, '{0}', '{1}')".format(name, email)
        )

        query = conn.execute('SELECT * FROM user order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self):
        conn = db_connect.connect()
        code = request.json['id']
        name = request.json['name']
        email = request.json['email']

        conn.execute("UPDATE user set " +
                     "name='" + str(name) +
                     "' email ='" + str(email) +
                     "' where id=%d" % int(code))

        query = conn.execute("SELECT * FROM user where id=%d" % int(code))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


class UserById(Resource):
    def delete(self, code):
        conn = db_connect.connect()
        conn.execute("DELETE FROM user where id=%d" % int(code))
        return {
            "status": "success"
        }

    def get(self, code):
        conn = db_connect.conect()
        query = conn.execute("SELECT * FROM user where id=%d" % int(code))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


api.add_resource(HelloWorld, '/')
api.add_resource(Users, "/users")
api.add_resource(UserById, "/users/<id>")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
