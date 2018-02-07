from flask import Flask, g, render_template, request
import os
import urllib.request
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
    towns = whereto.town.load(t)
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

def get_unrouted(db, origin_id):
  return [dict(t) for t in db.execute(
      'select * from towns where id not in (select destination_id from routes where origin_id = ?)',
      (origin_id,)).fetchall()]

def insert_route(db, origin_id, destination):
  db.execute('insert into routes(origin_id, destination_id, duration, duration_text, distance, distance_text) values(?,?,?,?,?,?)', 
             (origin_id,
              destination['id'],
              destination['duration']['value'],
              destination['duration']['text'],
              destination['distance']['value'],
              destination['distance']['text']))

def get_town(db, id):
  return dict(db.execute('select * from towns where id = ?', 
                         (id,)).fetchone())

def get_routes(db, origin_id, max_duration):
  return [dict(route) for route 
          in db.execute('select * from routes join towns where origin_id = ? and towns.id = routes.destination_id and duration <= ?', 
                        (origin_id,max_duration)).fetchall()]

def populate_routes(db, origin_id):
  distances = whereto.DistanceMatrix(app.config['MAPS_API_KEY'])
  distances.origin = get_town(db, origin_id)
  unrouted_towns = get_unrouted(db, origin_id)
  while unrouted_towns:
    print('unrouted count:', len(unrouted_towns))
    distances.destinations = unrouted_towns[:25]
    unrouted_towns = unrouted_towns[25:]
    distances.apply_response(urllib.request.urlopen(distances.url()).read())
    for d in distances.destinations:
      insert_route(db, origin_id, d)
  db.commit()

@app.route('/towns')
def show_towns():
  origin_id = int(request.args.get('originid'))
  print('origin_id:', origin_id)
  max_duration = int(request.args.get('maxduration'))
  print('max_duration:', max_duration)
  db = get_db()
  populate_routes(db, origin_id)
  routes = get_routes(db, origin_id, max_duration)
  return render_template('show_towns.html', 
    towns=sorted(routes, key=lambda t: t['duration']))

@app.route('/')
def main_form():
  return render_template('main_form.html')
