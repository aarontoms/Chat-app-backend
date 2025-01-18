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

app.route('/<groupid>/send', methods=['POST'])
def send(groupid):
    data = request.get_json()
    local_groupid = data.get("local_groupid")
    messageid = data.get("messageid")
    senderid = data.get("sender")
    message_content = data.get("message")
    msg = {
        "messageid": messageid,
        "sender": senderid,
        "message": message_content,
    }
    r.hset(f"{groupid}:messages:{messageid}", mapping=msg)
    r.expire(f"{groupid}:messages:{messageid}", ttl)

    return jsonify({"status": "success"}), 200

app.route('/<groupid>/send', methods=['GET'])
def test():
    return jsonify({"status": "success"}), 200