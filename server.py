import datetime
import uuid

import timeago
from flask import Flask, render_template, session, request, url_for, redirect
from flask_socketio import SocketIO, emit
from werkzeug import check_password_hash, generate_password_hash

from chat import chat
from comment import comment as cmt_obj
from database import database
from misc import misc
from moderator import moderator
from post import post as post_obj
from search import search as search_for
from subfreddit import subfreddit
from user import user

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
                               ago=timeago, date=datetime, page_title="Freddit: Front Page", misc=misc)

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

            db.get_cursor().execute("SELECT id, password FROM users WHERE email = %s", (email,))

            row = db.get_cursor().fetchone()

            if db.get_cursor().rowcount < 1:
                return '0'

            id = row[0]
            correct_password = row[1]

            if check_password_hash(correct_password, password):
                session['user_id'] = id
                session['authenticated'] = True

                client = user(id, db)

                print("[Site Log] user #" + str(id) + " - " + client.username + " has successfully authenticated.")
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

            if not username.isalnum():
                return '7'

            if len(username) >= 30:
                return '8'

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
    return "Subfreddit not found. <a href='/'>return home</a>"

@app.route('/p')
def empty_post():
    return "Post not found. <a href='/'>return home</a>"

@app.route('/fr/<name>')
def render_sub(name=None):
    if name is None:
        return redirect(url_for('empty_sub'))
    else:
        db.connect()

        if session.get('authenticated'):
            client = user(session['user_id'], db)

            name = name.lower()

            sub = next((x for x in client.subfreddits if x.path == name), None)

            if sub is None:
                sub = subfreddit(0, db, name)

            if sub.title is None or len(sub.title) == 0:
                return redirect(url_for('empty_sub'))

            return render_template('subfreddit.html',
                                   client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                                   sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title,
                                   is_owner=sub.is_owner(client.id), sticky=sub.get_sticky_post(), misc=misc)

@app.route('/fr/<name>/<sort>')
def render_sub_sort(name=None, sort=None):
    if name is None:
        return redirect(url_for('empty_sub'))
    else:
        db.connect()

        if session.get('authenticated'):
            userId = session['user_id']
            client = user(userId, db)

            name = name.lower()

            sub = next((x for x in client.subfreddits if x.path == name), None)

            if sub is None:
                sub = subfreddit(0, db, name)

            if sort is None:
                sort = "hot"

            if sub.title is None or len(sub.title) == 0:
                return redirect(url_for('empty_sub'))

            return render_template('subfreddit.html',
                                   client=client, posts=sub.get_posts(sort), subfreddits=client.subfreddits,
                                   sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title,
                                   is_owner=sub.is_owner(client.id), sticky=sub.get_sticky_post(), misc=misc)

@app.route('/fr/settings/<id>')
def render_sub_settings(id=None):
    if id is None:
        return None

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    sub = subfreddit(id, db)

    if sub is not None:
        return render_template('subfreddit_settings.html', client=client, subfreddits=client.subfreddits,
                               sub=sub, page_title='Subfreddit Settings for ' + sub.title,
                               is_owner=sub.is_owner(client.id), misc=misc)


@app.route('/fr/subscribe/<id>')
def subscribe(id=None):
    if id is None:
        return None

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    sub = subfreddit(id, db)

    if sub is not None:
        client.subscribe(id)

    return render_template('subfreddit.html',
                           client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                           sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title,
                           is_owner=sub.is_owner(client.id), sticky=sub.get_sticky_post(), misc=misc)

@app.route('/fr/unsubscribe/<id>')
def unsubscribe(id=None):
    if id is None:
        return None

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    sub = subfreddit(id, db)

    if sub is not None:
        client.unsubscribe(id)

    return render_template('subfreddit.html',
                           client=client, posts=sub.get_posts("hot"), subfreddits=client.subfreddits,
                           sub=sub, ago=timeago, date=datetime, is_mod=client.is_mod(sub.id), page_title=sub.title,
                           is_owner=sub.is_owner(client.id), sticky=sub.get_sticky_post(), misc=misc)

@app.route('/fr/save', methods=['POST'])
def subfreddit_save():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form['title']:
            return '0'

        title = request.form['title']
        desc = request.form['desc']
        header = request.form['header']
        header_text = request.form['header_text']

        sub_id = request.form["sub_id"]
        sub = subfreddit(sub_id, db)

        if (title != sub.title and len(title) > 3) or \
            desc != sub.desc or \
            header != sub.header_background or \
            header_text != sub.header_text:  #there's some sort of change so lets save

            sub.title = title

            if desc != sub.desc:
                sub.desc = desc

            if header != sub.header_background:
                if header_text != sub.header_text and len(header) >= 3 and header == header_text:
                    return '3'

                sub.header_background = header

            if header_text != sub.header_text:
                sub.header_text = header_text

            sub.save()
            return '1'
        return '2'

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
                                   date=datetime, is_mod=client.is_mod(sub.id), misc=misc, page_title=p.title,
                                   is_owner=sub.is_owner(client.id))

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
                                   date=datetime, is_mod=client.is_mod(sub.id), misc=misc, page_title=p.title,
                                   is_owner=sub.is_owner(client.id))

