
import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True
# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("search.html") as search:
                archivo = search.read()
            self.wfile.write(bytes(archivo, "utf8"))


        elif "searchDrug" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            try:
                if buscador[2] != "":
                    medicamento = buscador[1] + "=" + buscador[2]
                else:
                    medicamento = buscador[1] + "=" + "10"
            except IndexError:
                medicamento = buscador[1] + "&limit=10"

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient:%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>List of drugs with that active ingredient</h3><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Unknown</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "searchCompany" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            try:
                if buscador[2] != "":
                    medicamento = buscador[1] + "=" + buscador[2]
                else:
                    medicamento = buscador[1] + "=" + "10"
            except IndexError:
                medicamento = buscador[1] + "&limit=10"

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>List of drugs from that company</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Unknown</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "listDrugs" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            limite = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % limite, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug =["<h1>List of random drugs</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>" + n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    drug.append("<li>Unknown</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "listCompanies" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            limite = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" %limite, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>List of random companies</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>"+ n["openfda"]["manufacturer_name"][0]+ "</li>")
                except KeyError:
                    drug.append("<li>Unknown</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))


        elif "listWarnings" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            buscador = self.path.split("=")
            medicamento = buscador[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % medicamento, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)["results"]
            drug = ["<h1>List of random warnings</h1><br>"]
            for n in repos:
                try:
                    drug.append("<li>"+ n["warnings"][0]+ "</li>")
                except KeyError:
                    drug.append("<li>Unknown</li>")

            string = "".join(drug)
            self.wfile.write(bytes(string, "utf8"))

        elif "secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', "Basic realm = DENIED")
            self.end_headers()

        elif "redirect"  in self.path:
            self.send_response(301)
            self.send_header("Location","http://localhost:8000")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            with open("error.html", "r") as s:
                error = s.read()
            self.wfile.write(bytes(error, "utf8"))



        return


Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at %s:%s" % (IP, PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print("Server stopped!")