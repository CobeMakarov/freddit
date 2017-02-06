import os
from flask import Flask, render_template, session, request, url_for, redirect

from subfreddit import subfreddit
from database import database
from user import user
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

db = database()

client = ""

@app.route('/')
def renderFrontPage():

    db.connect()

    if session.get('authenticated'):
        userId = session['user_id']
        client = user(userId, db)

        print("[Site Log] user #" + str(userId) + " - " + client.username + " has connected to Freddit")

        if client.night:
            print("[Site Log] " + client.username + " has dark mode enabled, let's enable it sitewide.")

        return render_template('front_page.html', client=client, posts=client.buildFrontPage(), subfreddits=client.subfreddits)

    return render_template('authenticate.html')

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticateUser():

    error = False

    if request.method == "POST":
        type = request.form["type"]

        if type == "0":  #login

            if not request.form["email"] or not request.form["password"]:
                return '4'  #something is blank!

            email = request.form["email"]
            password = request.form["password"]

            db.getCursor().execute("SELECT id, password FROM users WHERE email = %s", (email, ))

            row = db.getCursor().fetchone()

            if db.getCursor().rowcount < 1:
                return '0'

            userId = row[0]
            correctPassword = row[1]

            if check_password_hash(correctPassword, password):
                session['user_id'] = userId
                session['authenticated'] = True

                client = user(userId, db)

                print("[Site Log] user #" + str(userId) + " - " + client.username + " has successfully authenticated.")
                return '1'  #user successfully logged in
            else:
                return '3'  #no account with those credentials found
        else:  #register
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password2 = request.form["password2"]
            night = request.form["night_mode"]

            if not request.form["username"] or not request.form["email"] or\
                    not request.form["password"] or not request.form["password2"]:
                return '4'  #something is blank!

            if '@' not in request.form['email'] or '.' not in request.form['email']:
                return '5'  #email not formatted correctly

            if password != password2:
                return '3'  #passwords do not match

            if not len(request.form["password"]) >= 6:
                return '6ix'

            if user.userExists(email, username, db):
                return '2'  #user already exists with that email or username

            session['user_id'] = user.create(email, generate_password_hash(password), username, night)
            session['authenticated'] = True
            return '1'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('renderFrontPage'))

@app.route('/fr')
def emptySubfreddit():
    return None

@app.route('/fr/<name>')
def renderSubFreddit(name=None):

    if name is None:
        return redirect(url_for('emptySubfreddit'))
    else:
        return name

@app.route('/settings', methods=['GET', 'POST'])
def renderSettings():
    return None

@app.route('/settings/create', methods=['GET', 'POST'])
def createSub():

    if not session.get('authenticated'):
        return redirect(url_for('renderFrontPage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["title"] or not request.form["path"] or not request.form["desc"]:
            return '0'

        title = request.form["title"]
        path = request.form["path"]
        desc = request.form["desc"]
        private = request.form["private"]

        if len(title) > 85:
            return '1'

        if len(path) > 30:
            return '2'

        sub_id = subfreddit.create(path, title, client.id, private, desc, db)

        client.subscribe(sub_id)
        client.moderate(sub_id)

        return redirect(url_for("renderSubFreddit", name=path))
    else:
        return render_template('front_page_create_subs.html', client=client, subfreddits=client.subfreddits)

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
