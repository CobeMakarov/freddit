import os
import uuid
import timeago, datetime

from flask_socketio import SocketIO, emit
from werkzeug import check_password_hash, generate_password_hash
from flask import Flask, render_template, session, request, url_for, redirect

from user import user
from misc import misc
from chat import chat
from search import search as search_for
from database import database
from subfreddit import subfreddit

from post import post as post_obj
from comment import comment as cmt_obj

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

socketio = SocketIO(app)

socket_users = {}
socket_messages = []
socket_new_messages = []

db = database()  # create a database object

chat_manager = ""

client = ""

@app.route('/')
def frontpage():
    db.connect()

    if session.get('authenticated'):
        userId = session['user_id']
        client = user(userId, db)

        print("[Site Log] user #" + str(userId) + " - " + client.username + " has connected to Freddit")

        if client.night:
            print("[Site Log] " + client.username + " has dark mode enabled, let's enable it sitewide.")

        return render_template('front_page.html', client=client, posts=client.build_frontpage(), subfreddits=client.subfreddits,
                               ago=timeago, date=datetime, page_title="Freddit: Front Page")

    return render_template('authenticate.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    db.connect()

    error = False

    if request.method == "POST":
        type = request.form["type"]

        if type == "0":  # login

            if not request.form["email"] or not request.form["password"]:
                return '4'  # something is blank!

            email = request.form["email"]
            password = request.form["password"]

            db.getCursor().execute("SELECT id, password FROM users WHERE email = %s", (email,))

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
                return '1'  # user successfully logged in
            else:
                return '3'  # no account with those credentials found
        else:  # register
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password2 = request.form["password2"]
            night = request.form["night_mode"]

            if not request.form["username"] or not request.form["email"] or \
                    not request.form["password"] or not request.form["password2"]:
                return '4'  # something is blank!

            if '@' not in request.form['email'] or '.' not in request.form['email']:
                return '5'  # email not formatted correctly

            if password != password2:
                return '3'  # passwords do not match

            if not len(request.form["password"]) >= 6:
                return '6ix'

            if user.exists(email, username, db):
                return '2'  # user already exists with that email or username

            session['user_id'] = user.create(email, generate_password_hash(password), username, night, db)
            session['authenticated'] = True
            return '1'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('frontpage'))


@app.route('/fr')
def empty_sub():
    return "Subfreddit not found."

@app.route('/p')
def empty_post():
    return "Post not found."

@app.route('/fr/<name>')
def render_sub(name=None):
    if name is None:
        return redirect(url_for('empty_sub'))
    else:
        db.connect()

        if session.get('authenticated'):
            userId = session['user_id']
            client = user(userId, db)

            sub = misc.get_obj_key("path", name, client.subfreddits)

            if sub is None:
                sub = subfreddit(0, db, name)

            if sub is None:
                return redirect(url_for('empty_sub'))

            return render_template('subfreddit.html',
                                   client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                                   sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title)

@app.route('/fr/<name>/<sort>')
def render_sub_sort(name=None, sort=None):
    if name is None:
        return redirect(url_for('empty_sub'))
    else:
        db.connect()

        if session.get('authenticated'):
            userId = session['user_id']
            client = user(userId, db)

            sub = misc.get_obj_key("path", name, client.subfreddits)

            if sub is None:
                sub = subfreddit(0, db, name)

            if sort is None:
                sort = "hot"

            return render_template('subfreddit.html',
                                   client=client, posts=sub.get_posts(sort), subfreddits=client.subfreddits,
                                   sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title)

@app.route('/fr/subscribe/<id>')
def subscribe(id=None):
    if id is None:
        return None;

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    sub = subfreddit(id, db)

    if sub is not None:
        client.subscribe(id)

    return render_template('subfreddit.html',
                           client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                           sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id))

@app.route('/fr/unsubscribe/<id>')
def unsubscribe(id=None):
    if id is None:
        return None;

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    sub = subfreddit(id, db)

    if sub is not None:
        client.unsubscribe(id)

    return render_template('subfreddit.html',
                           client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                           sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title="Freddit: Front Page")

@app.route('/p/<id>')
def render_post(id=None):
    if id is None:
        return redirect(url_for('empty_post'))
    else:
        db.connect()

        if session.get('authenticated'):
            userId = session['user_id']
            client = user(userId, db)

            p = post_obj(id, db)

            sub = subfreddit(p.subfreddit, db)

            return render_template('subfreddit_post.html',
                                   client=client, post=p, subfreddits=client.subfreddits, sub=sub, ago=timeago,
                                   date=datetime, is_mod=client.is_mod(sub.id), misc=misc, page_title=p.title)

