import time, threading, json, subprocess
from flask import Flask, escape, request

app = Flask(__name__)

'''
-mtime -7 (last 7 days)
-mtime -1 (last 24 hours)
-cmin -60 (last hour)
-cmin -300 (last 5 hours)

Linux: find *.dem -mtime -1 -type f -size +40M -print
Windows: powershell.exe Get-ChildItem -Path (Get-Item -Path \".\\\").FullName -Include *.dem -Recurse
'''

@app.route('/live')
def live():
    pass

@app.route('/recent')
def recent():
    pass

@app.route('/today')
def today():
    pass

@app.route('/week')
def week():
    pass

if __name__ == "__main__":
    app.run(debug=True)