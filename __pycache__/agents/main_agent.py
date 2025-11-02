# main.py
from agents.rfp_scraper import scrape_rfp_page
from agents.sales_agent import SalesAgent
from agents.main_agent import MainAgent

def main():
    print("🤖 Offline Sales Agent System (Ollama)")
    print("Scanning sample RFP URLs...\n")

    urls = [
        "https://example.com/rfp1",
        "https://example.com/rfp2"
    ]

    # Step 1: Scrape URLs
    rfp_data = [scrape_rfp_page(u) for u in urls]

    # Step 2: Identify and summarize
    sales_agent = SalesAgent()
    rfps_due = sales_agent.identify_rfps_due(rfp_data)
    summaries = sales_agent.summarize_rfps(rfps_due)

    # Step 3: Select RFP to respond to
    chosen = sales_agent.select_rfp_for_response(summaries)
    print(f"📄 Selected RFP: {chosen['title']} (Due {chosen['due_date']})\n")

    # Step 4: Send to Main Agent
    main_agent = MainAgent()
    response = main_agent.respond_to_rfp(chosen)
    print("📝 Generated Response:\n", response)

if __name__ == "__main__":
    main()