@app.route('/p/<id>/<sort>')
def render_post_sort(id=None, sort=None):
    if id is None:
        return redirect(url_for('empty_post'))
    else:
        db.connect()

        if session.get('authenticated'):
            userId = session['user_id']
            client = user(userId, db)

            p = post_obj(id, db)

            if sort == "top":
                p.load_comments("top")

            if sort == "new":
                p.load_comments("new")

            sub = subfreddit(p.subfreddit, db)

            return render_template('subfreddit_post.html',
                                   client=client, post=p, subfreddits=client.subfreddits, sub=sub, ago=timeago,
                                   date=datetime, is_mod=client.is_mod(sub.id), misc=misc, page_title=p.title)

@app.route('/u/<name>')
def render_user(name=None):
    if name is None:
        return None

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return None


@app.route('/settings/create', methods=['GET', 'POST'])
def create_sub():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

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

        ##return redirect(url_for("renderSubFreddit", name=path))
        return '3'
    else:
        return render_template('front_page_create_subs.html', client=client, subfreddits=client.subfreddits,
                               page_title="Freddit: Create Subfreddit")

@app.route('/search', methods=['GET', 'POST'])
def search():
    return None

@app.route('/chat', methods=['GET', 'POST'])
def render_chat():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    return render_template('chat.html', client=client, page_title="Freddit: Chatbox")

# post actions (posting a thread, commenting on a thread, voting on a thread or comment)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":

        if not request.form['sub'] or not request.form["title"] or not request.form["type"]:
            return "-1"

        sub_id = request.form["sub"]

        sub = subfreddit(sub_id, db)

        type = int(request.form["type"])

        title = request.form["title"]

        if not request.form["text"]:
            text = ""
        else:
            text = request.form["text"]

        if not request.form["media"]:
            media = ""
        else:
            media = request.form["media"]

        return str(client.post(sub_id, title, type, text, media))
    else:
        sub_id = request.args.get("sub")
        sub = subfreddit(sub_id, db)

        if sub.path is None:  # sub not exists
            return "subfreddit not found."

        return render_template('subfreddit_create_post.html', client=client, subfreddits=client.subfreddits, sub=sub,
                               page_title="Freddit: Create Post")
        #client.post(sub, "This is my first post!", 0, "This is the post content of my first post!")

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["id"] or not request.form["parent"] or not request.form["text"]:
            return "-1"

        post_id = request.form["id"]
        parent = request.form["parent"]
        text = request.form["text"]

        client.comment(post_id, parent, text)

        print post_id

        return str(post_id)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["id"] or not request.form["is_post"] or not request.form["vote"]:
            return '0'

        id = request.form["id"]
        is_post = (request.form["is_post"] == "true")
        vote = request.form["vote"]

        has_voted = client.has_voted(id, is_post)

        if has_voted == int(vote):  # already voted
            return '-1'

        if has_voted == -1:  # has not voted yet
            client.vote(id, vote, is_post)

            if is_post:
                post_obj.update_vote(id, vote, db)
            else:
                cmt_obj.update_vote(id, vote, db)
        else:
            client.update_vote(id, vote, is_post)

            if is_post:
                post_obj.update_vote(id, vote, db, True)
            else:
                cmt_obj.update_vote(id, vote, db, True)

        return '1'

@socketio.on('connect')
def socket_connect():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if not session.get('uuid'):
        session['uuid'] = uuid.uuid1()
        session['socket_information'] = {'id': client.id, 'name': client.username, 'uuid': str(session['uuid']), 'is_admin': client.admin}
        socket_users[session['uuid']] = session['socket_information']

    chat_manager = chat(db)

    socket_messages = chat_manager.get_latest_messages()

    #msg = {'text': client.username + " has joined the chat..", 'user': session['socket_information']}

    #emit('message', msg, broadcast=True)
    emit('restore', socket_messages)
    emit('join', session['socket_information'])

@socketio.on('disconnect')
def socket_disconnect():
    return None

@socketio.on('message')
def socket_message(message):
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if not session.get('uuid'):
        session['uuid'] = uuid.uuid1()
        session['socket_information'] = {'id': client.id, 'name': client.username, 'uuid': str(session['uuid']), 'is_admin': client.admin}
        socket_users[session['uuid']] = session['socket_information']

    msg = {'text': message, 'user': session['socket_information']}

    socket_messages.append(msg)
    socket_new_messages.append(msg)
    emit('message', msg, broadcast=True)

@socketio.on('try_bulk_save')
def try_bulk_save():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    chat_manager = chat(db)

    if chat_manager.bulk_save(socket_new_messages):
        del socket_new_messages[:]

@socketio.on('try_search')
def try_search(query, param):
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    results = ""

    print query

    if param == "users":
        results = search_for.users(query, db)
    elif param == "subfreddits":
        results = search_for.subfreddits(query, db)
    elif param == "posts":
        results = search_for.posts(query, db)

    emit('refresh_results', results)

@socketio.on('try_subfreddit_search')
def try_search_subfreddit(query, sub):
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    results = search_for.posts_in_sub(query, sub, db)

    emit('refresh_results', results)

# start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
