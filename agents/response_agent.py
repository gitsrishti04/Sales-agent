# agents/response_agent.py
import ollama

OLLAMA_MODEL = "llama3"

def generate_draft_response(rfp: dict) -> str:
    prompt = f"""You are a professional sales proposal writer for an FMCG supplier.
Given the RFP below, generate a concise cover response (2-3 paragraphs) that:
- Acknowledges the RFP
- Summarizes why our company is a fit
- Mentions key delivery/testing/acceptance highlights

RFP Title: {rfp.get('title')}
Due: {rfp.get('due_date')}
Summary: {rfp.get('summary')}

Write the response as a formal email body (no signatures)."""
    try:
        out = ollama.chat(model=OLLAMA_MODEL, messages=[{"role":"user","content":prompt}])
        return out['choices'][0]['message']['content']
    except Exception as e:
        return f"Draft fallback: We can respond to this RFP. Details: {rfp.get('summary')[:600]}"
