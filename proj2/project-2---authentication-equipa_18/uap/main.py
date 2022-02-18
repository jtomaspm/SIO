import cherrypy
import hashlib
from os.path import abspath
import requests
from cryptography import x509
import sec
import sqlite3
import json
from access_db import encrypt_db, decrypt_db

DB_FILE = "db/users.db"
DB_ENC = "db/users.locked"
DB_KEY = "certificates/users.key"



class UAP:

    @cherrypy.expose
    def domainPicker(self):
        return """<div class="log-form tab-pane fade" id="registerForm">
            <h2>Pick a domain</h2>
            <form action="/login" method="post">
                <input type="text" name="domain" placeholder="Domain" />
                <button type="submit" class="btn">Pick Domain</button>
            </form>
        </div>
        </br>
        </br>
        </br>
        <a href="/registerUser">Register User</a>
        <a href="/manageUsers">Manage Users</a>
        """


    @cherrypy.expose
    def registerUser(self):
        return """<div class="log-form tab-pane fade" id="registerForm">
            <h2>Register your new account</h2>
            <form action="/registerToDB" method="post">
                <input type="text" name="uname" placeholder="Username" />
                <input type="password" name="psw" placeholder="Password" />
                <input type="text" name="domain" placeholder="Domain" />
                <button type="submit" class="btn">Register</button>
            </form>
        </div>
        </br>
        </br>
        </br>
        <a href="/domainPicker">Login</a>
        <a href="/manageUsers">Manage Users</a>
        """

    @cherrypy.expose
    def registerToDB(self, uname, psw, domain):
        if psw == "" or sec.check_for_sp_chars(uname):
            raise cherrypy.HTTPRedirect("/?page=register")
        decrypt_db(DB_ENC, DB_KEY, DB_FILE)
        with sqlite3.connect(DB_FILE) as con:
            query = f"SELECT * FROM users WHERE username=\'{uname}\'"
            if len(con.execute(query).fetchall()) != 0:
                encrypt_db(DB_ENC, DB_KEY, DB_FILE)
                raise cherrypy.HTTPRedirect("/registerUser")
            else:
                query = "INSERT INTO users(username, password, domain) VALUES(\'%s\', \'%s\', \'%s\');" % (uname, psw, domain)
                con.execute(query)
                con.commit()

                encrypt_db(DB_ENC, DB_KEY, DB_FILE)
                raise cherrypy.HTTPRedirect("/registerUser") 
        
        
    @cherrypy.expose
    def deleteUser(self, name, domain):
        decrypt_db(DB_ENC, DB_KEY, DB_FILE)
        with sqlite3.connect("db/users.db") as con:
            querry = f"DELETE FROM users WHERE username=\"{name}\" AND domain=\"{domain}\";"
            con.execute(querry)
            con.commit()
        encrypt_db(DB_ENC, DB_KEY, DB_FILE)
        raise cherrypy.HTTPRedirect("/manageUsers")
            

    @cherrypy.expose
    def manageUsers(self):
        pagehtml = """
                        <html>
                            <head>
                            <title>UAP - manage users</title>
                                <style>
$gray-100: #f7fafc;
$gray-200: #edf2f7;
$gray-300: #e2e8f0;
$gray-400: #cbd5e0;
$gray-500: #a0aec0;
$gray-600: #718096;
$gray-700: #4a5568;
$gray-800: #2d3748;
$gray-900: #1a202c;

$white: #ffffff;

.container {
  max-width: 500px;
  margin: auto;
  margin-top: 3rem;
  overflow-x: auto;
}

table {
    font-family: "Open Sans", sans-serif;
    position: relative;
    border-collapse: collapse;
    border-spacing: 0;
    table-layout: auto;
    width: 100%;
    border: none;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

    * {
        border: none;
    }
    white-space: nowrap;
    thead tr {
        color: $gray-800;
        font-size: 1rem;
        font-weight: 500;
        text-align: left;

        th {
            background: $gray-200;
            padding: 0.75rem 1.5rem;
            vertical-align: middle;
        }
    }

    tbody {
        tr:nth-child(odd) td {
            background: $white;
        }

        tr:nth-child(even) td {
            background: $gray-200;
        }
        td {
            color: $gray-900;
            text-align: left;
            padding: 1.5rem 1.5rem;
            vertical-align: middle;
            font-size: 1.125rem;
            font-weight: normal;
        }
    }

    tr:last-child td:first-child {
        border-bottom-left-radius: 0.5rem;
    }

    th:first-child {
        border-top-left-radius: 0.5rem;
    }

    tr:last-child td:last-child {
        border-bottom-right-radius: 0.5rem;
    }

    th:last-child {
        border-top-right-radius: 0.5rem;
    }
  
  tr>th:first-child,tr>td:first-child {
    position: sticky;
    left: 0;
  }
}
                                </style>
                            </head>

                            <body>
                            <div class="container">
                                <table>
                                <tr>
                                    <th>Account Name</th>
                                    <th>Domain</th>
                                    <th>Delete</th>
                                </tr>"""

        decrypt_db(DB_ENC, DB_KEY, DB_FILE)
        with sqlite3.connect("db/users.db") as con:
            print(":::::::::::::::::::::::::::::::::::::")
            users = con.execute(f"SELECT username, domain FROM users").fetchall()
            print(users)
            for user in users:
                name = user[0]
                domain = user[1]
                link = "/deleteUser?domain="+domain+"&name="+name
                pagehtml+="""<tr>
                                <td>"""+name+"""</td>
                                <td>"""+domain+"""</td>
                                <td><a href="""+"\""+link+"\""+""">delete</a></td>
                            </tr>"""
        encrypt_db(DB_ENC, DB_KEY, DB_FILE)

        pagehtml+="""</table> </div>
        </br>
        </br>
        </br>
        <a href="/domainPicker">Login</a>
        <a href="/registerUser">Register User</a>
            </body>            
        </html>
        """
        return pagehtml


    @cherrypy.expose
    def login(self, domain):
        if sec.verifyCertificates(domain):
            pagehtml = """
                        <html>
                            <head>
                            <title>UAP - login</title>
                                <style>
                                    table, th, td {
                                        border:1px solid black;
                                    }
                                </style>
                            </head>

                            <body>
                                <h2>Accounts for domain: """+domain+"""</h2>
                                <table style="width:100%">
                                <tr>
                                    <th>Account Name</th>
                                    <th>Login</th>
                                </tr>"""

            decrypt_db(DB_ENC, DB_KEY, DB_FILE)
            with sqlite3.connect("db/users.db") as con:
                print(domain)
                print(":::::::::::::::::::::::::::::::::::::")
                users = con.execute(f"SELECT username FROM users WHERE domain='{domain}'").fetchall()
                print(users)
                for name in users:
                    name = name[0]
                    link = "/startAut?domain="+domain+"&name="+name
                    pagehtml+="""<tr>
                                    <td>"""+name+"""</td>
                                    <td><a href="""+"\""+link+"\""+""">login</a></td>
                                </tr>"""
            encrypt_db(DB_ENC, DB_KEY, DB_FILE)

            pagehtml+="""</table>
        </br>
        </br>
        </br>
        <a href="/manageUsers">Manage Users</a>
        <a href="/registerUser">Register User</a>
                </body>            
            </html>
            """
            return pagehtml
        else:
            raise cherrypy.HTTPRedirect(403, "invalid certificate")

    @cherrypy.expose
    def startAut(self, domain, name):
        decrypt_db(DB_ENC, DB_KEY, DB_FILE)
        with sqlite3.connect("db/users.db") as con:
                password = con.execute(f"SELECT password FROM users WHERE domain='{domain}' AND username='{name}'").fetchall()[0][0]
                print(password)
        encrypt_db(DB_ENC, DB_KEY, DB_FILE)
        cu = {"name" : name, "password" : password, "nonce": None, "challenge_responce": ["challenge_responce", "current_index"]}
        nonce = requests.get("http://"+domain+"/get_nonce?username="+name).json()
        cu["nonce"] = nonce[name]
        
        cu["challenge_responce"][0] = sec.get_cr(cu["password"], cu["nonce"])
        cu["challenge_responce"][1] = -1

        j = json.dumps(cu)
        with open("db/current_user.json", "w") as f:
            f.write(j)
        raise cherrypy.HTTPRedirect("http://"+domain+"/startAut")
        


    @cherrypy.expose
    @cherrypy.tools.accept(media='application/json')
    def nextChallengeBit(self):
        cu = json.load(open("db/current_user.json"))
        cu["challenge_responce"][1] += 1
        if cu["challenge_responce"][1] >= len(cu["challenge_responce"][0]):
            return json.dumps({"bit": "done"})
        j = json.dumps(cu)
        with open("db/current_user.json", "w") as f:
            f.write(j)
        print(cu["challenge_responce"][1], cu["challenge_responce"][0][cu["challenge_responce"][1]])
            
        return json.dumps({"bit": cu["challenge_responce"][0][cu["challenge_responce"][1]]})


config = {
    '/': {
        'tools.staticdir.root': abspath(".")
    }
}

cherrypy.config.update({'server.socket_port': 4000})


if __name__ == '__main__':
    cherrypy.quickstart(UAP(), "/", config)