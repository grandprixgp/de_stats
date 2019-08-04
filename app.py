import os, time, importlib, threading, json, subprocess, glob
from flask import Flask, escape, request

from ctypes import *

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

go_library = cdll.LoadLibrary("quickdemo/build/release/quickdemo-windows-4.0-amd64.dll")
go_library.Dump.argtypes = [GoString]
go_library.Dump.restype = c_char_p

util = importlib.import_module("util")
app = Flask(__name__)

def dump(demo_files):
    go_arg = GoString(" ".join(demo_files).encode(), sum(map(len, demo_files)) + 1)
    go_return = go_library.Dump(go_arg)
    return go_return.decode()

@app.route('/live')
def live():
    return app.response_class(
        response=json.dumps(dump(util.find_extension("dem", hours = 2))),
        status=200,
        mimetype='application/json'
    )

@app.route('/recent')
def recent():
    demo_files = dump(util.find_extension("dem", hours = 4))
    return "<br>".join(demo_files)

@app.route('/today')
def today():
    demo_files = dump(util.find_extension("dem", days = 1))
    return "<br>".join(demo_files)

@app.route('/week')
def week():
    return app.response_class(
        response=json.dumps(dump(util.find_extension("dem", weeks = 1))),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(debug=True)