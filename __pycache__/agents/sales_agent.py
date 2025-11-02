# agents/sales_agent.py
from langchain_ollama import ChatOllama
from datetime import datetime, timedelta
import re

class SalesAgent:
    def __init__(self, model="llama3.2"):
        self.model = ChatOllama(model=model)

    def identify_rfps_due(self, rfp_data):
        """Filter RFPs due within next 3 months."""
        now = datetime.now()
        limit = now + timedelta(days=90)
        due_soon = [
            r for r in rfp_data
            if "due_date" in r and now <= datetime.strptime(r["due_date"], "%Y-%m-%d") <= limit
        ]
        return due_soon

    def summarize_rfps(self, rfps):
        """Use Ollama to summarize RFPs."""
        summaries = []
        for r in rfps:
            prompt = f"Summarize this RFP:\nTitle: {r['title']}\nDescription: {r['description']}"
            res = self.model.invoke(prompt)
            summaries.append({"title": r["title"], "summary": res.content, "due_date": r["due_date"]})
        return summaries

    def select_rfp_for_response(self, summaries):
        """Ask model to pick one RFP to respond to."""
        prompt = "Given these RFP summaries, select the best one to respond to:\n"
        for i, r in enumerate(summaries, 1):
            prompt += f"{i}. {r['title']} (Due {r['due_date']}) - {r['summary']}\n"
        prompt += "\nReturn the title of the best RFP."

        res = self.model.invoke(prompt)
        selected_title = res.content.strip()
        chosen = next((r for r in summaries if r["title"].lower() in selected_title.lower()), None)
        return chosen or summaries[0] if summaries else None
