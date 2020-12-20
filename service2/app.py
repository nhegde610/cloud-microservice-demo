from flask import Flask,jsonify,request,abort
from flask_cors import CORS
from time import gmtime,strftime
import json
import sqlite3

app = Flask(__name__)
CORS(app,resources={r"/api/*": {"origins":"*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR']= False


@app.route("/api/users",methods=['GET'])
def get_users():
    conn = sqlite3.connect('mydb.db')
    print("opened database")
    api_list = []
    cursor = conn.execute("SELECT username, password, id from users")
    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['password'] = row[1]
        a_dict['id'] = row[2]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list': api_list})

@app.route("/api/users",methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)
    user = {
            'username' : request.json['username'],
            'password' : request.json['password']
        }
    return jsonify({'status':add_user(user)}),201

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    api_list=[]
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=?",(new_user['username'],))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        data = (new_user['username'],new_user['password'])
        print(data)
        cursor.execute("INSERT into users (username,password) values(?,?)",data)

        conn.commit()
        return "Success"
    conn.close()
    return jsonify(a_dict)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3001,debug=True)
