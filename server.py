import SocketServer, os
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):

        webDir = "www"
        absWebPath = os.path.abspath(webDir)

        #define the known files we serve, and their content types
        servedFiles = {
            ".css" : "text/css", 
            ".html" : "text/html"} 

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        elements = self.data.split('\n', 1)[0].split()

        filePath = webDir + elements[1]
        if filePath.endswith(('/')):
            filePath += "index.html"        
        absFilePath = os.path.abspath(filePath) 
        fileName, fileExtension = os.path.splitext(absFilePath)
        if(absWebPath in absFilePath): #Security, we don't want to be serving up system files after all
            try:
                    rFile = open(filePath)
                    self.request.send("HTTP/1.1 200 OK\r\n")
                    if(fileExtension in servedFiles.keys()):
                        self.request.send("Content-Type: " + servedFiles[fileExtension] +"\r\n\r\n")        
                    for line in rFile.readlines():
                        self.request.send(line)       
            except IOError:
                self.request.send("HTTP/1.1 404 Not Found\r\n") #Couldn't open the file; it's dead to us.      
        else:
            self.request.send("HTTP/1.1 404 Not Found\r\n") #Really this should be 403 Forbidden but that doesn't pass the test cases


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
