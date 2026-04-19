# ⚡ LeightonSec SOC — Unified Dashboard

The final piece of the LeightonSec SOC Toolkit. A single pane of glass that brings together all five layers of the security operations toolkit into one unified view — giving analysts instant visibility across the entire operation without switching between tools.

---

## What It Does

A SOC analyst shouldn't have to open five different tools to understand the current security posture. This dashboard aggregates live data from every tool in the LeightonSec toolkit, surfaces active alerts at the top, and provides one-click access to any tool that needs attention.

---

## Features

- **Live alert banner** — critical and high severity alerts surface immediately at the top
- **Real time stats** — tools online, total detections, open incidents, critical and escalated counts
- **Tool health monitoring** — green/red indicator per tool, offline tools flagged immediately
- **Per-tool stats** — key metrics from each tool displayed at a glance
- **One-click tool access** — click any tool card to open it directly
- **SOC layer map** — visual representation of where each tool sits in the stack
- **Auto-refresh** — dashboard updates every 30 seconds automatically
- **Graceful degradation** — if a tool goes offline the dashboard keeps running

---

## SOC Toolkit — Full Stack

Ingestion  → Intel Pipeline      — automated threat intelligence
Detection  → Log Analyser        — web server log analysis
→ PCAP Analyser       — network packet threat detection
Analysis   → AI Firewall         — LLM jailbreak detection
Response   → Incident Tracker    — SOC ticketing and escalation
Visibility → Unified Dashboard   ← you are here

---

## Alert Priority

Alerts are ranked by severity and displayed at the top:

| Severity | Trigger |
|----------|---------|
| CRITICAL | Critical priority incidents in Incident Tracker |
| HIGH | High risk AI Firewall detections, escalated incidents |
| MEDIUM | Medium risk detections |

Clicking an alert opens the relevant tool directly.

---

## Setup

**Requirements:** Python 3.x, other LeightonSec tools running

```bash
# Clone the repo
git clone git@github.com:LeightonSec/unified-dashboard.git
cd unified-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set secret key
echo "SECRET_KEY=your-secret-key-here" > .env

# Run the dashboard
python3 app.py
```

Then open `http://127.0.0.1:5003` in your browser.

**For full functionality start all tools:**
- AI Firewall on port 5000
- Incident Tracker on port 5002

---

## Project Structure

unified-dashboard/
├── app.py              # Flask server, aggregation API, health checks
├── templates/
│   └── index.html      # Dashboard UI — alerts, stats, tool grid, layer map
├── requirements.txt
└── .env                # Secret key (never committed)

---

## Adding New Tools

To add a new tool to the dashboard, add an entry to the `TOOLS` dict in `app.py`:

```python
TOOLS = {
    "new_tool": {
        "name": "Tool Name",
        "url": "http://127.0.0.1:PORT",
        "stats_endpoint": "/api/stats",
        "layer": "Detection"
    }
}
```

Then add the stats rendering logic in `index.html`.

---

## Roadmap

- [ ] Add Intel Pipeline report status
- [ ] Add PCAP Analyser recent detections
- [ ] Add Log Analyser stats
- [ ] Historical charts — detections over time
- [ ] Dark/light mode toggle
- [ ] Mobile responsive layout
- [ ] Docker compose — start all tools with one command

---

## Author

**Leighton Wilson** —  SOC Analyst | LeightonSec
[LeightonSec GitHub](https://github.com/LeightonSec)

---

*The final layer of the LeightonSec SOC Toolkit. Built to give analysts one place to see everything.*