#!/usr/bin/env python3
"""
Safe Phishing Simulation (Educational)
- Local-only demo. Do NOT use against real users without written authorization.
- Requires an instructor token in the URL to view pages.
- Logs submissions to a local file and prints to console for instructor review.
"""

from flask import Flask, render_template, request, abort, redirect, url_for
from pathlib import Path
import datetime
import os
import logging

# CONFIGURATION - change these for your lab environment
INSTRUCTOR_TOKEN = "INSTRUCTOR_SECRET_TOKEN"  # change to a strong secret for your lab
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "submissions.log"

# Set up local-only logging (do not send anywhere)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ]
)

app = Flask(__name__, template_folder="templates")


def authorized(token: str) -> bool:
    """Return True only if token matches the configured instructor token."""
    return bool(token and token == INSTRUCTOR_TOKEN)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/<site>", methods=["GET", "POST"])
def login(site):
    """
    Shows a simulated login page for a given 'site' (e.g., google, facebook).
    Requires ?token=INSTRUCTOR_SECRET_TOKEN to view.
    """
    token = request.args.get("token", "")
    if not authorized(token):
        # If unauthorized, show a safe blocked page
        return render_template("blocked.html"), 403

    if request.method == "POST":
        # Note: This is a DEMO. We intentionally DO NOT integrate any exfiltration capability.
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Log to local file + console with clear "SIMULATION" tag
        logging.info("[SIMULATION SUBMISSION] site=%s username=%s password=%s", site, username, password)

        # Build a safe record for instructor review (timestamp, site, username, note)
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "site": site,
            "username": username,
            # we store the password too here because this is a lab demo — instructor should
            # decide data retention; in real tests NEVER store real passwords.
            "password": password,
            "note": "SIMULATION_ONLY - REMOVE AFTER REVIEW"
        }

        # Append to local JSON-like line (simple, local)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{record}\n")

        # Show the training message page (safe)
        return render_template("training_message.html", site=site, user=username)

    # GET -> show the chosen site template
    template_name = f"{site}_login.html"
    if not os.path.exists(os.path.join(app.template_folder, template_name)):
        return "Template not found", 404

    return render_template(template_name, site=site)


@app.route("/admin/logs")
def view_logs():
    """Simple admin-only view of log file (requires token param)."""
    token = request.args.get("token", "")
    if not authorized(token):
        abort(403)

    # Read last N lines from the log file (simple implementation)
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()[-200:]  # last 200 submissions
    except FileNotFoundError:
        lines = ["[no submissions yet]\n"]

    return render_template("admin_logs.html", lines=lines)


if __name__ == "__main__":
    print("SAFE PHISHING SIMULATION (EDUCATIONAL) - STARTING")
    print("Make sure you run this only in a closed lab. Instructor token must be kept secret.")
    app.run(host="127.0.0.1", port=5000, debug=False)
