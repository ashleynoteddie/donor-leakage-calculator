import streamlit as st
import requests
import json

# 1. Page Configuration & Branded Styling
st.set_page_config(page_title="The NSQ Pipeline Integrity Audit", page_icon="⚡", layout="centered")

# Main Branded Headers
st.title("⚡ The NSQ Pipeline Integrity Audit")
st.subheader("by NSQ Solutions")
st.markdown("""
    Uncover immediate operational friction, 3-year compounded pipeline decay, 
    and the systemic bottlenecks preventing predictable, non-status-quo revenue growth.
""")
st.write("---")

# PASTE YOUR GOOGLE DEPLOYMENT WEB APP URL HERE (Ends in /exec)
WEB_APP_URL = "PASTE_YOUR_WEB_APP_URL_HERE"

# 2. Collect Intake Inputs (The Form)
org_name = st.text_input("Name of Organization", value="Save The World")

baseline_revenue = st.selectbox(
    "What is your organization's total annual baseline revenue?",
    ["Under $500k", "$500k - $2M", "$2M - $5M", "$5M+"]
)

# Scale the Pipeline Anchor Tier options based on Revenue Tier
if baseline_revenue == "Under $500k":
    tier_options = ["$1,000", "$2,500", "$5,000+"]
elif baseline_revenue == "$500k - $2M":
    tier_options = ["$2,500", "$5,000", "$10,000+"]
elif baseline_revenue == "$2M - $5M":
    tier_options = ["$5,000", "$10,000", "$25,000+"]
else:  # $5M+ Organization
    tier_options = ["$25,000", "$50,000", "$100,000+"]

major_gift_tier = st.selectbox(
    "What dollar amount represents the entry threshold for your pipeline's anchor tier (major gifts)?",
    tier_options
)

if "+" in major_gift_tier:
    clean_val = int(major_gift_tier.replace("$", "").replace(",", "").replace("+", ""))
    major_gift_value = st.number_input(f"What is your specific anchor tier threshold ($)?", min_value=clean_val, step=5000, value=clean_val)
else:
    major_gift_value = int(major_gift_tier.replace("$", "").replace(",", ""))

donor_percentage = st.selectbox(
    "Roughly what % of your active base sits within or above this anchor tier?",
    ["Less than 2%", "2% - 5%", "6% - 10%", "10%+"]
)

lapsed_range = st.selectbox(
    "Of those anchor relationships, what portion have lapsed (no gift in 12-24 months)?",
    [
        "Minimal friction (1-3% expected attrition)", 
        "Minor pipeline leakage (~7% stalled)", 
        "A noticeable amount (~20% stalled)", 
        "Close to half (~40% stalled)", 
        "Critical pipeline decay (~65% stalled)"
    ]
)

st.write("---")

# Initialize session state for the email gate
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "data_logged" not in st.session_state:
    st.session_state.data_logged = False

