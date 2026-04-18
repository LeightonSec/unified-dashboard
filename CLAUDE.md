# CLAUDE.md — Unified Dashboard

## What This Is
A Flask web application that aggregates live data from all LeightonSec
SOC tools into a single unified view. Surfaces active alerts, tool health
status and key metrics without the analyst having to open multiple tools.
The final and Visibility layer of the LeightonSec SOC Toolkit.

## SOC Toolkit Position
- **Layer:** Visibility
- **Receives from:** AI Firewall (port 5000), Incident Tracker (port 5002)
- **Feeds into:** Nothing — this is the top of the stack
- **Gap it fills:** Single pane of glass, unified security posture view

## Architecture
- `app.py` — Flask server, TOOLS config, health checks, data aggregation
- `templates/index.html` — Dashboard UI, alert banner, stats, tool grid, layer map

## Current Status
✅ Complete and live — LeightonSec/unified-dashboard
✅ Live alert banner — CRITICAL and HIGH alerts surface at top
✅ Tool health monitoring — green/red per tool
✅ AI Firewall stats — total, high risk, medium
✅ Incident Tracker stats — open, critical, resolved
✅ SOC layer map visual
✅ Auto-refresh every 30 seconds
✅ Graceful degradation — works even when tools are offline
✅ One-click tool access from dashboard

## Tool Configuration
Defined in TOOLS dict in app.py:

```python
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
```

## Tool Ports Reference
- Intel Pipeline — no web interface currently
- AI Firewall — port 5000
- PCAP Analyser — port 5001
- Incident Tracker — port 5002
- Unified Dashboard — port 5003

## Next Steps
- [ ] Add PCAP Analyser stats integration (port 5001)
- [ ] Add Log Analyser stats integration
- [ ] Add Intel Pipeline last run status
- [ ] Historical detection charts
- [ ] Docker Compose — start entire toolkit with one command
- [ ] Mobile responsive layout

## Security Notes
- SECRET_KEY in .env — never committed
- Dashboard only makes GET requests to tools — read only
- All tool URLs hardcoded to 127.0.0.1 — localhost only
- 2-3 second timeouts on all tool requests
- Graceful degradation — no crashes if tools are offline

## Conventions
- All tool configs in TOOLS dict — never hardcode URLs elsewhere
- Health check always before stats fetch
- Alert severity order: CRITICAL → HIGH → MEDIUM → LOW
- Auto-refresh interval: 30 seconds
- Never write to other tools — dashboard is read only