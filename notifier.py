from datetime import datetime

class Notifier:
    @staticmethod
    def format_security_alert(result):
        name = result["name"]
        url = result["url"]
        
        if result.get("status_code") == 200:
            emoji = "✅"
            status = "Working"
        else:
            emoji = "🚨"
            status = "Problem Detected"
        
        message = f"{emoji} **{name}**\n"
        message += f"🔗 {url}\n"
        message += f"Status: {status}\n"
        
        if result.get("ai_summary"):
            message += f"\n📝 Summary:\n{result['ai_summary']}\n"
        
        if result.get("defaced"):
            message += "⚠️ Possible Defacement Detected!\n"
        
        if result.get("anomalies"):
            message += "Warnings: " + ", ".join(result["anomalies"]) + "\n"
        
        message += f"🕒 {datetime.now().strftime('%d %b %Y, %I:%M %p WAT')}"
        return message

    @staticmethod
    def format_daily_report(results):
        problems = [r for r in results if r.get("status_code") != 200]
        message = "🛡️ **FUASK Sentinel Daily Security Report**\n\n"
        
        message += f"✅ {len(results) - len(problems)} pages OK\n"
        if problems:
            message += f"🚨 {len(problems)} pages have issues\n\n"
            for p in problems:
                message += f"❌ {p['name']}\n"
        
        message += f"\n🕒 Checked at: {datetime.now().strftime('%d %b %Y, %I:%M %p WAT')}"
        return message
