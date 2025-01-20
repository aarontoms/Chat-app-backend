import redis
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})

load_dotenv()
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=host, port=port, password=password)

ttl = 60

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

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "success"}), 200

@app.route('/<groupid>/send', methods=['POST'])
def send(groupid):
    data = request.get_json()
    print(data)
    session_groupid = data.get("session_groupid")
    sender = data.get("username")
    message_content = data.get("text")
    id = data.get("id")
    # messageid = r.incr(f"{groupid}:counter")
    msg = {
        "messageid": id,
        "sender": sender,
        "message": message_content,
    }
    r.hset(f"{groupid}:messages:{id}", mapping=msg)
    r.expire(f"{groupid}:messages:{id}", ttl)
    # r.expire(f"{groupid}:counter", ttl + 10)

    return jsonify({"status": "success", "messageid": id}), 200

@app.route('/<groupid>/send', methods=['GET'])
def test(groupid):
    return jsonify({"status": "success", "message":groupid}), 200

@app.route('/<groupid>/postname', methods=['POST'])
def postname(groupid):
    data = request.get_json()
    name = data.get("username")
    r.set(f"{groupid}:username", name)
    r.expire(f"{groupid}:username", ttl + 20)
    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True)