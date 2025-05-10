import socket
import threading
import os
import os.path
import random
import gzip

from app.request_parser import Request
#from request_parser import Request

files_path = "/tmp/data/codecrafters.io/http-server-tester/"

REC_BUFFER_SIZE = 1024
PORT = 4221

accepted_encodings_list = ["gzip"]

response_200 = b"HTTP/1.1 200 OK\r\n\r\n"
response_201 = b"HTTP/1.1 201 Created\r\n\r\n"

response_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"


def build_response_200(content_type, content, encoding = None, connection = None):
    if encoding == "gzip":
        content = gzip.compress(content.encode())
    else:
        content = content.encode()

    content_length = len(content)

    headers = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
    )
    
    if encoding:
        headers += f"Content-Encoding: {encoding}\r\n"

    if connection:
        headers += f"Connection: {connection}\r\n"

    headers += "\r\n"

    return headers.encode("utf-8") + content


def handle_request(client_socket, client_address):
    
    #moved here to be able to serve files dynamically, even after server has already started
    try:
        files_list = os.listdir(files_path)
    except FileNotFoundError:
        print("who needs files anyways:")

    while True:
        req_msg = client_socket.recv(REC_BUFFER_SIZE)

        if not req_msg:
            break

        print(f"Client sent req_msg: {req_msg}")

        request = Request(req_msg) #parsed request object

        print(f"REQUEST TYPE: {request.method}")

        req_method = request.method
        req_url = request.url
        req_sub_urls = request.sub_urls
        req_headers = request.headers

        req_body = request.body

        req_accepted_encodings = request.headers.get("Accept-Encoding", None)
        encoding = pick_encoding(req_accepted_encodings) if req_accepted_encodings else None

        req_connection = request.headers.get("Connection", None)

        response = None

        match req_method:
            case "GET":
                if req_sub_urls:
                    match req_sub_urls[0]:
                        case "/" :
                            response = response_200
                        case "echo":
                            content_type = "text/plain"
                            response = build_response_200(content_type, req_sub_urls[1], encoding, req_connection)
                        case "user-agent":
                            content_type = "text/plain"
                            user_agent = req_headers.get("User-Agent", None)
                            print(f"found user agent: {user_agent}")
                            print(f"ALL HEADERS: {req_headers}")
                            response = build_response_200(content_type, user_agent, encoding, req_connection)
                        case "files":
                            content_type = "application/octet-stream"
                            file_name = os.path.basename(req_sub_urls[1])
                            if file_name in files_list:
                                with open(os.path.join(files_path, file_name), "r") as file:
                                    content = file.read()
                                response = build_response_200(content_type, content, encoding, req_connection)
                            else:
                                response= response_404
                        case _ :
                            response = response_404
                
                elif req_url == "/":
                    response = response_200
                else:
                    response = response_404

            #TODO: implement checks for filepath, currently path traversal attacks are possible ...use os.path.abspath()
            case "POST":
                if req_sub_urls:
                    match req_sub_urls[0]:
                        case "files":
                            file_name = os.path.basename(req_sub_urls[1])
                            with open(os.path.join(files_path, file_name), "w") as file:
                                file.write(req_body)
                            response = response_201

        print(f"SENDING RESPONSE: {response}")
        client_socket.send(response)

        if req_headers.get("Connection", None) == "close":
            break

    client_socket.close()


def main():
    server_socket = socket.create_server(("localhost", PORT), reuse_port=True)

    while True:
        # accept incoming TCP connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Incoming connection from client adress: {client_address}")

        thread = threading.Thread(
            target = handle_request,
            args = (client_socket, client_address),
            daemon = True
        )

        thread.start()

        

#TODO: implement more robust encoding strategy, currently encoding is just random lol
def pick_encoding(accepted_encodings_string):
    accepted_encodings = accepted_encodings_string.split(", ")
    available_encodings = []

    for encoding in accepted_encodings:
        if encoding in accepted_encodings_list:
            available_encodings.append(encoding)

    encoding = random.choice(available_encodings) if available_encodings else None

    return encoding

if __name__ == "__main__":
    main()
