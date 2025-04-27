class Request:
    def __init__(self, req_data):

        self.raw_data = req_data
        self.text = req_data.decode("utf-8")

        self.method = self.get_request_method()

        self.url = self.get_url()
        self.sub_urls = self.get_sub_urls()

        self.headers = self.get_headers()
        self.body = self.get_request_body()


    def get_request_method(self):
        request_method = self.text.split(" ", 1)[0].strip()
        return request_method

    def get_url(self):
        request_string_split_0 = self.text.split(" ", 1)
        request_string_split_1 = request_string_split_0[1].split("HTTP/1.1")

        url = request_string_split_1[0].strip()
        print(f"Extracted URL: {url} from request!")

        return url

    def get_sub_urls(self):
        endpoints = [e for e in self.url.split("/") if e]
        return endpoints

    def get_headers(self):
        headers = {}
        lines = self.text.split("\r\n")

        for line in lines[1:]: #skip request line
            if line == "":
                break #end of headers

            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        return headers

    def get_request_body(self):
        request_body = self.text.split("\r\n")[-1].strip()

        return request_body

