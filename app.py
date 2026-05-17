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

# DYNAMIC STEP 1: Scale the Major Gift Tier options based on Revenue Tier
if baseline_revenue == "Under $500k":
    tier_options = ["$1,000", "$2,500", "$5,000+"]
elif baseline_revenue == "$500k - $2M":
    tier_options = ["$2,500", "$5,000", "$10,000+"]
elif baseline_revenue == "$2M - $5M":
    tier_options = ["$5,000", "$10,000", "$25,000+"]
else:  # $5M+ Organization
    tier_options = ["$25,000", "$50,000", "$100,000+"]

major_gift_tier = st.selectbox(
    "What dollar amount is considered the entry baseline for a major gift in your program?",
    tier_options
)

# DYNAMIC STEP 2: Handle custom text input if they select the top '+' tier
if "+" in major_gift_tier:
    clean_val = int(major_gift_tier.replace("$", "").replace(",", "").replace("+", ""))
    major_gift_value = st.number_input(f"What is your specific major gift threshold ($)?", min_value=clean_val, step=5000, value=clean_val)
else:
    major_gift_value = int(major_gift_tier.replace("$", "").replace(",", ""))

donor_percentage = st.selectbox(
    "Roughly what % of your active donor base falls into that major gift tier?",
    ["Less than 2%", "2% - 5%", "6% - 10%", "10%+"]
)

lapsed_range = st.selectbox(
    "And of those major donors, what portion have not given a gift in the last 12-24 months?",
    [
        "Minimal friction (1-3% expected attrition)", 
        "Minor pipeline leakage (~7% stalled)", 
        "A noticeable amount (~20% stalled)", 
        "Close to half (~40% stalled)", 
        "Critical pipeline decay (~65% stalled)"
    ]
)

st.write("---")

# 3. Smart Scaling Backend Engine
if st.button("Run Diagnostic Analysis →", type="primary"):
    if not org_name:
        st.warning("Please enter your Organization Name to run the audit.")
    else:
        # Step A: Establish realistic total donor database baseline based on revenue tier
        if baseline_revenue == "Under $500k":
            total_database = 1000
        elif baseline_revenue == "$500k - $2M":
            total_database = 3000
        elif baseline_revenue == "$2M - $5M":
            total_database = 7500
        else:
            total_database = 20000

        # Step B: Determine the major donor percentage midpoint
        if donor_percentage == "Less than 2%":
            mj_pct = 0.01
        elif donor_percentage == "2% - 5%":
            mj_pct = 0.035
        elif donor_percentage == "6% - 10%":
            mj_pct = 0.08
        else:
            mj_pct = 0.12

        # Calculate total baseline of active major donors
        calculated_major_donors = max(1, round(total_database * mj_pct))

        # Step C: Map out the stall rate percentages based on selection
        if "Minimal friction" in lapsed_range:
            stall_rate_min, stall_rate_max = 0.01, 0.03
            status_tier = "Elite Health"
        elif "Minor pipeline leakage" in lapsed_range:
            stall_rate_min, stall_rate_max = 0.04, 0.10
            status_tier = "Low Risk"
        elif "A noticeable amount" in lapsed_range:
            stall_rate_min, stall_rate_max = 0.11, 0.30
            status_tier = "Moderate Risk"
        elif "Close to half" in lapsed_range:
            stall_rate_min, stall_rate_max = 0.31, 0.50
            status_tier = "High Risk"
        else:
            stall_rate_min, stall_rate_max = 0.51, 0.80
            status_tier = "Critical Bleed"

        # Step D: Dynamic Calculations
        min_lapsed = max(1, round(calculated_major_donors * stall_rate_min))
        max_lapsed = max(1, round(calculated_major_donors * stall_rate_max))

        min_stalled_revenue = major_gift_value * min_lapsed
        max_stalled_revenue = major_gift_value * max_lapsed
        
        min_ltv_impact = min_stalled_revenue * 3
        max_ltv_impact = max_stalled_revenue * 3
        
        # Overhead replacement cost estimated at $2,500 per major account
        min_replace_cost = min_lapsed * 2500
        max_replace_cost = max_lapsed * 2500
        
        # Display Results based on Tiers
        if status_tier == "Elite Health":
            st.success(f"✨ {status_tier} Verification for {org_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Minor Friction Value ({min_lapsed} Donor)", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label=f"Minor Friction Value ({max_lapsed} Donors)", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown(f"""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Peer Baseline:** Benchmarked against a standard **{total_database:,} active donor profile** for your operational tier, your organization shows exceptional donor retention.
            * **Current Status:** Your major donor pipeline is remarkably healthy. This tiny variance represents standard expected attrition.
            * **Immediate Action Item:** Focus purely on stewardship. No major recovery campaign is required.
            """)
        
        elif status_tier in ["Low Risk", "Moderate Risk"]:
            st.warning(f"⚠️ {status_tier} Status for {org_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Immediate Budget Gap ({min_lapsed} Donors)", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label=f"Immediate Budget Gap ({max_lapsed} Donors)", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown(f"""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Peer Baseline:** Evaluated against a standard **{total_database:,} active donor profile**, your selections indicate an estimated **{min_lapsed} to {max_lapsed} high-capacity relationships** have disengaged.
            * **Current Status:** Minor to moderate pipeline leakage detected. This represents classic operational friction but is immediate low-hanging fruit for budget optimization.
            * **Immediate Action Item:** Implement a targeted **Donor Re-engagement Campaign**. A structured outreach sequence can easily reclaim these accounts before they completely decay.
            """)
            
        else:
            st.error(f"🚨 {status_tier} Status for {org_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Conservative Minimum Bleed ({min_lapsed} Donors)", value=f"${min_stalled_revenue:,.2f}")
                st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
            with col2:
                st.metric(label=f"Max Potential Revenue Loss ({max_lapsed} Donors)", value=f"${max_stalled_revenue:,.2f}")
                st.metric(label="Est. Donor Replacement Cost", value=f"${max_replace_cost:,.2f}")
                
            st.markdown(f"""
            ### 🧠 Strategic Diagnosis & Action Items:
            * **Peer Baseline:** Analyzed against a standard **{total_database:,} active donor matrix**, your profile indicates a critical breakdown impacting **{min_lapsed} to {max_lapsed} major accounts**.
            * **Current Status:** You have a major block of high-capacity structural funding that has completely stalled out. 
            * **Immediate Action Item:** Your team needs an immediate, high-touch **Priority Rescue Pipeline** strategy to rebuild warm connections to these specific high-value stakeholders.
            """)
