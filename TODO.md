# This file will list things we didn't have time to do and could be improvements for the future of this project.

 - Handle parallelization of requests. Currently, the Server implementation (network/server.py) tries to create threads for each client. However, the clients completely ignore these threads. Does ccg2lambda & the others libraries even support threading & parallelization?
 - Create a web interface for the project. It should graft upon the TCP API and display the results in a web page. That also implies hosting the server code on a server somewhere, so that it's actually accessible.
