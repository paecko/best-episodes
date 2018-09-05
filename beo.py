import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from jinja2 import Environment
from helper import get_link, format_episode, get_episodes, get_tvshow

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'beo.db'),
    SECRET_KEY='auf9u&aod$f9(8fk(+ha7;aas7@',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('BEO_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_db(row):
    colname = [d[0] for d in row.description]
    result_list = [dict(zip(colname, r)) for r in row.fetchall()]
    return result_list


@app.cli.command('addshows')
def add_shows():
    with app.app_context():
        db = get_db()
        shows = get_tvshow(5)

        for show in shows:
            '''Cheeck doesnt work. Check later.

            rows = query_db('SELECT * FROM entries WHERE imdb_id = ?', show['imdb_id'])
            if len(rows) == 0:
            '''
            db.execute('INSERT INTO entries (title,imdb_id,rating) VALUES (?,?,?)',
                       (show['name'], show['imdb_id'], show['rating']))
        print("Shows added")
        db.commit()


@app.cli.command('addepisodes')
def add_episodes():
    with app.app_context():
        db = get_db()
        showrows = db.execute('SELECT * FROM entries')
        showdata = showrows.fetchall()
        if len(showdata) != 0:
            for show in showdata:
                episodes = get_episodes(show['imdb_id'])
                for episode in episodes:
                    db.execute('INSERT INTO episodes (id,episode,title,rating) VALUES(?,?,?,?)',
                               (show['id'], episode['episode'], episode['title'], episode['rating']))
            db.commit()
            print("Episodes added for each show")
        else:
            print("No shows loaded in database")


@app.cli.command('testadd')
def testadd():
    db = get_db()
    show = db.execute('SELECT * FROM entries WHERE imdb_id=?', ("tt0944947",))
    showdata = show.fetchall()
    show = showdata[0]
    episodes = get_episodes(show['imdb_id'])
    for episode in episodes:
        db.execute('INSERT INTO episodes (id,episode,title,rating) VALUES(?,?,?,?)',
                   (show['id'], episode['episode'], episode['title'], episode['rating']))
    db.commit()


app.jinja_env.filters['format_episode'] = format_episode


@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    rows = db.execute('SELECT * FROM entries')
    if request.method == 'POST':
        if request.form.get('searchsub'):
            rows = db.execute('SELECT * from entries WHERE LOWER(title) = ?', (request.form['searchin'].lower(),))
        if request.form.get('popular'):
            rows = db.execute('SELECT * from entries ORDER BY rating desc')
        if request.form.get('alpha'):
            rows = db.execute('SELECT * from entries ORDER BY title')
    q = query_db(rows)
    return render_template('layout.html', shows=q)


@app.route('/episodelist/<showid>')
def episodelist(showid):
    db = get_db()
    showrow = db.execute('SELECT id, title FROM entries WHERE imdb_id=?', (showid,))
    primarykey = showrow.fetchall()
    episodesrow = db.execute("SELECT * FROM episodes WHERE id = ?", (primarykey[0]['id'],))
    episodelist = query_db(episodesrow)
    showname = primarykey[0]['title']
    for episode in episodelist:
        episode['link'] = get_link(showname,episode['episode'])

    return render_template('episodelist.html', episodelist=episodelist)

# testing git username