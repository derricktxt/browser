# Chapter 1 - Web Browser Engineering
# Derrick Jeffers
# this file should replecate the processes of telnet

import socket
import ssl

class url:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self):
        s = socket.socket(
                    family = socket.AF_INET,
                    type = socket.SOCK_STREAM,
                    proto = socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        
        responseHeaders = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            responseHeaders[header.casefold()] = value.strip()
        
        assert "transfer-encoding" not in responseHeaders
        assert "content-encoding" not in responseHeaders

        content = response.read()
        s.close()
        return content

def show(body):
    inTag = False
    for char in body:
        if char == "<":
            inTag = True
        elif char == ">":
            inTag = False
        elif not inTag:
            print(char, end="")

def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(url(sys.argv[1]))
