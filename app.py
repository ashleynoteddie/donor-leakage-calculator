import streamlit as st

# 1. Page Configuration & Styling
st.set_page_config(page_title="Donor Velocity Audit", page_icon="📊", layout="centered")

st.title("📊 The Donor Velocity Audit")
st.markdown("""
    Welcome to the diagnostic engine. Answer the baseline questions below to instantly 
    calculate your organization's stalled revenue metrics and priority rescue pipeline.
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

# Dynamic Visibility Block: If they choose $25,000+, ask for the exact number
if major_gift_tier == "$25,000+":
    major_gift_value = st.number_input("What is your specific major gift level threshold ($)?", min_value=25000, step=5000, value=25000)
else:
    # Strip the commas and dollar signs to turn text selections into integers
    major_gift_value = int(major_gift_tier.replace("$", "").replace(",", ""))

donor_percentage = st.selectbox(
    "Roughly what % of your active donor base falls into that major gift tier?",
    ["Less than 2%", "2% - 5%", "6% - 10%", "10%+"]
)

lapsed_range = st.selectbox(
    "And of those donors, how many have not given a gift in the last 12-24 months?",
    ["1-10 (Only a few)", "11-30 (A good amount)", "31-50 (Close to half)", "50+ (We're panicking)"]
)

st.write("---")

# 3. The Backend Calculation Engine
if st.button("Calculate My Stalled Revenue Impact →", type="primary"):
    if not org_name:
        st.warning("Please enter your Organization Name to run the audit.")
    else:
        # Map out the minimum and maximum ranges based on their selections
        if lapsed_range == "1-10 (Only a few)":
            min_lapsed, max_lapsed = 1, 10
        elif lapsed_range == "11-30 (A good amount)":
            min_lapsed, max_lapsed = 11, 30
        elif lapsed_range == "31-50 (Close to half)":
            min_lapsed, max_lapsed = 31, 50
        else:
            min_lapsed, max_lapsed = 51, 100

        # Execute the Velocity Formulas
        min_stalled_revenue = major_gift_value * min_lapsed
        max_stalled_revenue = major_gift_value * max_lapsed
        
        # 4. Display the Strategic Results Output Page Live
        st.success(f"Audit Complete for {org_name}!")
        
        # Create a visually impactful metric dashboard
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Conservative Minimum Revenue Bleed", value=f"${min_stalled_revenue:,.2f}")
        with col2:
            st.metric(label="Maximum Potential Revenue Loss", value=f"${max_stalled_revenue:,.2f}")
            
        st.markdown(f"""
        ### 🧠 Strategic Diagnosis & Action Items:
        * **Current Status:** Based on your answers, you have a critical block of high-capacity major donors who have completely stalled out in your velocity pipeline.
        * **Immediate Action Item:** Your team needs a targeted **Priority Rescue Pipeline** to establish warm bridges back to these accounts before they completely decay. 
        """)