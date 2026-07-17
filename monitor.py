import requests
import hashlib
import json
from datetime import datetime
from .settings import PAGES_TO_MONITOR
from .security_analyzer import SecurityAnalyzer
from .ai_summarizer import AISummarizer

ai_summarizer = AISummarizer()

class WebsiteMonitor:
    def __init__(self):
        self.state_file = "data/state.json"
        self.load_state()

    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        except:
            self.state = {}

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def check_page(self, page):
        url = page["url"]
        name = page["name"]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response_time = response.elapsed.total_seconds()
            
            # Security analysis
            ssl_info = SecurityAnalyzer.check_ssl(url)
            header_analysis = SecurityAnalyzer.check_security_headers(response.headers)
            anomalies = SecurityAnalyzer.analyze_response(response)
            
            content_hash = hashlib.md5(response.text.encode()).hexdigest()
            
            # AI Summary (only for successful pages with substantial content)
            summary = ""
            if response.status_code == 200 and len(response.text) > 500:
                summary = ai_summarizer.summarize_page(response.text, name)
            
            previous = self.state.get(url, {})
            has_changed = previous.get("hash") != content_hash if previous else True
            
            result = {
                "name": name,
                "url": url,
                "status_code": response.status_code,
                "response_time": round(response_time, 2),
                "ssl": ssl_info,
                "security_score": header_analysis["score"],
                "anomalies": anomalies,
                "changed": has_changed,
                "ai_summary": summary[:500] if summary else "",  # Limit length
                "timestamp": datetime.now().isoformat()
            }
            
            self.state[url] = {"hash": content_hash, "last_check": result}
            self.save_state()
            
            return result
            
        except Exception as e:
            return {
                "name": name,
                "url": url,
                "status_code": "Error",
                "error": str(e),
                "anomalies": ["Connection failed"]
            }
