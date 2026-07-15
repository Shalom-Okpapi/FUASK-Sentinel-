import requests
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

class SecurityAnalyzer:
    @staticmethod
    def check_ssl(url):
        """Check SSL certificate health"""
        try:
            hostname = urlparse(url).hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (expiry - datetime.utcnow()).days
                    return {
                        "valid": True,
                        "days_left": days_left,
                        "status": "good" if days_left > 30 else "warning"
                    }
        except Exception:
            return {"valid": False, "status": "critical"}

    @staticmethod
    def check_security_headers(headers):
        """Analyze important security headers"""
        missing = []
        for header in IMPORTANT_SECURITY_HEADERS:  # from settings
            if header.lower() not in [h.lower() for h in headers]:
                missing.append(header)
        return {
            "score": max(0, 100 - len(missing) * 20),
            "missing_headers": missing
        }

    @staticmethod
    def analyze_response(response, baseline_time=0):
        """Detect anomalies"""
        anomalies = []
        
        if response.status_code != 200:
            anomalies.append(f"HTTP {response.status_code}")
        
        # Response time anomaly
        if baseline_time > 0 and response.elapsed.total_seconds() > baseline_time * ANOMALY_RESPONSE_TIME_MULTIPLIER:
            anomalies.append(f"Slow response: {response.elapsed.total_seconds():.2f}s")
        
        return anomalies
