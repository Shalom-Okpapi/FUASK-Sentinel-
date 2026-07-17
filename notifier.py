from datetime import datetime

class Notifier:
    @staticmethod
    def format_security_alert(result):
        name = result["name"]
        url = result["url"]
        status = result["status_code"]
        
        emoji = "✅" if status == 200 else "🚨"
        
        message = f"{emoji} **{name}**\n"
        message += f"🔗 {url}\n"
        
        if status == 200:
            message += f"⚡ {result['response_time']}s | Security: {result['security_score']}/100\n"
            
            if result.get("ai_summary"):
                message += f"\n📝 AI Summary:\n{result['ai_summary']}\n"
            
            if result.get("ssl", {}).get("days_left"):
                message += f"🔐 SSL: {result['ssl']['days_left']} days left\n"
        else:
            message += f"❌ Status: {status}\n"
        
        if result.get("anomalies"):
            message += "⚠️ " + ", ".join(result["anomalies"]) + "\n"
        
        message += f"🕒 {datetime.now().strftime('%d %b %Y, %I:%M %p WAT')}"
        return message

    @staticmethod
    def format_daily_report(results):
        working = sum(1 for r in results if r.get("status_code") == 200)
        total = len(results)
        
        report = f"🛡️ **FUASK Sentinel Daily Security Report**\n\n"
        report += f"✅ {working}/{total} pages secure\n\n"
        
        for r in results:
            status_emoji = "✅" if r.get("status_code") == 200 else "❌"
            report += f"{status_emoji} {r['name']} — {r.get('response_time', 'N/A')}s\n"
        
        report += f"\n🕒 Generated at: {datetime.now().strftime('%d %b %Y, %I:%M %p WAT')}"
        return report
