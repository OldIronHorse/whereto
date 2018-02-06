from flask import Flask

app = Flask('whereto')

@app.route('/')
def hello_world():
  return 'Hello, World!'
