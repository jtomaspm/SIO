import cherrypy
import sqlite3
from os.path import abspath
from cryptography.fernet import Fernet
import sec

DB_STRING = "static/db/shop.db"


class App:

    @cherrypy.expose
    def index(self, page="login"):
        html = open('static/index.html').read()

        sec.read_data()

        return html

    # Verify if username and password are in the database
    @cherrypy.expose
    def verifyUser(self, uname, psw):
        if sec.handle_check_ip_request(1, cherrypy.request.headers["Remote-Addr"]):
            raise cherrypy.HTTPError(403, "Forbidden")

        uname = sec.swap_sp_char_for_token(uname)
        psw = sec.swap_sp_char_for_token(psw)

        with sqlite3.connect(DB_STRING) as con:
            query = f"SELECT * FROM User WHERE username=\'{uname}\' AND password=\'{psw}\'"
            if len(con.execute(query).fetchall()) != 0:
                cherrypy.session["uname"] = uname

                raise cherrypy.HTTPRedirect("/search?searchkey=")
            else:
                raise cherrypy.HTTPRedirect("/?page=login")

    # Verify username/password, if doesn't exist create a new account and log in
    @cherrypy.expose
    def registerUser(self, uname, psw):
        if sec.handle_check_ip_request(2, cherrypy.request.headers["Remote-Addr"]):
            raise cherrypy.HTTPError(403, "Forbidden")

        if psw == "" or sec.check_for_sp_chars(uname):
            raise cherrypy.HTTPRedirect("/?page=register")

        with sqlite3.connect(DB_STRING) as con:
            query = f"SELECT * FROM User WHERE username=\'{uname}\'"
            if len(con.execute(query).fetchall()) != 0:
                raise cherrypy.HTTPRedirect("/?page=register")
            else:
                query = "INSERT INTO User(username, password) VALUES(\'%s\', \'%s\');" % (uname, psw)
                con.execute(query)
                con.commit()

                cherrypy.session["uname"] = uname
                raise cherrypy.HTTPRedirect("/search?searchkey=")

    # handle search bar
    @cherrypy.expose
    def search(self, searchkey=""):
        uname = cherrypy.session["uname"]

        if sec.check_for_sp_chars(searchkey):
            raise cherrypy.HTTPRedirect("/search?searchkey=")

        with sqlite3.connect(DB_STRING) as con:
            html = open("static/htmlTemplates/shopHeaderTemplate.html").read()

            html += "<h2 style=\"text-align:center;\">Hello, " + uname + f"</h2><a class=\"btn btn-primary\" href=\"/profile\">Profile</a>"

            html += open("static/htmlTemplates/shopHeaderTemplate2.html").read()

            query = f"SELECT * FROM Game WHERE name LIKE '%{searchkey}%'"
            table = con.execute(query).fetchall()

            if not searchkey == "":
                html += f"<h3 style=\"color: white;\">Search results for '{searchkey}'</h3>"

            html += f"""
                        <form action="/comments" method="get" id="gameForm">
                    """

            for game in table:
                # add valid outputs to html
                html += f"""
                        <div class="col-lg-3 col-sm-6 col-md-3" id="{game[0]}">
                            <button type="submit" name="id_game" value="{game[0]}" class="btn-link">
                                <div class="box-img">
                                    <h4>{game[1]}</h4>
                                    <img src="{game[3]}" alt="" style="max-height: 180px;"/>
                                </div>
                            </button>
                        </div>
                        """

            html += "</form>"
            html += open("static/htmlTemplates/shopFooterTemplate.html").read()
        return html

    # Set up the profile page
    @cherrypy.expose
    def profile(self):
        html = open('static/htmlTemplates/profileTemplate1.html').read()
        html += cherrypy.session["uname"] + "</br></br></br></br>"
        html += open('static/htmlTemplates/profileTemplate2.html').read()

        # Generate random key for action delete account
        key = Fernet.generate_key().decode("utf-8")
        cherrypy.session["key"] = key
        html += f"<input type=\"hidden\" name=\"key\" value=\"{key}\">"

        html += open('static/htmlTemplates/profileTemplate3.html').read()
        html += f"<input type=\"hidden\" name=\"key\" value=\"{key}\">"
        html += open('static/htmlTemplates/profileTemplate4.html').read()

        return html

    @cherrypy.expose
    def deleteAccount(self, key):
        if "key" in cherrypy.session.keys() and cherrypy.session["key"] == key:
            uname = cherrypy.session["uname"]
            with sqlite3.connect(DB_STRING) as con:
                id_user = con.execute(f"SELECT id_user FROM User WHERE username='{uname}'").fetchall()[0][0]
                con.execute(f"DELETE FROM User WHERE id_user={id_user}")
                con.execute(f"DELETE FROM Comment WHERE id_user={id_user}")
                con.commit()

                cherrypy.session.pop("uname", None)
                raise cherrypy.HTTPRedirect("/")

        elif "uname" in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/search")

        else:
            raise cherrypy.HTTPRedirect("/")

    # Logout
    @cherrypy.expose
    def logout(self, key):
        if "key" in cherrypy.session.keys() and cherrypy.session["key"] == key:
            cherrypy.session.pop("uname", None)
            raise cherrypy.HTTPRedirect("/")
        elif "uname" in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/search")

    # Set up the comments html
    @cherrypy.expose
    def comments(self, id_game, preview=""):
        uname = cherrypy.session["uname"]
        # Generate random key for action delete account
        key = Fernet.generate_key().decode("utf-8")
        cherrypy.session["key"] = key

        # check for admin permissions
        admin_user = False
        with open("static/db/SuperUsers.txt") as admins:
            for admin in admins:
                if (str(uname)).strip() == (str(admin)).strip():
                    admin_user = True
                    break

        if sec.check_for_sp_chars(preview):
            raise cherrypy.HTTPRedirect("/comments?id_game=" + str(id_game))

        html = open('static/htmlTemplates/commentTemplate1.html').read()

        # Get the name of the game
        with sqlite3.connect(DB_STRING) as con:
            query = f"SELECT name FROM Game WHERE id_game={id_game}"
            name = con.execute(query).fetchone()[0]
            html += name

        # Get ratings and calculate the avg
        with sqlite3.connect(DB_STRING) as con:
            query = f"SELECT * FROM Comment WHERE id_game={id_game}"
            table = con.execute(query)
            r = 0
            c = 0
            for com in table:
                r += com[2]
                c += 1
            if c == 0:
                c = 1
            r = int(r / c)
            query = f"UPDATE Game SET rating={r} WHERE id_game={id_game}"
            con.execute(query)
            con.commit()

        html += open("static/htmlTemplates/commentTemplate2.html").read()
        html += f"</h2><a class=\"btn btn-primary\" href=\"/profile\">Profile</a>"
        html += f"""<p class="text-center">Rated {r} stars!</p></br>  """

        # Get the comments of the game
        with sqlite3.connect(DB_STRING) as con:
            query = f"SELECT * FROM Comment WHERE id_game={id_game}"
            columns = con.execute(query)

            for col in columns:
                query = f"SELECT username FROM User WHERE id_user={col[3]}"

                user = con.execute(query).fetchone()[0]

                html += f"""<div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-10">
                                            <p>
                                                <strong>{user}</strong>
                        """
                html += """<span class="float-right"><i class="text-warning fa fa-star"></i></span>""" * int(col[2])

                html += f"""
                                            </p>
                                            <div class="clearfix"></div>
                                            <p>{col[1]}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        """
                # generate admin buttons
                if admin_user:
                    html += f"""<div style="display:flex;"><form action="/deleteComment" method="get">
                                                    <input type="hidden" name="commentid" value="{col[0]}">
                                                    <input type=\"hidden\" name=\"key\" value=\"{key}\">
                                                    <button type="submit" class="btn btn-default">delete</button>
                                               </form>"""
                    html += f"""<form action="/modUser" method="get">
                                                    <input type="hidden" name="id_game" value="{id_game}">
                                                    <input type="hidden" name="unametomod" value="{user}">
                                                    <input type=\"hidden\" name=\"key\" value=\"{key}\">
                                                    <button type="submit" class="btn btn-default">mod</button>
                                               </form></div>"""
            html += f"""
                        <form action="/addComment" method="get" id="commentForm">
                        </br>
                        </br>
                        </br>
                        <div class="star_rating">
                            <input type="radio" id="star5" name="rating" class="star" value="5" checked>
                                <label for="star5" class="star" title="5 stars"></label>
                            <input type="radio" id="star4" name="rating" class="star" value="4">
                                <label for="star4" class="star" title="4 stars"></label>
                            <input type="radio" id="star3" name="rating" class="star" value="3">
                                <label for="star3" class="star" title="3 stars"></label>
                            <input type="radio" id="star2" name="rating" class="star" value="2">
                                <label for="star2" class="star" title="2 stars"></label>
                            <input type="radio" id="star1" name="rating" class="star" value="1">
                                <label for="star1" class="star" title="1 stars"></label>
                        </div>
                        <div class="comments">
                            <div class="comment-box add-comment">
                              <span class="commenter-name">
                                <input type="hidden" name="id_game" value="{id_game}"/>
                                <input type="text" placeholder="Add a comment" value="{preview}" name="comment"/>
                                <button type="submit" name="check" value="0" class="btn btn-default">Preview</button>
                                <button type="submit" name="check" value="1" class="btn btn-default">Comment</button>
                              </span>
                            </div>
                        </div>
                        </form>
                        """

        if preview != "":
            html += f"""
                        </br></br></br></br></br></br></br></br>
                        <div class="card">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-10">
                                        <p>
                                            <strong>{user}</strong>
                    """
            html += f"""
                                            </p>
                                            <div class="clearfix"></div>
                                            <p>{preview}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </br></br></br></br></br></br></br></br>
                        """

        html += open('static/htmlTemplates/commentTemplate3.html').read()

        return html

    # User add a comment to a certain id_game
    @cherrypy.expose
    def addComment(self, comment, id_game, rating, check):
        if sec.handle_check_ip_request(3, cherrypy.request.headers["Remote-Addr"]):
            raise cherrypy.HTTPError(403, "Forbidden")

        uname = cherrypy.session["uname"]
        comment = sec.swap_sp_char_for_token(comment)

        if check == "1":
            with sqlite3.connect(DB_STRING) as con:
                id_user = con.execute(f"SELECT id_user FROM User WHERE username='{uname}'").fetchall()[0][0]

                con.execute(
                    f"INSERT INTO Comment(comment, rating, id_user, id_game) VALUES('{comment}','{rating}','{id_user}','{id_game}')")
                con.commit()

                raise cherrypy.HTTPRedirect("/comments?id_game=" + str(id_game))
        else:
            raise cherrypy.HTTPRedirect("/comments?id_game=" + str(id_game) + "&preview=" + comment)

    @cherrypy.expose
    def deleteComment(self, commentid, key):
        if not ("key" in cherrypy.session.keys() and cherrypy.session["key"] == key):
            raise cherrypy.HTTPRedirect(403, "Forbidden")

        with sqlite3.connect(DB_STRING) as con:
            id_game = con.execute(f"SELECT id_game FROM Comment WHERE id_comment='{commentid}'").fetchall()[0][0]
            query = f"DELETE FROM Comment WHERE id_comment='{commentid}'"
            con.execute(query)
            con.commit()

            raise cherrypy.HTTPRedirect("/comments?id_game=" + str(id_game))

    @cherrypy.expose
    def modUser(self, key, unametomod, id_game):
        if not ("key" in cherrypy.session.keys() and cherrypy.session["key"] == key):
            raise cherrypy.HTTPRedirect(403, "Forbidden")

        with open("static/db/SuperUsers.txt") as admins:
            addAdmin = True
            for admin in admins:
                if admin == unametomod:
                    addAdmin = False
                    break
        if addAdmin:
            with open("static/db/SuperUsers.txt", "a") as admins:
                admins.write(f"{unametomod}\n")
        raise cherrypy.HTTPRedirect("/comments?id_game=" + str(id_game))


config = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': abspath(".")
    },
    '/static':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': "static"
         },
    '/img':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': "static/img"
         },
    '/htmlTemplates':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': "static/htmlTemplates"
         },
    '/css':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': "static/css"
         },
    '/db':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': "static/db"
         }
}
cherrypy.quickstart(App(), "/", config)
