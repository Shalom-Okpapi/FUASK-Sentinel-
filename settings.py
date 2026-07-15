from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Monitoring settings
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 30))

# Pages to monitor
PAGES_TO_MONITOR = [
    {"name": "Homepage", "url": "https://www.fuask.edu.ng/"},
    {"name": "About Us", "url": "https://www.fuask.edu.ng/about-us.php"},
    {"name": "Academics", "url": "https://www.fuask.edu.ng/academics"},
    {"name": "Contact Us", "url": "https://www.fuask.edu.ng/contact-us.php"},
    {"name": "News", "url": "https://www.fuask.edu.ng/news"},
    # Add more pages as needed
]

# Cybersecurity settings
IMPORTANT_SECURITY_HEADERS = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]
ANOMALY_RESPONSE_TIME_MULTIPLIER = 2.5
