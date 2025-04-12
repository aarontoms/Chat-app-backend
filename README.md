# 🛠️ Temporary Group Chat Backend

This is the **Flask backend** for the Temporary Group Chat App.  
Handles group creation, messaging, and auto-deletion of messages after 10 minutes.

---

## 🚀 Tech Stack

| Category         | Technology              |
|------------------|-------------------------|
| Backend          | Flask (Python)          |
| Database         | Redis                   |
| Hosting          | Koyeb                   |
| Redis Client     | redis                   |

---

## 📦 Features

- 🔑 Join/Leave groups using passwords.
- 🗨️ Send and receive messages.
- 🕑 Messages automatically delete after 10 minutes.
- 🚀 Fast backend with Redis caching.
- 🔒 Secure, environment variable-based config.

---

## 🛠️ Developer Guide

### 1. Clone the Repository

```bash
git clone https://github.com/aarontoms/Chat-app-backend.git
cd group-chat-backend
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create Environment Variables

Create a `.env` file in the project root:

```env
REDIS_HOST = <'redis-host-url'>
REDIS_PORT = <your_redis_port>
REDIS_PASSWORD = <redis_password>
```

---

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

---

## 📜 Important Notes

- Redis must be running and reachable for message expiry to work.
- Environment variables are **mandatory** for the app to run.

---

## 📄 Endpoints Overview

| Method | Endpoint         | Description                    |
|--------|------------------|--------------------------------|
| POST   | `/create`           | Create a group                   |
| POST   | `/postpassword`          | Join a group                  |
| POST   | `/send`   | Send a message to a group       |
| GET    | `/getmessages`   | Get all messages in a group     |

---

## 🧩 Folder Structure

```
/backend
  ├── app.py
  ├── requirements.txt
  └── .env (not committed)
```

---

## 📣 Contributing

Feel free to fork, open issues, and submit PRs!

---
