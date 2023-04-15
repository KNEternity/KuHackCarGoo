from flask import Flask
import sqlite3 as sql
app=Flask(__name__)
@app.route('/')
def hello():
    return '''<html>
<head>
<link rel="stylesheet" href='/static/style.css' />
</head>
<body>
<p>Hello, World!</p>
</body>
</html>'''

if __name__ == "__main__":
    app.run()