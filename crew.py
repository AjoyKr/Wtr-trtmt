from utils import find_top_companies, fetch_10k_filings, analyze_capex_10k

def run_company_search(industry, num_companies):
    """Find top companies in a selected industry and fetch 10-K filings."""
    print(f"🔍 Searching for {num_companies} companies in industry: {industry}")

    companies = find_top_companies(industry, num_companies)

    if not companies:
        print("❌ ERROR: No companies found. OpenAI search may have failed.")
        return []

    for company in companies:
        print(f"📄 Fetching 10-K filings for {company['name']}")
        filings = fetch_10k_filings(company["name"])
        company["filings"] = filings

    print("✅ Company search complete.")
    return companies

def run_capex_analysis(companies):
    """Analyze CAPEX trends in 10-K filings to identify water treatment opportunities."""
    print("🔎 Running CAPEX analysis...")
    
    results = []
    for company in companies:
        for filing_summary in company.get("filings", []):
            print(f"📑 Analyzing filing for {company['name']}")
            capex_result = analyze_capex_10k(filing_summary, company["name"])
            results.append({
                "Company": company["name"],
                "Increase in CAPEX": capex_result["increase_in_capex"],
                "Opportunity for Water Treatment": capex_result["opportunity_reason"],
                "Source": capex_result["source_url"]
            })

    print("✅ CAPEX analysis complete.")
    return results

