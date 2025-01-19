import redis
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=host, port=port, password=password)

ttl = 600  

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
    messageid = r.incr(f"{groupid}:counter")
    msg = {
        "messageid": messageid,
        "sender": sender,
        "message": message_content,
    }
    r.hset(f"{groupid}:messages:{messageid}", mapping=msg)
    r.expire(f"{groupid}:messages:{messageid}", ttl)

    return jsonify({"status": "success"}), 200

@app.route('/<groupid>/send', methods=['GET'])
def test(groupid):
    return jsonify({"status": "success", "message":groupid}), 200

if __name__ == '__main__':
    app.run(debug=True)