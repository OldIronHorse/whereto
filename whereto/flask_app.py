from flask import Flask, g, render_template, request
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

@app.route('/towns')
def show_towns():
  origin = request.args.get('origin')
  print('origin:', origin)
  max_duration = request.args.get('maxduration')
  print('max_duration:', max_duration)
  db = get_db()
  #TODO: get origin as dict
  origin_town = whereto.town.from_row(db.execute(
      'select commune, department, region from towns where commune = ?', 
      (origin,)).fetchone())
  cur = db.execute('select commune, department, region from towns order by commune')
  destinations = [whereto.town.from_row(town) for town in  cur.fetchall()]
  print('destinations:', destinations)
  #TODO: get desinations as list of dicts
  #TODO: hit maps api for travel times
  #TODO: filters and sort
  return render_template('show_towns.html', towns=destinations)

@app.route('/')
def main_form():
  return render_template('main_form.html')
