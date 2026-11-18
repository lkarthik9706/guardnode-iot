import urllib.request
import json
import time

base = 'http://127.0.0.1:8000'

def get(path):
    res = urllib.request.urlopen(base + path)
    return res.status, json.loads(res.read().decode())

def post(path, body):
    req = urllib.request.Request(
        base + path,
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    res = urllib.request.urlopen(req)
    return res.status, json.loads(res.read().decode())

def main():
    print('=== 1. VERIFY ENDPOINTS IN INITIAL STATE ===')
    for ep in ['/api/health', '/api/status', '/api/devices', '/api/alerts', '/api/traffic']:
        status, data = get(ep)
        print(f'{ep}: status={status}, type={type(data).__name__}')

    print('\n=== 2. TEST MODE SWITCH TO LIVE AND BACK TO DEMO ===')
    s_live, d_live = post('/api/mode', {'mode': 'LIVE', 'interface': 'default'})
    print(f"Switch to LIVE: status={s_live}, mode={d_live.get('mode')}, is_monitoring={d_live.get('is_monitoring')}")

    time.sleep(1)
    s_demo, d_demo = post('/api/mode', {'mode': 'DEMO', 'interface': 'default'})
    print(f"Switch to DEMO: status={s_demo}, mode={d_demo.get('mode')}, is_monitoring={d_demo.get('is_monitoring')}")

    print('\n=== 3. WAIT FOR DEMO ENGINE EVENTS AND CHECK TELEMETRY ===')
    time.sleep(4)
    s_status, d_status = get('/api/status')
    print(f"Status: monitoring={d_status.get('monitoring')}, packets_analyzed={d_status.get('packets_analyzed')}, devices={d_status.get('devices_detected')}")

    s_devs, devs = get('/api/devices')
    print(f"Devices ({len(devs)} tracked):")
    for d in devs[:4]:
        print(f"  IP: {d['ip']}, Name: {d['name']}, Rate: {d['packet_rate']}, Mean: {d['mean_packet_rate']}, Median: {d['median_packet_rate']}, Max: {d['maximum_packet_rate']}, Status: {d['status']}, Packets: {d['packet_count']}")

    s_alerts, alerts = get('/api/alerts')
    print(f"Alerts: status={s_alerts}, count={len(alerts)}")

    s_traffic, traffic = get('/api/traffic')
    print(f"Traffic: status={s_traffic}, history_length={len(traffic.get('traffic_history', []))}")

    print('\n=== ALL VERIFICATIONS COMPLETED SUCCESSFULLY ===')

if __name__ == '__main__':
    main()
