"""Machine-readable JSON cost report."""
from __future__ import annotations
import json
from datetime import datetime
from typing import Dict


class JSONReporter:
    def generate(self, summary: Dict, output_path: str) -> str:
        payload = {"generated_at": datetime.utcnow().isoformat(), **summary}
        with open(output_path, "w") as fh:
            json.dump(payload, fh, indent=2)
        return output_path
