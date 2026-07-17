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
        working = [r for r in results if r.get("status_code") == 200]
        problems = [r for r in results if r.get("status_code") != 200]
        
        message = "🛡️ **FUASK Sentinel Security Report**\n\n"
        
        if problems:
            message += f"🚨 {len(problems)} page(s) have issues. {len(working)} out of {len(results)} pages are working fine.\n\n"
            
            for p in problems:
                message += f"❌ **{p['name']}**\n"
                if p.get("status_code") == "Error" or p.get("error"):
                    message += f"   └ server returned error: {p.get('error', p.get('status_code'))}\n"
                else:
                    message += f"   └ Status: {p.get('status_code')}\n"
                message += f"   └ {p['url']}\n\n"
        else:
            message += f"✅ All {len(results)} pages are working normally.\n\n"
        
        message += f"🕐 Checked at: {datetime.now().strftime('%a %d %b, %I:%M %p WAT')}\n"
        message += "\nThe bot will keep monitoring. Fix any issues quickly."
        
        return message
