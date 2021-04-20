from flask import Flask 
from threading import Thread 
import codecs

app = Flask('')

@app.route('/')
def home():
  return 'DoxBot is live! 🔴'

def run():
  app.run(host='0.0.0.0',port=8194)

def keep_alive():
  t = Thread(target=run)
  t.start()