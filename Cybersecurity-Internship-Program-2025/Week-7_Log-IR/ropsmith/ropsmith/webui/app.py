from flask import Flask, render_template_string
import networkx as nx

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>ROP Smith Web UI (Coming Soon)</h1>"
