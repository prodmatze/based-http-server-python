import socket  # noqa: F401
import threading
import os
import os.path

try:
    files_path = "/tmp/data/codecrafters.io/http-server-tester/"
    files_list = os.listdir(files_path)
except FileNotFoundError:
    print("dont need the files here lol")

accepted_encodings = {"gzip": "gzip"}

response_200 = b"HTTP/1.1 200 OK\r\n\r\n"
response_201 = b"HTTP/1.1 201 Created\r\n\r\n"

response_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"


def build_response_200(content_type, content, encoding = None):
    content_length = len(content)

    encoding_line = "\r\n"
    if encoding:
        encoding_line = f"Content-Type: {content_type}\r\n"

    return (
        f"HTTP/1.1 200 OK"
        f"{encoding_line}"
        f"Content-Encoding: {encoding}\r\n"
        f"Content-Length: {content_length}"
        f"\r\n\r\n{content}"
    ).encode("utf-8")


def handle_request(client_socket, client_address):
    req_msg = client_socket.recv(1024)
    print(f"Client sent req_msg: {req_msg}")

    request_method = get_request_method(req_msg)
    request_body = get_request_body(req_msg)

    print(f"REQUEST TYPE: {request_method}")

    url = get_url_from_get_request(req_msg)
    sub_urls = get_sub_urls(url)

    response = None

    match request_method:
        case "GET":
            if sub_urls:
                match sub_urls[0]:
                    case "/" :
                        response = response_200
                    case "echo":
                        content_type = "text/plain"
                        accepted_encoding = get_header_value_from_request(req_msg, "Accept-Encoding")
                        encoding = accepted_encodings.get("accepted_encoding", None) if accepted_encoding else None
                        response = build_response_200(content_type, sub_urls[1])
                    case "user-agent":
                        content_type = "text/plain"
                        user_agent = get_header_value_from_request(req_msg, "User-Agent:")
                        response = build_response_200(content_type, user_agent)
                    case "files":
                        content_type = "application/octet-stream"
                        file_name = os.path.basename(sub_urls[1])
                        if file_name in files_list:
                            content = open(os.path.join(files_path, file_name), "r").read()
                            response = build_response_200(content_type, content)
                        else:
                            response = response_404
                    case _ :
                        response = response_404
            
            elif url == "/":
                response = response_200
            else:
                response = response_404
        case "POST":
            if sub_urls:
                match sub_urls[0]:
                    case "files":
                        file_name = os.path.basename(sub_urls[1])
                        open(os.path.join(files_path, file_name), "w").write(request_body)
                        response = response_201

    print(f"SENDING RESPONSE: {response}")
    client_socket.send(response)
    client_socket.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

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

        
def get_url_from_get_request(request):
    request_string = request.decode("utf-8")
    request_string_split_0 = request_string.split(" ", 1)

    request_string_split_1 = request_string_split_0[1].split("HTTP/1.1")

    url = request_string_split_1[0].strip()
    print(f"Extracted URL: {url} from request!")
    
    return url

def get_sub_urls(url):
    endpoints = [e for e in url.split("/") if e]
    return endpoints

def get_header_value_from_request(request, header_key):
    request_string = request.decode("utf-8")

    header_value = None
    for line in request_string.split("\r\n"):
        if line.startswith(header_key):
            header_value = line.split(header_key, 1)[1].strip()

            return header_value

    return None

def get_request_method(request):
    request_string = request.decode("utf-8")
    request_method = request_string.split(" ", 1)[0].strip()

    return request_method

def get_request_body(request):
    request_string = request.decode("utf-8")
    request_body = request_string.split("\r\n")[-1].strip()

    return request_body


    





if __name__ == "__main__":
    main()

