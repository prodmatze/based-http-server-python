import socket  # noqa: F401


response_200 = b"HTTP/1.1 200 OK\r\n\r\n"
response_400 = b"HTTP/1.1 404 Not Found\r\n\r\n"


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, client_address = server_socket.accept()
    print(f"Incomming connection from client adress: {client_address}")

    req_msg = client_socket.recv(1024)
    print(f"Client sent req_msg: {req_msg}")

    url = get_url_from_request(req_msg)

    response = None
    if url == "/":
        response = response_200
    else:
        response = response_400

    client_socket.send(response)
        

    

def get_url_from_request(request):
    request_string = request.decode("utf-8")
    request_string_split_0 = request_string.split("GET")

    request_string_split_1 = request_string_split_0[1].split("HTTP/1.1")

    url = request_string_split_1[0].strip()

    print(f"Extracted URL: {url} from request!")

    return url



if __name__ == "__main__":
    main()

