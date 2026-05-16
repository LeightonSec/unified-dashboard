import pytest
from unittest.mock import patch, MagicMock

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c


def _mock_get(status=200, json_data=None, raise_exc=None):
    if raise_exc:
        m = MagicMock(side_effect=raise_exc)
        return m
    mock = MagicMock()
    mock.status_code = status
    mock.json.return_value = json_data or {}
    return mock


class TestIndex:
    def test_index(self, client):
        assert client.get('/').status_code == 200


class TestHealth:
    @patch('app.requests.get')
    def test_all_online(self, mock_get, client):
        mock_get.return_value = _mock_get(status=200)
        data = client.get('/api/health').get_json()
        assert all(t['online'] for t in data.values())

    @patch('app.requests.get')
    def test_all_offline(self, mock_get, client):
        mock_get.side_effect = Exception('refused')
        data = client.get('/api/health').get_json()
        assert all(not t['online'] for t in data.values())

    @patch('app.requests.get')
    def test_returns_tool_names(self, mock_get, client):
        mock_get.return_value = _mock_get(status=200)
        data = client.get('/api/health').get_json()
        assert 'ai_firewall' in data
        assert 'incident_tracker' in data
        assert 'name' in data['ai_firewall']


class TestDashboard:
    @patch('app.requests.get')
    def test_tools_offline(self, mock_get, client):
        mock_get.side_effect = Exception('refused')
        data = client.get('/api/dashboard').get_json()
        assert data['summary']['tools_online'] == 0
        assert data['summary']['tools_total'] == 2
        assert data['alerts'] == []

    @patch('app.requests.get')
    def test_tools_online_counted(self, mock_get, client):
        mock_get.return_value = _mock_get(status=200, json_data={})
        data = client.get('/api/dashboard').get_json()
        assert data['summary']['tools_online'] == 2

    @patch('app.requests.get')
    def test_ai_firewall_high_generates_alert(self, mock_get, client):
        def side_effect(url, **kwargs):
            if '5000' in url:
                return _mock_get(status=200, json_data={'total': 50, 'high': 5})
            return _mock_get(status=200, json_data={})
        mock_get.side_effect = side_effect

        data = client.get('/api/dashboard').get_json()
        alert_tools = [a['tool'] for a in data['alerts']]
        assert 'AI Firewall' in alert_tools

    @patch('app.requests.get')
    def test_incident_tracker_critical_generates_alert(self, mock_get, client):
        def side_effect(url, **kwargs):
            if '5002' in url:
                return _mock_get(status=200,
                                 json_data={'open': 3, 'critical': 2, 'escalated': 0})
            return _mock_get(status=200, json_data={})
        mock_get.side_effect = side_effect

        data = client.get('/api/dashboard').get_json()
        severities = [a['severity'] for a in data['alerts']]
        assert 'CRITICAL' in severities

    @patch('app.requests.get')
    def test_incident_tracker_stats_propagate(self, mock_get, client):
        def side_effect(url, **kwargs):
            if '5002' in url:
                return _mock_get(status=200,
                                 json_data={'open': 4, 'critical': 1, 'escalated': 2})
            return _mock_get(status=200, json_data={})
        mock_get.side_effect = side_effect

        summary = client.get('/api/dashboard').get_json()['summary']
        assert summary['open_incidents'] == 4
        assert summary['critical_incidents'] == 1
        assert summary['escalated'] == 2

    @patch('app.requests.get')
    def test_alerts_sorted_critical_first(self, mock_get, client):
        def side_effect(url, **kwargs):
            if '5000' in url:
                return _mock_get(status=200, json_data={'total': 10, 'high': 3})
            return _mock_get(status=200,
                             json_data={'open': 1, 'critical': 1, 'escalated': 1})
        mock_get.side_effect = side_effect

        alerts = client.get('/api/dashboard').get_json()['alerts']
        severities = [a['severity'] for a in alerts]
        assert severities == sorted(
            severities,
            key=lambda s: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}.get(s, 4)
        )

    @patch('app.requests.get')
    def test_no_alerts_when_no_issues(self, mock_get, client):
        def side_effect(url, **kwargs):
            if '5000' in url:
                return _mock_get(status=200, json_data={'total': 10, 'high': 0})
            return _mock_get(status=200,
                             json_data={'open': 1, 'critical': 0, 'escalated': 0})
        mock_get.side_effect = side_effect

        data = client.get('/api/dashboard').get_json()
        assert data['alerts'] == []

    @patch('app.requests.get')
    def test_dashboard_structure(self, mock_get, client):
        mock_get.side_effect = Exception('offline')
        data = client.get('/api/dashboard').get_json()
        assert 'tools' in data
        assert 'alerts' in data
        assert 'summary' in data
        for key in ('total_detections', 'open_incidents', 'critical_incidents',
                    'escalated', 'tools_online', 'tools_total'):
            assert key in data['summary']
