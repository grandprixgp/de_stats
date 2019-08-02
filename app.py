import os, time, importlib, threading, json, subprocess, glob
from flask import Flask, escape, request

util = importlib.import_module("util")
app = Flask(__name__)

@app.route('/live')
def live():
    demo_files = util.find_extension("dem", hours = 2)
    return "<br>".join(demo_files)

@app.route('/recent')
def recent():
    demo_files = util.find_extension("dem", hours = 4)
    return "<br>".join(demo_files)

@app.route('/today')
def today():
    demo_files = util.find_extension("dem", days = 1)
    return "<br>".join(demo_files)

@app.route('/week')
def week():
    demo_files = util.find_extension("dem", weeks = 1)
    return "<br>".join(demo_files)

if __name__ == "__main__":
    app.run(debug=True)