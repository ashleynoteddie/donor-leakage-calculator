import streamlit as st

# 1. Page Configuration & Styling
st.set_page_config(page_title="Donor Revenue Diagnostic", page_icon="📊", layout="centered")

st.title("📊 The Donor Revenue Diagnostic")
st.markdown("""
    Welcome to the diagnostic engine. Answer the baseline questions below to instantly 
    analyze your organization's donor pipeline health.
""")
st.write("---")

# 2. Collect Intake Inputs (The Form)
org_name = st.text_input("Name of Organization")

baseline_revenue = st.selectbox(
    "What is your organization's total annual baseline revenue?",
    ["Under $500k", "$500k - $2M", "$2M - $5M", "$5M+"]
)

major_gift_tier = st.selectbox(
    "What dollar amount is considered a major gift?",
    ["$2,500", "$5,000", "$10,000", "$25,000+"]
)

# Dynamic Visibility Block
if major_gift_tier == "$25,000+":
    major_gift_value = st.number_input("What is your specific major gift level threshold ($)?", min_value=25000, step=5000, value=25000)
else:
    major_gift_value = int(major_gift_tier.replace("$", "").replace(",", ""))

donor_percentage = st.selectbox(
    "Roughly what % of your active donor base falls into that major gift tier?",
    ["Less than 2%", "2% - 5%", "6% - 10%", "10%+"]
)

lapsed_range = st.selectbox(
    "And of those donors, how many have not given a gift in the last 12-24 months?",
    ["0 (We are fully retained!)", "1-10 (Only a few)", "11-30 (A good amount)", "31-50 (Close to half)", "50+ (We're panicking)"]
)

st.write("---")

# 3. The Smart Backend Calculation Engine
if st.button("Run Diagnostic Analysis →", type="primary"):
    if not org_name:
        st.warning("Please enter your Organization Name to run the audit.")
    else:
        # Check for the perfect score first
        if lapsed_range == "0 (We are fully retained!)":
            st.balloons()
            st.success(f"Excellent Health Profile for {org_name}!")
            st.metric(label="Stalled Revenue Risk", value="$0.00")
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** Your major donor pipeline is exceptionally healthy. You have virtually zero leakage in your high-capacity tiers.
            * **Immediate Action Item:** Focus on **donor stewardship and amplification**. Since retention is locked down, look at inviting these active champions into multi-year commitments or legacy giving structures.
            """)
        
        else:
            # Map out the ranges for organizations experiencing leakage
            if lapsed_range == "1-10 (Only a few)":
                min_lapsed, max_lapsed = 1, 10
                status_tier = "Low Risk"
            elif lapsed_range == "11-30 (A good amount)":
                min_lapsed, max_lapsed = 11, 30
                status_tier = "Moderate Risk"
            elif lapsed_range == "31-50 (Close to half)":
                min_lapsed, max_lapsed = 31, 50
                status_tier = "High Risk"
            else:
                min_lapsed, max_lapsed = 51, 100
                status_tier = "Critical Bleed"

            min_stalled_revenue = major_gift_value * min_lapsed
            max_stalled_revenue = major_gift_value * max_lapsed
            
            # 4. Display Tier-Specific Content
            if status_tier in ["High Risk", "Critical Bleed"]:
                st.error(f"Diagnostic Analysis Complete: {status_tier} Status for {org_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Conservative Minimum Revenue Bleed", value=f"${min_stalled_revenue:,.2f}")
                with col2:
                    st.metric(label="Maximum Potential Revenue Loss", value=f"${max_stalled_revenue:,.2f}")
                    
                st.markdown("""
                ### 🧠 Strategic Diagnosis & Action Items:
                * **Current Status:** You have a critical block of high-capacity major donors who have completely stalled out in your pipeline.
                * **Immediate Action Item:** Your team needs a targeted **Priority Rescue Pipeline** to establish warm bridges back to these accounts before they completely decay.
                """)
            else:
                st.warning(f"Diagnostic Analysis Complete: {status_tier} Status for {org_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Stalled Pipeline Value (Low Est.)", value=f"${min_stalled_revenue:,.2f}")
                with col2:
                    st.metric(label="Stalled Pipeline Value (High Est.)", value=f"${max_stalled_revenue:,.2f}")
                    
                st.markdown("""
                ### 🧠 Strategic Diagnosis & Action Items:
                * **Current Status:** Minor pipeline leakage detected. This is normal friction, but it represents low-hanging fruit for expansion.
                * **Immediate Action Item:** Implement a standard **Donor Re-engagement Campaign**. A simple, structured outreach touchpoint over the next 30 days can easily reclaim these accounts.
                """)
