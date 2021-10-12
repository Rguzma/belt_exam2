from flask import Flask               #Created for modularized

app= Flask(__name__)
app.secret_key = "something"