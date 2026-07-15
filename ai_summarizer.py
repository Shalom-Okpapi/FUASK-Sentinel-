from groq import Groq
from settings import BOT_TOKEN  # We'll add GROQ_API_KEY to settings later

class AISummarizer:
    def __init__(self):
        self.client = None
        try:
            from dotenv import load_dotenv
            load_dotenv()
            import os
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)
        except:
            pass

    async def summarize_page(self, page_content, page_name):
        """Generate intelligent summary using AI"""
        if not self.client or len(page_content) < 100:
            return "AI summary not available. Page content too short or API key missing."

        prompt = f"""
        You are a helpful university assistant. Summarize the following webpage content 
        from {page_name} in 2-4 clear sentences. Focus on important announcements, 
        deadlines, admissions, events, or updates. Highlight anything urgent.

        Content:
        {page_content[:8000]}  # Limit to avoid token limits
        """

        try:
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Summary unavailable: {str(e)[:100]}"
