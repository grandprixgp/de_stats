import os, time, platform, importlib, threading, json, subprocess, glob
from flask import Flask, escape, request, jsonify

from ctypes import *

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

go_library = cdll.LoadLibrary("quickdemo/build/quickdemo-windows.dll" if platform.uname()[0] == "Windows" else "quickdemo/build/quickdemo-linux-amd64.so")
go_library.Dump.argtypes = [GoString]
go_library.Dump.restype = c_char_p

util = importlib.import_module("util")
app = Flask(__name__)

def dump(demo_files):
    go_arg = GoString(" ".join(demo_files).encode(), sum(map(len, demo_files)) + 1)
    go_return = go_library.Dump(go_arg)
    return go_return.decode()

@app.route('/matches/', methods=['POST'])
def matches():
    return app.response_class(
        response=dump(util.find_extension("dem", hours = request.get_json(cache = True)["hours"], days = request.get_json(cache = True)["days"], weeks = request.get_json(cache = True)["weeks"])),
        status=200,
        mimetype='application/json'
    )
    #return app.response_class(
    #    response=dump(util.find_extension("dem", hours = 2)),
    #    status=200,
    #    mimetype='application/json'
    #)

@app.route('/recent')
def recent():
    return app.response_class(
        response=dump(util.find_extension("dem", hours = 4)),
        status=200,
        mimetype='application/json'
    )

@app.route('/today')
def today():
    return app.response_class(
        response=dump(util.find_extension("dem", days = 1)),
        status=200,
        mimetype='application/json'
    )

@app.route('/week')
def week():
    return app.response_class(
        response=dump(util.find_extension("dem", weeks = 1)),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='112')