# LeightonSec SOC — Unified Dashboard

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

The visibility layer of the LeightonSec SOC Toolkit. A single pane of glass that aggregates live data from all SOC tools, surfaces active alerts, and gives analysts instant posture awareness without switching between tools.

---

## Ethical Use

This dashboard is built for legitimate security operations teams monitoring infrastructure they own and operate. It makes read-only requests to local SOC tools. Do not expose it on the public internet without authentication.

---

## Why This Matters

A SOC analyst shouldn't have to open five different tools to understand the current security posture. When alerts are firing, time spent switching tabs costs detection time. This dashboard aggregates live data from every tool in the toolkit, surfaces critical alerts at the top, and provides one-click access to any tool that needs attention — all auto-refreshing every 30 seconds.

---

## Features

- **Live alert banner** — CRITICAL and HIGH alerts surface immediately at the top
- **Real-time stats** — tools online, total detections, open incidents, critical and escalated counts
- **Tool health monitoring** — green/red indicator per tool, offline tools flagged immediately
- **Per-tool stats** — key metrics from each tool displayed at a glance
- **One-click tool access** — click any tool card to open it directly
- **SOC layer map** — visual representation of where each tool sits in the stack
- **Auto-refresh** — dashboard updates every 30 seconds automatically
- **Graceful degradation** — if a tool goes offline the dashboard keeps running

---

## Setup

```bash
git clone git@github.com:LeightonSec/unified-dashboard.git
cd unified-dashboard
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "SECRET_KEY=your-secret-key-here" > .env
python3 app.py
```

Open `http://127.0.0.1:5003`. For full functionality, start the AI Firewall (port 5000) and Incident Tracker (port 5002) first.

---

## SOC Toolkit — Full Stack

```
Ingestion  → Intel Pipeline      — automated threat intelligence
Detection  → Log Analyser        — web server log analysis
           → PCAP Analyser       — network packet threat detection
Analysis   → AI Firewall         — LLM jailbreak detection
Response   → Incident Tracker    — SOC ticketing and escalation
Visibility → Unified Dashboard   ← you are here
```

---

## Alert Severity

| Severity | Trigger |
|----------|---------|
| CRITICAL | Critical priority incidents in Incident Tracker |
| HIGH | High risk AI Firewall detections or escalated incidents |
| MEDIUM | Medium risk detections |

---

## Adding a New Tool

Add an entry to the `TOOLS` dict in `app.py`, then add stats rendering logic to `index.html`:

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

---

## Scope

- Read-only — makes only GET requests to other tools, never writes
- Localhost only — all tool URLs hardcoded to 127.0.0.1; not designed for distributed deployment
- Designed to run alongside the rest of the LeightonSec SOC Toolkit

---

## Limitations

- No historical data — current snapshot only, no time-series charts
- No authentication — deploy behind a VPN or firewall
- Tool URLs and ports are hardcoded in `app.py` — requires a code change to relocate tools

---

## Licence

MIT © Leighton Wilson / LeightonSec
