"""PDF report wrapper — converts the HTML report to PDF via weasyprint."""
from __future__ import annotations
from .html_reporter import HTMLReporter
from typing import Dict


class PDFReporter:
    """
    Requires: pip install weasyprint
    On Debian/Ubuntu: apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
    """
    def generate(self, summary: Dict, output_path: str) -> str:
        try:
            import weasyprint
        except ImportError:
            raise RuntimeError("weasyprint not installed — run: pip install weasyprint")

        html_path = output_path.replace(".pdf", "_tmp.html")
        HTMLReporter().generate(summary, html_path)
        weasyprint.HTML(filename=html_path).write_pdf(output_path)
        import os
        os.remove(html_path)
        return output_path
