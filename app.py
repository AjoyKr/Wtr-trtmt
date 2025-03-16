import streamlit as st
import pandas as pd
from crew import run_company_search, run_capex_analysis

# Set page title and layout
st.set_page_config(page_title="Opportunity Finder", layout="wide")

# Add Logo
st.image("assets/Crayon-Logo.svg", width=150)

# Title
st.title("💡 Opportunity Finder - Gradiant")

# 📌 Step 1: User Inputs
st.subheader("🔍 Select Industry Vertical")
industry = st.selectbox("Choose Industry:", [
    "Semiconductors and Microelectronics",
    "Food & Beverage",
    "Mining & Resources",
    "Automotive",
    "Pharmaceuticals"
])

st.subheader("📊 Select Number of Companies to Analyze")
num_companies = st.selectbox("How many companies?", [1, 2, 3, 4, 5])

# Run Agents on Button Click
if st.button("🔎 Find Opportunities"):
    st.write("⏳ Searching for top companies and fetching 10-K filings...")
    
    company_data = run_company_search(industry, num_companies)
    st.session_state["company_data"] = company_data

    st.write("✅ Companies found. Now analyzing CAPEX trends...")
    opportunity_results = run_capex_analysis(company_data)
    st.session_state["opportunity_results"] = opportunity_results

# Display Results
if "opportunity_results" in st.session_state:
    st.subheader("💰 Business Opportunities Identified")

    results_df = pd.DataFrame(st.session_state["opportunity_results"])
    st.table(results_df)

    # Add download button
    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results as CSV", csv, "opportunities.csv", "text/csv")

# Reset Button
if st.button("🔄 Reset"):
    st.session_state.clear()
    st.experimental_rerun()