@app.route('/u/<name>')
def render_user(name=None):
    if name is None:
        return None

    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    profiled_id = user.get_id_by_username(name, db)

    if profiled_id == 0:
        return "user not found."

    profiled = user(profiled_id, db)

    return render_template('profile.html', client=client, subfreddits=client.subfreddits, page_title=profiled.username,
                           profile=profiled, ago=timeago, date=datetime)

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

        if len(path) > 30 or not path.isalpha():
            return '2'

        sub_id = subfreddit.create(path.lower(), title, client.id, private, desc, db)

        client.subscribe(sub_id)
        client.moderate(sub_id)

        ##return redirect(url_for("renderSubFreddit", name=path))
        return '3'
    else:
        return render_template('front_page_create_sub.html', client=client, subfreddits=client.subfreddits,
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

@app.route('/discover')
def discover_subfreddits():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    subs = subfreddit.discover(db)

    return render_template('discover.html', client=client, page_title="Freddit: Discover",
                           subfreddits=client.subfreddits, discovered_subfreddits=subs, sort="popular")

@app.route('/discover/<sort>')
def discover_subfreddits_sort(sort):
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    if sort is None:
        sort = "popular"

    if sort != "popular" and sort != "new":
        sort = "popular"

    db.connect()

    client = user(session['user_id'], db)

    subs = subfreddit.discover(db, sort)

    return render_template('discover.html', client=client, page_title="Freddit: Discover",
                           subfreddits=client.subfreddits, discovered_subfreddits=subs, sort=sort)

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

@app.route('/edit', methods=['POST'])
def edit():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        id = request.form["id"]
        text = request.form["text"]

        p = post_obj(id, db)

        if p.user_id == client.id or client.is_mod(p.subfreddit) or client.admin:
            if p.media_url is not None:
                return '0'

            if text == p.post_text:
                return '2'

            p.post_text = text

            p.update()
            return '-1'
        else:
            return '1'

@app.route('/comment', methods=['POST'])
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

        return str(post_id)

@app.route('/vote', methods=['POST'])
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

@app.route('/sticky', methods=['POST'])
def sticky():
    if not session.get('authenticated'):
        return '0'

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["id"]:
            return '0'  # something went wrong

        id = request.form["id"]

        p = post_obj(id, db)

        if not client.is_mod(p.subfreddit):
            return '1'  # user doesn't have permission

        p.sticky()

        return '2'

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('authenticated'):
        return '0'

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["id"]:
            return '0'  # something went wrong

        id = request.form["id"]

        p = post_obj(id, db)

        if not client.is_mod(p.subfreddit):
            return '1'  # user doesn't have permission

        p.delete()

        return '2'

@app.route('/unsticky', methods=['POST'])
def unsticky():
    if not session.get('authenticated'):
        return '0'

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        if not request.form["id"]:
            return '0'  # something went wrong

        id = request.form["id"]

        p = post_obj(id, db)

        if not client.is_mod(p.subfreddit):
            return '1'  # user doesn't have permission

        p.unsticky()

        return '2'

@app.route('/flush', methods=['POST'])
def flush():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST" and client.admin:
        client.flush()
    return 'flush'

# settings post actions

@app.route('/add_mod', methods=['POST'])
def add_mod():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        mods = request.form["mods"].replace(" ", "").split(',')
        sub_id = request.form["sub_id"]
        sub = subfreddit(sub_id, db)

        mod_html = ""

        if sub.is_owner(client.id):
            for mod in mods:
                obj = moderator(user.get_id_by_username(mod, db), mod, sub_id, db)

                sub.add_moderator(obj)

                mod_html += obj.html()

            return mod_html

@app.route('/remove_mod', methods=['POST'])
def remove_mod():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        mod = request.form["mod"]
        sub_id = request.form["sub_id"]

        sub = subfreddit(sub_id, db)

        if sub.is_owner(client.id):
            sub.remove_moderator(mod)
            return '1'

    return '0'

@app.route('/add_flair', methods=['POST'])
def add_flair():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        text = request.form["text"]
        label = request.form["label"]
        sub_id = request.form["sub_id"]

        sub = subfreddit(sub_id, db)

        if sub.is_owner(client.id):

            if len(text) <= 15:
                result = sub.add_flair(text, label)
            else:
                return '2'

            if not result:
                return '1'
            else:
                return result.html()

@app.route('/remove_flair', methods=['POST'])
def remove_flair():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        id = request.form["id"]
        sub_id = request.form["sub_id"]

        sub = subfreddit(sub_id, db)

        if sub.is_owner(client.id):
            sub.remove_flair(id)

            return '1'

    return '0'

@app.route('/set_flair', methods=['POST'])
def set_flair():
    if not session.get('authenticated'):
        return redirect(url_for('frontpage'))

    db.connect()

    client = user(session['user_id'], db)

    if request.method == "POST":
        id = request.form["id"]
        sub_id = request.form["sub_id"]

        client.set_flair(sub_id, id)
        return '1'
    return '0'

# socket actions

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

    query = query.lower()

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
