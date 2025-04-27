# 🖥️ Based HTTP Server (Python)

This project is a fully working HTTP/1.1 server built from scratch using only Python sockets.

---

## 📋 Features

- Accepts multiple concurrent TCP connections (threaded server)
- Handles basic `GET` and `POST` requests
- Supports file serving from a directory
- Supports gzip compression (`Content-Encoding: gzip`) if requested
- Handles persistent connections (`Connection: keep-alive`)
- Cleanly closes connections when `Connection: close` header is received
- Parses incoming HTTP requests manually (no external libraries)
- Dynamically generates appropriate HTTP responses

---

## 🚀 How to Run Locally

```bash
# Clone this repository
git clone https://github.com/prodmatze/based-http-server-python.git
cd based-http-server-python

# Run the server
python3 app/main.py
```

The server will listen on `localhost:4221`.

---

## 🧪 Example Usage

**Basic GET request:**

```bash
curl http://localhost:4221/
```

**Echo endpoint:**

```bash
curl http://localhost:4221/echo/hello
# Response: "hello"
```

**User-Agent endpoint:**

```bash
curl -A "my-custom-agent" http://localhost:4221/user-agent
# Response: "my-custom-agent"
```

**File download:**

```bash
curl http://localhost:4221/files/filename.txt
```

**Request gzip compressed response:**

```bash
curl --compressed http://localhost:4221/echo/hello
```

**Persistent connections:**

```bash
curl --keepalive-time 60 http://localhost:4221/echo/keepalive
```

---

## 🛠️ Technologies Used

- Python 3
- Standard Library only (`socket`, `threading`, `gzip`, `os`)

---

## ✨ Future Improvements (Optional)

- Better parsing to support HTTP/1.0 and HTTP/2.0 versions
- Support for additional HTTP methods (`PUT`, `DELETE`)
- Improved error handling for file operations
- Timeout handling for idle persistent connections
- Refactor project-structure a little (seperate Class for response, etc)

---

## This project was created as part of the [Codecrafters.io](https://codecrafters.io/) "Build Your Own HTTP Server" challenge, where the goal was to reimplement core HTTP server functionality step-by-step.

