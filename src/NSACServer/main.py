import json, requests, urllib.parse
from datetime import datetime as dt
from http.server import BaseHTTPRequestHandler, HTTPServer


CONTENT_URL = "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/content.json"
PAGE_URL = "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/%s/%s"
TLDS_URL = "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/tlds.txt"

curpath = "example.nsac"

class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
                path = globals().get("curpath", "example.nsac")
                path2 = urllib.parse.urlparse(self.path).path

                if len(path2) == 0:
                    path2 = "index.html"

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(requests.get(
                    PAGE_URL % (path, path2)
                ).text, "utf-8"))

content = requests.get(CONTENT_URL)
content = json.loads(content.text)

tlds = requests.get(TLDS_URL).text

def cmd_whois() -> str:
    domain = input("Enter domain name: ")
    domain = domain.split(".")[-2:]

    if domain[-1] not in tlds.splitlines():
        return "Invalid TLD"
    
    mappedContent = list(map(lambda a: a["website"], content))
    
    try:
        idx = mappedContent.index({"dn": domain[0], "tld": domain[1]})
    except (ValueError, IndexError):
        return "Website not found"
        
    date = dt(content[idx]["registryDate"][2],
              content[idx]["registryDate"][1],
              content[idx]["registryDate"][0])
    
    return (f"Registrar: {content[idx]["registrar"]}\n" \
            f"Registry Date: {date.date().isoformat()}")

def cmd_hostdom() -> str:
    global curpath
    domain = input("Enter domain name: ")
    domain = domain.split(".")[-2:]

    if domain[-1] not in tlds.splitlines():
        return "Invalid TLD"

    mappedContent = list(map(lambda a: a["website"], content))
    
    try:
        mappedContent.index({"dn": domain[0], "tld": domain[1]})
    except (ValueError, IndexError):
        return "Website not found"
    
    port = input("Enter port to host domain at: ")

    try:
        port = int(port)
    except (ValueError, TypeError):
        port = 8000
    
    curpath = ".".join(domain)
    
    print(f"Serving {curpath} at localhost:{port}")
    httpserver = HTTPServer(("localhost", port), Handler)

    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        httpserver.server_close()

    del httpserver
    return "Stopped serving"

def main() -> None:
    print("NSACServer - Enter command")
    print("--------------------------")
    print("1 - WHOIS lookup")
    print("2 - Host domain")
    print("E - Exit")

    while True:
        cmd = input(">> ").upper()
        if cmd == "":
            pass
        elif cmd == "1":
            print(cmd_whois())
        elif cmd == "2":
            print(cmd_hostdom())
        elif cmd == "E":
            exit()
        else:
            print("Unknown command")
            
if __name__ == "__main__":
    main()
