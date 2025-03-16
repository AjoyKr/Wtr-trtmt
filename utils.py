import requests
import openai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to find top companies using OpenAI GPT-4o
def find_top_companies(industry, num_companies):
    """Uses OpenAI GPT-4o to generate a list of the top N companies in a given industry."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()

    prompt = f"""
    You are a business analyst with expertise in global industries.
    List the top {num_companies} companies in the {industry} industry in the USA.
    Provide only the company names in a comma-separated format.
    Example: Intel, AMD, Nvidia, Qualcomm, Broadcom
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in business intelligence."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        company_list = response.choices[0].message.content.strip().split(", ")

        if not company_list or len(company_list) == 0:
            print("❌ ERROR: OpenAI did not return company names.")
            return []

        # Convert to required format
        companies = [{"name": company.strip(), "ticker": "Unknown"} for company in company_list]
        
        print(f"✅ Found companies: {companies}")
        return companies
    
    except openai.OpenAIError as e:
        print(f"❌ ERROR: OpenAI request failed - {str(e)}")
        return []

# Function to summarize 10-K filings using OpenAI GPT-4o
def fetch_10k_filings(company_name):
    """Uses OpenAI to summarize 10-K filings instead of retrieving unavailable 2024/2025 filings."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()

    prompt = f"""
    You are a financial analyst. Assume the current year is 2023.
    Provide a summary of the most recent 10-K filings for {company_name} (2023 or earlier).
    Instead of providing links, summarize key financial trends related to capital expenditures (CAPEX).
    Identify any planned increases in CAPEX and specify which industries or projects are mentioned.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in financial research."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        filings_summary = response.choices[0].message.content.strip()

        if not filings_summary:
            print(f"❌ ERROR: No 10-K filing information found for {company_name}.")
            return []

        print(f"✅ Found filing insights for {company_name}.")
        return [filings_summary]

    except openai.OpenAIError as e:
        print(f"❌ ERROR: OpenAI request failed - {str(e)}")
        return []

# Function to analyze CAPEX trends using OpenAI GPT-4o (assuming 2023 is the present year)
def analyze_capex_10k(filing_summary, company_name):
    """Uses OpenAI to analyze CAPEX trends in 10-K reports and provide structured output similar to ChatGPT results."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()

    prompt = f"""
    You are a financial analyst reviewing the 10-K filing for {company_name} (2023 or earlier).
    Provide a **structured summary** of planned **capital expenditures (CAPEX)** that could indicate a **need for water treatment solutions**.
    
    **Format your response as follows:**
    
    **Company:** {company_name}
    
    **CapEx Plans:**
    - **[Year]**: [Description of CAPEX increase, including specific numbers if available]
    - **Beyond [Year]**: [Long-term investment plans related to CAPEX]
    
    **Potential Need for Gradiant's Offerings:**
    - **[Project Type]**: [How the CAPEX spending might require advanced water treatment solutions]
    - **[Location]**: [Specific locations or industries that will be impacted]
    
    **Example Output Format:**  
    ```
    **Company:** Intel  
    
    **CapEx Plans:**  
    - **2024**: Planned a 2% increase in CapEx to $26.2 billion.  
    - **Beyond 2024**: Received $8.5 billion from the CHIPS and Science Act to build four new semiconductor fabs.  
    
    **Potential Need for Gradiant's Offerings:**  
    - **New Fabs Construction**: Water-intensive processes in new semiconductor fabs in Arizona and Ohio require wastewater treatment.  
    - **Upgrading Existing Plants**: Increased environmental regulations require water recycling systems in Oregon and New Mexico plants.  
    ```
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in financial analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2  # Reduce randomness for structured output
        )

        capex_analysis = response.choices[0].message.content.strip()

        return {
            "increase_in_capex": capex_analysis.split("**CapEx Plans:**")[1].split("**Potential Need")[0].strip() if "**CapEx Plans:**" in capex_analysis else "N/A",
            "opportunity_reason": capex_analysis.split("**Potential Need for Gradiant's Offerings:**")[1].strip() if "**Potential Need for Gradiant's Offerings:**" in capex_analysis else "N/A",
            "source_url": "Analyzed based on latest available 10-K summary."
        }
    except openai.OpenAIError as e:
        return {"increase_in_capex": "Error", "opportunity_reason": str(e), "source_url": "Analyzed based on latest available 10-K summary."}

