import os, time, platform, importlib, threading, json, subprocess, glob
from functools import wraps
from flask import Flask, escape, request, jsonify
from werkzeug.exceptions import HTTPException, BadRequest

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

def validate_json(*keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            if not request.json:
                raise BadRequest
            else:
                if not all (key in request.get_json(cache = True) for key in keys):
                    raise BadRequest
                else:
                    return func(*args, **kw)
        return wrapper
    return decorator

@app.route('/matches', methods=['POST'])
@validate_json("hours", "days", "weeks")
def matches():
    return app.response_class(
        response=dump(util.find_extension("dem", hours = int(request.get_json()["hours"]), days = int(request.get_json()["days"]), weeks = int(request.get_json()["weeks"]))),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='112')