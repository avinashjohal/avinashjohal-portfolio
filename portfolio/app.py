import os
import json
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])

SERVICES = [
    {
        "title": "Web Application Security Testing",
        "description": "OWASP-based assessments, vulnerability reporting, remediation guidance.",
        "price": "Starting $299",
    },
    {
        "title": "Network Penetration Testing",
        "description": "Internal/external testing, exploitation analysis, risk prioritization.",
        "price": "Starting $399",
    },
    {
        "title": "Digital Forensics",
        "description": "Evidence collection, timeline analysis, reporting for incidents.",
        "price": "Custom",
    },
    {
        "title": "Threat Hunting & SIEM",
        "description": "Use cases, detections, correlation rules, dashboards.",
        "price": "Starting $249",
    },
]

PROJECTS = [
    {
        "title": "Network Intrusion Detection",
        "description": "Packet capture with Scapy, feature extraction, anomaly detection.",
        "tags": ["Python", "Scapy", "IDS"],
        "repo": "https://github.com/example/ids",
        "live": "",
        "image": "images/placeholder.svg",
    },
    {
        "title": "Malware Static Analyzer",
        "description": "PE parsing, YARA scanning, IOC extraction pipeline.",
        "tags": ["Python", "YARA", "Forensics"],
        "repo": "https://github.com/example/malware-analyzer",
        "live": "",
        "image": "images/placeholder.svg",
    },
    {
        "title": "Log Forensics Pipeline",
        "description": "Ingest, normalize, and investigate logs with ELK.",
        "tags": ["ELK", "Python", "SIEM"],
        "repo": "https://github.com/example/log-forensics",
        "live": "",
        "image": "images/placeholder.svg",
    },
    {
        "title": "OSINT Toolkit",
        "description": "Data collection from public sources, enrichment, simple reporting.",
        "tags": ["Python", "OSINT", "CLI"],
        "repo": "https://github.com/example/osint-toolkit",
        "live": "",
        "image": "images/placeholder.svg",
    },
    {
        "title": "Web App Pentest Reports",
        "description": "Templates and examples of findings with remediation.",
        "tags": ["OWASP", "Reporting", "Docs"],
        "repo": "https://github.com/example/pentest-reports",
        "live": "",
        "image": "images/placeholder.svg",
    },
    {
        "title": "SIEM Detection Rules",
        "description": "Correlation rules and dashboards for common TTPs.",
        "tags": ["SIEM", "Detection", "MITRE ATT&CK"],
        "repo": "https://github.com/example/siem-rules",
        "live": "",
        "image": "images/placeholder.svg",
    },
]

def send_email(name: str, email: str, message: str) -> bool:
    recipient = os.environ.get("MAIL_RECIPIENT", "")
    server = os.environ.get("MAIL_SERVER", "")
    username = os.environ.get("MAIL_USERNAME", "")
    password = os.environ.get("MAIL_PASSWORD", "")
    port = int(os.environ.get("MAIL_PORT", "587"))
    use_tls = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    sender = os.environ.get("MAIL_DEFAULT_SENDER", username or email)
    if not recipient or not server:
        return False
    body = f"From: {name}\nEmail: {email}\n\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = "Portfolio Contact"
    msg["From"] = sender
    msg["To"] = recipient
    try:
        smtp = smtplib.SMTP(server, port, timeout=10)
        if use_tls:
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.sendmail(sender, [recipient], msg.as_string())
        smtp.quit()
        return True
    except Exception:
        return False

def persist_submission(name: str, email: str, message: str) -> None:
    path = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(path, exist_ok=True)
    fpath = os.path.join(path, "contact_submissions.json")
    try:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except Exception:
        data = []
    data.append({"name": name, "email": email, "message": message})
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    skills = [
        {"name": "Web Security", "level": 85},
        {"name": "Network Security", "level": 80},
        {"name": "Digital Forensics", "level": 75},
        {"name": "Python", "level": 88},
        {"name": "SIEM", "level": 78},
    ]
    return render_template("about.html", skills=skills)

@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        ok = send_email(form.name.data.strip(), form.email.data.strip(), form.message.data.strip())
        if ok:
            flash("Message sent successfully.", "success")
        else:
            persist_submission(form.name.data.strip(), form.email.data.strip(), form.message.data.strip())
            flash("Message saved locally.", "info")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)

