import socket  # noqa: F401


response_200 = b"HTTP/1.1 200 OK\r\n\r\n"
response_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"

def build_echo_response(content):
    content_length = len(content)

    response = f"HTTP/1.1 200 OK \r\n Content-Type: text/plain \r\n Content-Length:{content_length} \r\n \r\n {content}".encode("utf-8")

    return response

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, client_address = server_socket.accept()
    print(f"Incoming connection from client adress: {client_address}")

    req_msg = client_socket.recv(1024)
    print(f"Client sent req_msg: {req_msg}")

    url = get_url_from_get_request(req_msg)
    sub_urls = get_sub_urls(url)

    response = None

    print(f"Sub urls: {sub_urls}")

    match sub_urls[0]:
        case "/" :
            response = response_200
        case "echo":
            response = build_echo_response(sub_urls[1])
        case _ :
            response = response_404

    client_socket.send(response)
        

    

#GET requests
def get_url_from_get_request(request):
    request_string = request.decode("utf-8")
    request_string_split_0 = request_string.split("GET")

    request_string_split_1 = request_string_split_0[1].split("HTTP/1.1")

    url = request_string_split_1[0].strip()

    print(f"Extracted URL: {url} from request!")

    return url

def get_sub_urls(url):
    endpoints = [e for e in url.split("/") if e]
    return endpoints





if __name__ == "__main__":
    main()

