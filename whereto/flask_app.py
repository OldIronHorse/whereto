from flask import Flask, g
import os
import sqlite3
import whereto

app = Flask('whereto')
app.config.from_object(__name__)
app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'whereto.db'),
  SECRET_KEY='development key',
))
app.config.from_envvar('WHERETO_SETTINGS', silent=True)

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def init_db():
  db = get_db()
  c = db.cursor()
  with app.open_resource('schema.sql', mode='r') as f:
    c.executescript(f.read())
  with app.open_resource('data/towns-france.csv', mode='r') as t:
    towns = whereto.load_towns(t)
    for town in towns:
      c.execute("insert into towns(commune, department, region) values(?,?,?)",
        (town['commune'], town['department'], town['region']))
  db.commit()

@app.cli.command('initdb')
def initdb_command():
  init_db()
  print('Initialised the database')
  db = get_db()
  for town in db.cursor().execute('select * from towns'):
    print(tuple(town))

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

@app.route('/')
def hello_world():
  return 'Hello, World!'
