import redis
from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
import os, random, string, bcrypt, json

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

load_dotenv()
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=host, port=port, password=password)

ttl = 600

@app.route('/', methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
@app.route('/*', methods=['OPTIONS'])
def handle_options(path=None):
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    password = data.get("password")
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    roomid = ''.join(random.choices(string.ascii_uppercase, k=3))
    r.set(f"{roomid}:password", password)
    r.expire(f"{roomid}:password", ttl + 20)

    return jsonify({"roomid": roomid}), 200

@app.route('/<groupid>/postname', methods=['POST'])
def postname(groupid):
    data = request.get_json()
    username = data.get("username")
    userid = data.get("userid")
    r.rpush(f"{groupid}:joined_users", json.dumps(data))
    r.expire(f"{groupid}:joined_users", ttl + 20)
    r.expire(f"{groupid}:password", ttl + 20)
    
    joined_users = []
    for user in r.lrange(f"{groupid}:joined_users", 0, -1):
        joined_users.append(user.decode())
    print(joined_users)
    socketio.emit(f"{groupid}_joined", {"joined_users": joined_users})
    
    return jsonify({"username": username, "userid": userid, "roomid": groupid}), 200

@app.route('/<groupid>/postpassword', methods=['POST'])
def postpassword(groupid):
    data = request.get_json()
    password = data.get("password")
    stored_password = r.get(f"{groupid}:password")
    if not stored_password:
        return jsonify({"status": 404, "message": "Room does not exist"}), 404
    if bcrypt.checkpw(password.encode(), stored_password):
        return jsonify({"status": 200, "message": "Joined chat"}), 200
    else:
        return jsonify({"status": 401, "message": "Invalid password"}), 401

@app.route('/<groupid>/getname', methods=['POST'])
def getname(groupid):
    data = request.get_json()
    userid = data.get("userid")
    
    joined_users = [user.decode() for user in r.lrange(f"{groupid}:joined_users", 0, -1)]
    for user in joined_users:
        user = json.loads(user)
        if user.get("userid") == userid:
            return jsonify({"username": user["username"], "users": joined_users}), 200
        
    return jsonify({"status": 404, "message": "User not found"}), 404

@app.route('/<groupid>/send', methods=['POST'])
def send(groupid):
    data = request.get_json()
    print(data)
    sender = data.get("sender")
    message_content = data.get("text")
    id = data.get("id")
    timestamp = data.get("time")
    msg = {
        "sender": sender,
        "message": message_content,
        "messageid": id,
        "time": timestamp
    }
    print(msg)
    r.hset(f"{groupid}:messages:{id}", mapping=msg)
    r.expire(f"{groupid}:messages:{id}", ttl)
    r.expire(f"{groupid}:joined_users", ttl + 20)
    r.expire(f"{groupid}:password", ttl + 20)
    socketio.emit(f"{groupid}_message", msg)

    return jsonify({"status": "success", "messageid": id}), 200

@app.route('/<groupid>/getmessages', methods=['POST'])
def getmessages(groupid):
    data = request.get_json()
    username = data.get("username")
    joined_users = [json.loads(user.decode()) for user in r.lrange(f"{groupid}:joined_users", 0, -1)]
    if not any(user.get("username") == username for user in joined_users):
        return jsonify({"status": 404, "message": f"User {username} not found"}), 404

    messages = []
    for key in r.scan_iter(f"{groupid}:messages:*"):
        message = r.hgetall(key)
        messages.append({k.decode(): v.decode() for k, v in message.items()})

    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    socketio.run(app)