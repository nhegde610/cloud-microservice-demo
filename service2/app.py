from flask import Flask,jsonify,request,abort
from flask_cors import CORS
from time import gmtime,strftime
import json
import sqlite3

app = Flask(__name__)
CORS(app,resources={r"/api/*": {"origins":"*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR']= False

@app.route("/api/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print("opened database successully")
    api_list=[]
    cursor = conn.execute("SELECT buildtime,version,methods,links from apirelease")
    for row in cursor:
        s_dict = {}
        s_dict['version'] = row[0]
        s_dict['buildtime'] = row[1]
        s_dict['methods'] = row[2]
        s_dict['links'] = row[3]
        api_list.append(s_dict)
    conn.close()
    return jsonify({'api_version': api_list}), 200



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

@app.route("/api/msgs",methods=['GET'])
def get_msg():
    conn = sqlite3.connect('mydb.db')
    api_list=[]
    cursor= conn.execute("SELECT id,username,message,msg_time from msg")
    data = cursor.fetchall()
    print(f"data {data} {type(data)}")
    if data !=0:
        for row in data:
            msgs = {}
            msgs['username'] = row[1]
            msgs['message'] = row[2]
            msgs['msg_time'] = row[3]
            print(msgs)
            api_list.append(msgs)
    else:
        return api_list
    conn.close()
    print(api_list)
    return jsonify({'msg_list':api_list})

@app.route("/api/msgs",methods=['POST'])
def add_msg():
    user_msg = {}
    if not request.json or not 'username' in request.json or not 'message' in request.json:
        abort(400)
    user_msg['username'] = request.json['username']
    user_msg['message'] = request.json['message']
    user_msg['msg_time'] = strftime("%Y-%m-%d  %H:%M:%S",gmtime())
    print(user_msg)
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=?",(user_msg['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("INSERT into msg (username,message,msg_time) values(?,?,?)",(user_msg['username'],user_msg['message'],user_msg['msg_time']))
    conn.commit()
    return jsonify({'status':"Success"}),200


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3001,debug=True)
