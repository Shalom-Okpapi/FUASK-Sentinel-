import requests

class SensitiveScanner:
    @staticmethod
    def scan_common_vulnerable_paths(base_url):
        """Scan for common sensitive files exposed by misconfiguration"""
        paths = [
            "/.env", "/admin", "/wp-admin", "/administrator", 
            "/backup", "/config", "/db.sql", "/phpmyadmin"
        ]
        findings = []
        
        for path in paths:
            try:
                url = base_url.rstrip("/") + path
                r = requests.get(url, timeout=8, allow_redirects=False)
                if r.status_code in [200, 301, 403] and len(r.text) > 50:
                    findings.append(f"Possible exposed: {path} ({r.status_code})")
            except:
                pass
        return findings
