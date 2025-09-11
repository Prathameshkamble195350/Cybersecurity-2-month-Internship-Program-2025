from flask import Flask, render_template, request
import os
import sys
import time

app = Flask(__name__)

# Available demo templates
TEMPLATES = {
    "google": "google_login.html",
    "facebook": "facebook_login.html",
    "office365": "office365_login.html"
}

def print_banner():
    banner = r"""
\033[1;31m
   █████╗  ██████╗ ███████╗ ██████╗██╗██████╗ 
  ██╔══██╗██╔════╝ ██╔════╝██╔════╝██║██╔══██╗
  ███████║██║  ███╗█████╗  ██║     ██║██████╔╝
  ██╔══██║██║   ██║██╔══╝  ██║     ██║██╔═══╝ 
  ██║  ██║╚██████╔╝███████╗╚██████╗██║██║     
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝╚═╝     
        \033[0m
   \033[1;31m[ACCSI] FakeLogin Page Generator – Training Tool\033[0m
   \033[1;31m[1] Requires root for port binding below 1024\033[0m
   \033[1;31m[2] For EDUCATIONAL and awareness purposes only!\033[0m
"""
    print(banner)
    time.sleep(1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/<site>", methods=["GET", "POST"])
def fake_login(site):
    if site not in TEMPLATES:
        return "Template not found", 404

    if request.method == "POST":
        username = request.form.get("username")
        print(f"[SIMULATION] {site} login attempt with username: {username}")
        return render_template("training_message.html", site=site, user=username)

    return render_template(TEMPLATES[site])


if __name__ == "__main__":
    print_banner()
    app.run(host="0.0.0.0", port=5000, debug=True)
