import redis
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

#redis connection
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")
r = redis.Redis(host=host, port=port, password=password)

groupid = "12345"
ttl_seconds = 10  # TTL in seconds (10 minutes)
messageid = r.incr(f"{groupid}:counter")
r.expire(f"{groupid}:counter", ttl_seconds+10)
senderid = "user2"
message_content = "Hello, 1!"

app.route('/send', methods=['POST'])
def receive():
    data = request.get_json()
    messageid = data.get("messageid")
    senderid = data.get("sender")
    message_content = data.get("message")
    msg = {
        "messageid": messageid,
        "sender": senderid,
        "message": message_content,
    }
    r.hset(f"{groupid}:messages:{messageid}", mapping=msg)
    r.expire(f"{groupid}:messages:{messageid}", ttl_seconds)

    return jsonify({"status": "success"}), 200
