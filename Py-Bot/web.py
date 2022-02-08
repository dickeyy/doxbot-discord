from flask import Flask 
from flask import render_template
from threading import Thread 
import codecs

app = Flask('')

@app.route('/')
def index():
  return render_template("index.html")

def run():
  app.run(host='0.0.0.0',port=8194)

def web_server():
  t = Thread(target=run)
  t.start()