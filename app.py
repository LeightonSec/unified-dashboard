import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)
_secret = os.getenv('SECRET_KEY')
if not _secret:
    raise RuntimeError("SECRET_KEY is not set — refusing to start")
app.config['SECRET_KEY'] = _secret

# Tool endpoints
TOOLS = {
    "ai_firewall": {
        "name": "AI Firewall",
        "url": "http://127.0.0.1:5000",
        "stats_endpoint": "/stats",
        "layer": "Analysis"
    },
    "incident_tracker": {
        "name": "Incident Tracker",
        "url": "http://127.0.0.1:5002",
        "stats_endpoint": "/api/stats",
        "layer": "Response"
    }
}

def _safe_int(value, default: int = 0) -> int:
    """Coerce a tool-reported stat to an int at the trust boundary.

    The dashboard only ever displays numeric counts. Source tools run on
    localhost but ingest attacker-controlled input (hostile PCAPs, ticket
    free-text), so their /stats output is data-untrusted even though the
    connection is local — localhost trust is not data trust. Coercing every
    stat to int here means no attacker-influenced string can reach the
    dashboard's innerHTML sink. This pairs with the client-side escaping in
    templates/index.html as defense in depth.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def check_tool_health(url: str) -> bool:
    try:
        response = requests.get(url, timeout=2)  # gate: ignore — intentional localhost-only health check, all URLs hardcoded to 127.0.0.1
        return response.status_code == 200
    except Exception:
        return False

def get_tool_stats(tool_key: str) -> dict:
    tool = TOOLS.get(tool_key)
    if not tool:
        return {}
    try:
        url = tool["url"] + tool["stats_endpoint"]
        response = requests.get(url, timeout=3)  # gate: ignore — intentional localhost-only stats fetch, all URLs hardcoded to 127.0.0.1
        if response.status_code == 200:
            raw = response.json()
            if isinstance(raw, dict):
                # Coerce every stat to int at the boundary — see _safe_int.
                # The source tool is localhost but its data is untrusted.
                return {key: _safe_int(val) for key, val in raw.items()}
    except Exception:
        pass
    return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard')
def dashboard_data():
    """Aggregate data from all tools"""
    data = {
        "tools": {},
        "alerts": [],
        "summary": {
            "total_detections": 0,
            "open_incidents": 0,
            "critical_incidents": 0,
            "escalated": 0,
            "tools_online": 0,
            "tools_total": len(TOOLS)
        }
    }

    for tool_key, tool_config in TOOLS.items():
        online = check_tool_health(tool_config["url"])
        stats = get_tool_stats(tool_key) if online else {}

        data["tools"][tool_key] = {
            "name": tool_config["name"],
            "layer": tool_config["layer"],
            "url": tool_config["url"],
            "online": online,
            "stats": stats
        }

        if online:
            data["summary"]["tools_online"] += 1

        # Extract key metrics
        if tool_key == "ai_firewall" and stats:
            total = stats.get("total", 0)
            high = stats.get("high", 0)
            data["summary"]["total_detections"] += total
            if high > 0:
                data["alerts"].append({
                    "tool": "AI Firewall",
                    "severity": "HIGH",
                    "message": f"{high} high risk jailbreak attempts detected",
                    "url": tool_config["url"]
                })

        if tool_key == "incident_tracker" and stats:
            open_tickets = stats.get("open", 0)
            critical = stats.get("critical", 0)
            escalated = stats.get("escalated", 0)
            data["summary"]["open_incidents"] = open_tickets
            data["summary"]["critical_incidents"] = critical
            data["summary"]["escalated"] = escalated

            if critical > 0:
                data["alerts"].append({
                    "tool": "Incident Tracker",
                    "severity": "CRITICAL",
                    "message": f"{critical} critical incidents require immediate attention",
                    "url": tool_config["url"]
                })
            if escalated > 0:
                data["alerts"].append({
                    "tool": "Incident Tracker",
                    "severity": "HIGH",
                    "message": f"{escalated} escalated incidents awaiting review",
                    "url": tool_config["url"]
                })

    # Sort alerts by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    data["alerts"].sort(key=lambda x: severity_order.get(x["severity"], 4))

    return jsonify(data)

@app.route('/api/health')
def health():
    """Quick health check of all tools"""
    health_data = {}
    for tool_key, tool_config in TOOLS.items():
        health_data[tool_key] = {
            "name": tool_config["name"],
            "online": check_tool_health(tool_config["url"])
        }
    return jsonify(health_data)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5003)
