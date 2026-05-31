"""Send cost alerts via AWS SES or SMTP."""
from __future__ import annotations
import smtplib
from email.mime.text import MIMEText


class EmailNotifier:
    def __init__(self, smtp_host: str = "", smtp_port: int = 587,
                 username: str = "", password: str = ""):
        self.host     = smtp_host
        self.port     = smtp_port
        self.username = username
        self.password = password

    def send(self, to: str, subject: str, body: str) -> bool:
        msg            = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"]    = self.username
        msg["To"]      = to
        try:
            with smtplib.SMTP(self.host, self.port) as s:
                s.starttls()
                s.login(self.username, self.password)
                s.sendmail(self.username, to, msg.as_string())
            return True
        except Exception as exc:
            print(f"Email send failed: {exc}")
            return False
