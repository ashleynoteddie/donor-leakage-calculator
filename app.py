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
org_name = st.text_input("Name of Organization", value="Save The World")

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
    [
        "1-3 (Elite retention / normal friction)", 
        "4-10 (Minor pipeline leakage)", 
        "11-30 (A good amount stalled)", 
        "31-50 (Close to half stalled)", 
        "50+ (Critical pipeline decay)"
    ]
)

st.write("---")

# 3. The Smart Backend Calculation Engine
if st.button("Run Diagnostic Analysis →", type="primary"):
    if not org_name:
        st.warning("Please enter your Organization Name to run the audit.")
    else:
        # Map out the ranges based on selection
        if lapsed_range == "1-3 (Elite retention / normal friction)":
            min_lapsed, max_lapsed = 1, 3
            status_tier = "Elite Health"
        elif lapsed_range == "4-10 (Minor pipeline leakage)":
            min_lapsed, max_lapsed = 4, 10
            status_tier = "Low Risk"
        elif lapsed_range == "11-30 (A good amount stalled)":
            min_lapsed, max_lapsed = 11, 30
            status_tier = "Moderate Risk"
        elif lapsed_range == "31-50 (Close to half stalled)":
            min_lapsed, max_lapsed = 31, 50
            status_tier = "High Risk"
        else:
            min_lapsed, max_lapsed = 51, 100
            status_tier = "Critical Bleed"

        # Calculate Nuanced Financial Data
        min_stalled_revenue = major_gift_value * min_lapsed
        max_stalled_revenue = major_gift_value * max_lapsed
        
        min_ltv_impact = min_stalled_revenue * 3
        max_ltv_impact = max_stalled_revenue * 3
        
        # Acquisition cost benchmarked at a conservative $2,500 per lost major donor
        min_replace_cost = min_lapsed * 2500
        max_replace_cost = max_lapsed * 2500
        
        # Scenario 1: Elite Health (The Grace Zone)
        if status_tier == "Elite Health":
            st.success(f"✨ {status_tier} Verification for {org_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Minor Friction Value (Low)", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label="Minor Friction Value (High)", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** Your retention rates are in the top tier of industry standards. This tiny variance represents expected annual attrition (e.g., donors relocating, changing foundations, or shifting focus).
            * **Immediate Action Item:** Run a **Standard Maintenance Review**. No major overhaul campaigns are necessary. A simple, personalized update message to these few accounts will easily ensure they don't drift further.
            """)
        
        # Scenario 2: Low & Moderate Risk
        elif status_tier in ["Low Risk", "Moderate Risk"]:
            st.warning(f"⚠️ {status_tier} Status for {org_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Immediate Budget Gap (Low)", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label="Immediate Budget Gap (High)", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** Minor to moderate pipeline leakage detected. This is a common operational bottleneck, but it represents immediate low-hanging fruit for budget optimization.
            * **Immediate Action Item:** Implement a targeted **Donor Re-engagement Campaign**. A structured 30-day outreach sequence can easily reclaim these warm accounts before connection fades.
            """)
            
        # Scenario 3: High Risk & Critical Bleed
        else:
            st.error(f"🚨 {status_tier} Status for {org_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Conservative Minimum Bleed", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label="Maximum Potential Revenue Loss", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** You have a critical block of high-capacity major donors who have completely stalled out in your pipeline, creating a significant funding gap.
            * **Immediate Action Item:** Your team needs an immediate, dedicated **Priority Rescue Pipeline** strategy to establish high-touch personal bridges back to these accounts.
            """)            with col2:
                st.metric(label="Minor Friction Value (High)", value=f"${max_stalled_revenue:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** Your retention rates are in the top tier of industry standards. This tiny variance represents expected annual attrition (e.g., donors relocating, changing foundations, or shifting focus).
            * **Immediate Action Item:** Run a **Standard Maintenance Review**. No major overhaul campaigns are necessary. A simple, personalized update message to these few accounts will easily ensure they don't drift further.
            """)
        
        # Scenario 2: Low & Moderate Risk
        elif status_tier in ["Low Risk", "Moderate Risk"]:
            st.warning(f"⚠️ {status_tier} Status for {org_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Stalled Pipeline Value (Low)", value=f"${min_stalled_revenue:,.2f}")
            with col2:
                st.metric(label="Stalled Pipeline Value (High)", value=f"${max_stalled_revenue:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** Minor to moderate pipeline leakage detected. This is a common operational bottleneck, but it represents immediate low-hanging fruit for budget optimization.
            * **Immediate Action Item:** Implement a targeted **Donor Re-engagement Campaign**. A structured 30-day outreach sequence can easily reclaim these warm accounts before connection fades.
            """)
            
        # Scenario 3: High Risk & Critical Bleed
        else:
            st.error(f"🚨 {status_tier} Status for {org_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Conservative Minimum Revenue Bleed", value=f"${min_stalled_revenue:,.2f}")
            with col2:
                st.metric(label="Maximum Potential Revenue Loss", value=f"${max_stalled_revenue:,.2f}")
                
            st.markdown("""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Current Status:** You have a critical block of high-capacity major donors who have completely stalled out in your pipeline, creating a significant funding gap.
            * **Immediate Action Item:** Your team needs an immediate, dedicated **Priority Rescue Pipeline** strategy to establish high-touch personal bridges back to these accounts.
            """)
