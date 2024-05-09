import socket
import os

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()

    print(msg)

    request_parts = msg.split()
    resource = request_parts[1].lstrip("/")
    if not resource:
        resource = "index.html"

    filename = os.path.join("html", resource)

    try:
        with open(filename, "rb") as file:
            content = file.read()
            response_status = "HTTP/1.1 200 OK\r\n"
    except FileNotFoundError:
        content = b"File not found"
        response_status = "HTTP/1.1 404 Not Found\r\n"

    response = response_status + \
               "Server: SelfMadeServer v0.0.1\r\n" + \
               "Content-type: text/html\r\n" + \
               "Connection: close\r\n\r\n" + \
               content.decode("utf-8")

    conn.send(response.encode())

    conn.close()