# Step 1: Trigger Audit Processing
if st.button("Process Pipeline Integrity Audit →", type="primary") or st.session_state.form_submitted:
    st.session_state.form_submitted = True
    
    # 3. THE NSQ VALUE GATE FORM
    st.markdown("### 📥 Secure Your Executive Briefing")
    st.info("To compile your 3-year structural risk matrix and custom pipeline stabilization roadmap, verify your professional coordinates:")
    
    user_name = st.text_input("Your Full Name")
    user_role = st.selectbox("Your Role / Title", ["Executive Director", "Board Member", "VP of Development / CDO", "Development Director", "Other / Advisor"])
    user_email = st.text_input("Professional Email Address")
    
    # Step 2: Final Unlock Button
    if st.button("Unlock Integrity Audit Dashboard ↓", type="secondary"):
        if not user_name or not user_email:
            st.error("Please provide your name and professional email address to view the audit data.")
        elif not org_name:
            st.error("Please ensure the Organization Name field is completed at the top.")
        else:
            st.write("---")
            
            # --- Systemic Backend Engineering ---
            if baseline_revenue == "Under $500k":
                total_database = 1000
            elif baseline_revenue == "$500k - $2M":
                total_database = 3000
            elif baseline_revenue == "$2M - $5M":
                total_database = 7500
            else:
                total_database = 20000

            if donor_percentage == "Less than 2%":
                mj_pct = 0.01
            elif donor_percentage == "2% - 5%":
                mj_pct = 0.035
            elif donor_percentage == "6% - 10%":
                mj_pct = 0.08
            else:
                mj_pct = 0.12

            calculated_major_donors = max(1, round(total_database * mj_pct))

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

            min_lapsed = max(1, round(calculated_major_donors * stall_rate_min))
            max_lapsed = max(1, round(calculated_major_donors * stall_rate_max))

            min_stalled_revenue = major_gift_value * min_lapsed
            max_stalled_revenue = major_gift_value * max_lapsed
            min_ltv_impact = min_stalled_revenue * 3
            max_ltv_impact = max_stalled_revenue * 3
            min_replace_cost = min_lapsed * 2500
            max_replace_cost = max_lapsed * 2500
            
            # --- SILENT WEBHOOK LOGGER ---
            if not st.session_state.data_logged and WEB_APP_URL != "https://script.google.com/macros/s/AKfycbzaW_zpDby0Xy_dtPafEEAWdCIIRxa3mWtexLaiRAdXHhY6L0sR--Ck3dzZjM_cwfrGbQ/exec":
                payload = {
                    "organization": org_name,
                    "name": user_name,
                    "role": user_role,
                    "email": user_email,
                    "deficit": f"${max_ltv_impact:,.2f}"
                }
              try:
                    response = requests.post(WEB_APP_URL, data=json.dumps(payload), timeout=10)
                    st.session_state.data_logged = True
                    st.toast("Audit processing triggered!", icon="⚡")
                    
                    # DIAGNOSTIC FEEDBACK: This will print the status on your live app
                    st.write(f"🔬 Debug Status Code: {response.status_code}")
                    st.write(f"🔬 Debug Response Text: {response.text}")
                except Exception as e:
                    st.error(f"❌ Network Connection Error: {str(e)}")
            
            # --- DISPLAY AUDIT RESULTS PANEL ---
            if status_tier == "Elite Health":
                st.success(f"✨ {status_tier} Verification for {org_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=f"Minor Pipeline Friction ({min_lapsed} Account)", value=f"${min_stalled_revenue:,.2f}")
                    st.metric(label="3-Year Compounded Impact", value=f"${min_ltv_impact:,.2f}")
                with col2:
                    st.metric(label=f"Minor Pipeline Friction ({max_lapsed} Accounts)", value=f"${max_stalled_revenue:,.2f}")
                    st.metric(label="Est. Account Replacement Cost", value=f"${max_replace_cost:,.2f}")
                    
                st.markdown(f"""
                ### 🧠 NSQ Strategic Diagnosis & Action Items for {user_name}:
                * **The Benchmark:** Benchmarked against a standard **{total_database:,} active pipeline matrix** for your operational scale, your core retention is in the top tier of industry standards.
                * **The NSQ Perspective:** Status-quo consultants will tell you to coast because your numbers are green. We disagree. Exceptional retention means your anchor tier is primed for **amplification and expansion**. 
                * **Immediate Action:** Pivot from preservation to leverage. Look at transitioning these highly secure, active champions into multi-year commitments or collaborative seed-funding initiatives.
                """)
            
            elif status_tier in ["Low Risk", "Moderate Risk"]:
                st.warning(f"⚠️ {status_tier} Operational Friction for {org_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=f"Immediate Cash Drag ({min_lapsed} Accounts)", value=f"${min_stalled_revenue:,.2f}")
                    st.metric(label="3-Year Compounded Deficit", value=f"${min_ltv_impact:,.2f}")
                with col2:
                    st.metric(label=f"Immediate Cash Drag ({max_lapsed} Accounts)", value=f"${max_stalled_revenue:,.2f}")
                    st.metric(label="Est. Account Replacement Cost", value=f"${max_replace_cost:,.2f}")
                    
                st.markdown(f"""
                ### 🧠 NSQ Strategic Diagnosis & Action Items for {user_name}:
                * **The Benchmark:** Evaluated against a standard **{total_database:,} active donor profile**, your selections indicate that **{min_lapsed} to {max_lapsed} core revenue relationships** have silently drifted away.
                * **The NSQ Perspective:** Chasing new, unvetted donor acquisition to fill this gap is a status-quo trap that drains team capacity. Your most efficient, immediate pathway to budget optimization sits right on your baseline bench.
                * **Immediate Action:** Implement a targeted, non-transactional **Relationship Stabilization Blueprint**. A structured, high-stewardship touchpoint sequence over the next 30 days can cleanly reactivate these warm accounts.
                """)
                
            else:
                st.error(f"🚨 {status_tier} Systemic Pipeline Leakage for {org_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=f"Conservative Immediate Bleed ({min_lapsed} Donors)", value=f"${min_stalled_revenue:,.2f}")
                    st.metric(label="3-Year Compounded Deficit", value=f"${min_ltv_impact:,.2f}")
                with col2:
                    st.metric(label=f"Max Potential Structural Loss ({max_lapsed} Donors)", value=f"${max_stalled_revenue:,.2f}")
                    st.metric(label="Est. Account Replacement Cost", value=f"${max_replace_cost:,.2f}")
                    
                st.markdown(f"""
                ### 🧠 NSQ Strategic Diagnosis & Action Items for {user_name}:
                * **The Benchmark:** Analyzed against a standard **{total_database:,} active donor matrix**, your data indicates a deep architectural breakdown impacting **{min_lapsed} to {max_lapsed} anchor relationships**.
                * **The NSQ Perspective:** This degree of decay is a lagging indicator of structural fatigue. Simply screaming louder for major gifts or hiring a generic fundraising agency will not patch this hull. You have a systemic engagement design flaw.
                * **Immediate Action:** You require an immediate, high-touch **Priority Pipeline Rescue Mechanism** to re-architect how your leadership team bridges, interfaces, and locks in long-term alignment with core ecosystem stakeholders.
                """)
