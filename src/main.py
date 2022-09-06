""" A bookmark server which support 

"""
#! user/bin/env/python3

import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Dict
from urllib.parse import parse_qs
import requests
import threading
from socketserver import ThreadingMixIn

# Use Dict to save all shortname: longuri pair
memory:Dict = {
    'cat': 'https://www.wikidata.org/wiki/Q146',
    'dog': 'https://www.wikidata.org/wiki/Q144'
}

index_page:str = """
<!DOCTYPE html>
<head>
    <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/0/08/Simple_icon_time.svg">
    <title>Bookmark Server</title>
</head>
<body>
    <form action="/" method="post">
        <label for="shortname">
            short name
            <input type="text" name="shortname" id="shortname" >
        </label>
        <br>
        <label for="longuri">
            long URI
            <input type="url" name="longuri" id="longuri" >
        </label>
        <br>
        <button type="submit"> Submit </button>
    </form>
    <hr>
    <p>
        <h3>URI in server</h3>
        <ul>
            {} <!--old bookmarks here-->
        </ul>
    </p>
</body>
"""

page_404:str = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <title> 404 Error </title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>404 Not Found</h1>
        <br>
        <h2>
            {} <!-- put error reason here -->
        </h2>
        <button onclick="goto_index()">Back to Home page</button>
        <script>
            function goto_index(){{
                location.replace("/")
            }}
        </script>
    </body>
</html>
"""

page_400:str = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>400 Bad Request</title>
    </head>
    <bod>
        <h2>400 Bad Request</h2>
        <br>
        <p>
            {} <!--Error message here-->
        </p>
        <button onclick="goto_index()">Back to Homepage</button>
        <script>
            function goto_index()
            {{
                location.replace(url="/")
            }}
        </script>
    </bod>
</html>
"""

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."

class BookMarkServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        # "receive uri: {self.path}"
        shortname:str = self.path[1:]
        if shortname != "":
            if shortname in memory:
                self.__response_303_longuri(longuri=memory[shortname])
            else:
                self.__response_404_page(err_message=f"Server don't recognize shortname: {shortname}.")
        else:
            self.__response_index_page()
        return
    
    def do_POST(self) -> None:
        # Decode form data {"shortname":_,"longuri":_}
        content_length:int = int(self.headers.get('Content-Length',0))
        body:str = self.rfile.read(content_length).decode()
        params:dict = parse_qs(body)
        if("shortname" not in params or "longuri" not in params):
            self.__response_400_page(f"Missing paramenters: {params}")
        else:
            shortname:str = params.get("shortname")[0]
            longuri:str = params.get("longuri")[0]
            if(shortname in memory):
                #404
                self.__response_404_page(err_message=f"Your shortname {shortname} is already exists.")
            elif(not self.__check_longuri(longuri)):
                #404
                self.__response_404_page(err_message=f"Your longuri {longuri} is not exists.")
            else:
                #save shortname and longuri into memory
                memory[shortname] = longuri
                #redirect to 303 homepage
                self.__response_303_longuri('/')
        return 

    def __response_index_page(self)->None:
        "Return index page, render bookmarks into our index_page"
        # turn memory bookmark into html link
        bookmarks:list = []
        for shortname, longuri in memory.items():
            bookmarks.append(f"<li>{shortname}: {longuri}</li>")
        new_page:str = index_page.format("\n".join(bookmarks))
        self.send_response(200)
        self.send_header('Content-Length',len(new_page))
        self.send_header('Content-Type', "text/html; charset=utf8")
        self.end_headers()
        self.wfile.write(new_page.encode())
        return
    
    def __response_303_longuri(self,longuri:str)->None:
        "Redirect user to long uri"
        self.send_response(303)
        self.send_header('Location',longuri)
        self.end_headers()
        return
    
    def __response_400_page(self, err_message:str)->None:
        new_page:str = page_400.format(err_message)
        self.send_response(400)
        self.send_header("Content-Type","text/html; charset=utf8")
        self.send_header("Content-Length", len(new_page))
        self.end_headers()
        self.wfile.write(new_page.encode())
        return

    def __response_404_page(self, err_message:str)->None:
        "Response 404 page with err_message"
        newpage:str = page_404.format(err_message)
        self.send_response(404)
        self.send_header('Content-Length', len(newpage))
        self.send_header('Content-Type','text/html; charset=utf8')
        self.end_headers()
        self.wfile.write(newpage.encode())
        return
    
    def __check_longuri(self, longuri:str)->bool:
        "Check longuri, if uri exist, return true"
        try:
            res:requests.Response = requests.get(url=longuri)
            return res.status_code == 200
        except requests.RequestException:
            return False
        except:
            return False

def main():
    port:int = int(os.environ.get('PORT',8000))
    server_address = ('', port)
    # httpd:HTTPServer = HTTPServer(server_address=server_address,RequestHandlerClass=BookMarkServerHandler)
    httpd:HTTPServer = ThreadHTTPServer(server_address=server_address,RequestHandlerClass=BookMarkServerHandler)
    httpd.serve_forever()
    pass

if __name__=="__main__":
    main()